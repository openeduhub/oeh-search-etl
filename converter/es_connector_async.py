from __future__ import annotations

import asyncio
import base64
import json
import logging
import os
from typing import TypeVar

import scrapy
from aiohttp import BasicAuth
from scrapy.utils.project import get_project_settings

import edu_sharing_async as es
from converter.es_connector_common import transform_item, EduSharingConstants
from converter.util import async_timed
from edu_sharing_async.rest import ApiException


log = logging.getLogger(__name__)
_T = TypeVar('_T')
_T_co = TypeVar('_T_co')


def config():
    settings = get_project_settings()
    configuration = es.Configuration()
    configuration.host = settings.get("EDU_SHARING_BASE_URL") + "rest"
    configuration.username = settings.get("EDU_SHARING_USERNAME")
    configuration.password = settings.get("EDU_SHARING_PASSWORD")
    return configuration


def mc_uuid(group):
    return EduSharingConstants.GROUP_PREFIX + EduSharingConstants.MEDIACENTER_PREFIX + group


def grp_uuid(group):
    return EduSharingConstants.GROUP_PREFIX + group


class GroupManager:
    def __init__(self, client: es.ApiClient):
        self._group_names: set[str] = set()
        self.iam_api = es.IAMV1Api(client)
        self.media_center_api = es.MEDIACENTERV1Api(client)
        self._lock = asyncio.Lock()

    async def init(self):
        print('initializing group manager')
        result: es.GroupEntries = await self.iam_api.search_groups(repository=EduSharingConstants.HOME, pattern="", max_items=1000000)
        for group_entry in result.groups:
            ge: es.Group = group_entry
            self._group_names.add(ge.authority_name)
        print(f'edusharing groupmanager initialized, recieved {len(self._group_names)} groups')

    async def _create_mediacenter(self, group) -> str:
        result = await self.media_center_api.create_mediacenter(
            repository=EduSharingConstants.HOME,
            mediacenter=group,
            body={"mediacenter": {}, "displayName": group}
        )
        name = result["authorityName"]
        self._group_names.add(name)
        return name

    async def _create_group(self, group) -> str:
        result = await self.iam_api.create_group(repository=EduSharingConstants.HOME, group=group, body={})
        name = result["authorityName"]
        self._group_names.add(name)
        return name

    async def _group_exists_in_repository(self, uuid) -> bool:
        try:
            _ = await self.iam_api.get_group(EduSharingConstants.HOME, uuid)
            logging.info(f"Group {uuid} was found in edu-sharing")
            return True
        except ApiException:
            logging.info(f"Group {uuid} was not found in edu-sharing")
            return False

    async def _add_group(self, uuid, group) -> str:
        # check is necessary in case another thread added it while we were waiting.
        if uuid in self._group_names:
            return uuid
        if True is await self._group_exists_in_repository(uuid):
            logging.info(f"Group {uuid} was found in edu-sharing (cache inconsistency), no need to create")
            self._group_names.add(uuid)
            return uuid
        return await self._create_group(group)

    async def _add_mediacenter(self, uuid, group) -> str:
        # check is necessary in case another thread added it while we were waiting.
        if uuid in self._group_names:
            return uuid
        if True is await self._group_exists_in_repository(uuid):
            logging.info(f"Group {uuid} was found in edu-sharing (cache inconsistency), no need to create")
            self._group_names.add(uuid)
            return uuid
        return await self._create_mediacenter(group)

    async def sync_groups(self, groups_to_sync, mediacenters_to_sync):
        missing_groups = dict()
        missing_mcs = dict()
        # check if we need to add groups/media centers
        for g in groups_to_sync:
            uuid = grp_uuid(g)
            if uuid not in self._group_names:
                missing_groups[uuid] = g
            else:
                yield uuid
        for mc in mediacenters_to_sync:
            uuid = mc_uuid(mc)
            if uuid not in self._group_names:
                missing_mcs[uuid] = mc
            else:
                yield uuid

        async with self._lock:
            for uuid, grp in missing_groups.items():
                yield await self._add_group(uuid, grp)
            for uuid, mc in missing_mcs.items():
                yield await self._add_mediacenter(uuid, mc)


class AsyncEsApiClient(es.ApiClient):
    _instance = None
    _lock = asyncio.Lock()
    _loop = None
    _group_manager: GroupManager = None

    @classmethod
    def get_instance_blocking(cls):
        if 'SCRAPY_CHECK' in os.environ:
            return None
        loop = asyncio.get_event_loop()
        client = loop.run_until_complete(cls.get_instance())
        return client

    @classmethod
    async def get_instance(cls):
        # if cls._instance is not None:
        #     return cls._instance
        #
        async with cls._lock:
            # check if someone was faster
            if cls._instance is not None:
                return cls._instance
            cls._loop = asyncio.get_event_loop()
            if not cls._loop.is_running():
                cls._loop.run_forever()
            cls._instance = cls(configuration=config(), header_name='Accept', header_value='application/json')
            await cls._instance.auth_or_raise()
            cls._group_manager = GroupManager(cls._instance)
            await cls._group_manager.init()
            return cls._instance

    def __init__(self, configuration=None, header_name=None, header_value=None, cookie=None, cache=None):
        super().__init__(configuration, header_name, header_value, cookie)
        log.error('AsyncEsApiClient.__init__')
        self.refresh_session_task = asyncio.create_task(self.refresh_session())
        self.bulk_api = es.BULKV1Api(self)
        self.media_center_api = es.MEDIACENTERV1Api(self)
        self.iam_api = es.IAMV1Api(self)
        self.node_api = es.NODEV1Api(self)
        self.auth_data = None

    @property
    def aio_client(self):
        return self.rest_client.pool_manager

    def deserialize(self, response, response_type):
        """
        we sometimes allow invalid objects into the EduSharing backend.
        But the Models here check for this, so we don't use them.
        so instead of returning from `self.__deserialize(data, response_type)`
        we just return `data`.
        :param response:
        :param response_type:
        :return:
        """
        try:
            return super().deserialize(response, response_type)
        except ValueError:
            #  failed to deserialize from model object
            try:
                return json.loads(response.data)
            except ValueError:
                return response.data

    async def auth_or_raise(self):
        """
        initial authentication, throws if something's wrong.
        :return:
        """
        if self.auth_data is not None:
            return
        headers = {'Accept': 'application/json'}
        auth_url = self.configuration.host + '/authentication/v1/validateSession'
        auth_obj = BasicAuth(self.configuration.username, self.configuration.password)
        async with self.rest_client.pool_manager.get(auth_url, auth=auth_obj, headers=headers) as auth_resp:
            if not auth_resp.ok:
                raise RuntimeError(f'auth on EduSharing backend failed {auth_resp.reason}')
            self.auth_data = await auth_resp.json()
            print(f'client authenticated: {auth_resp.reason}')

    async def refresh_session(self) -> None:
        """
        grab a session cookie and refresh it every 5 minutes until canceled
        """
        headers = {'Accept': 'application/json'}
        auth_url = self.configuration.host + '/authentication/v1/validateSession'
        auth_obj = BasicAuth(self.configuration.username, self.configuration.password)
        retries = 3
        while True:
            async with self.rest_client.pool_manager.get(auth_url, auth=auth_obj, headers=headers) as auth_resp:
                if not auth_resp.ok:
                    if retries < 0:
                        # give up
                        break
                    retries -= 1
                    log.error(f'auth on EduSharing backend failed {auth_resp.reason}')
                    continue  # try again
                log.debug('auth to EduSharing completed successfully')
                retries = 3
                self.auth_data = await auth_resp.json()
                # print(result_data)
            await asyncio.sleep(60*5)

        # TODO: handle error and close client
        self._loop.stop()
        self.rest_client.pool_manager.close()
        raise RuntimeError('could not authenticate with EduSharing after three retries, gave up and closed client')

    @async_timed
    async def find_item(self, spider: scrapy.Spider, node_id: str):
        properties = {
            "ccm:replicationsource": [spider.name],
            "ccm:replicationsourceid": [node_id],
        }
        try:
            response = await self.bulk_api.find(properties)
            properties = response["node"]["properties"]
            if (
                "ccm:replicationsourcehash" in properties
                and "ccm:replicationsourceuuid" in properties
            ):
                return [
                    properties["ccm:replicationsourceuuid"][0],
                    properties["ccm:replicationsourcehash"][0],
                ]
        except ApiException as e:
            if e.status == 404:
                pass
            else:
                raise e
        return None

    @async_timed
    async def insert_item(self, spider, uuid, item, reset_version=False):
        transformed = transform_item(uuid, spider, item)
        node = await self.sync_node(spider, "ccm:io", transformed, reset_version)
        node_id = node["ref"]["id"]
        await self.set_node_permissions(node_id, item)
        await self.set_node_preview(node_id, item)
        await self.set_node_text(node_id, item)

    @async_timed
    async def set_node_text(self, uuid, item) -> bool:
        if "fulltext" not in item:
            return False
        headers = {
            "Accept": "application/json",
            "Content-Type": "multipart/form-data",
        }
        url = get_project_settings().get("EDU_SHARING_BASE_URL")
        path = f'rest/node/v1/nodes/-home-/{uuid}/textContent?mimetype=text/plain'
        data = item["fulltext"].encode("utf-8")
        async with self.aio_client.post(url+path, headers=headers, data=data) as response:
            return response.ok

    @async_timed
    async def sync_node(self, spider, _type, properties, reset_version=False):
        group_by = []
        if "ccm:replicationsourceorigin" in properties:
            group_by = ["ccm:replicationsourceorigin"]
        try:
            response = await self.bulk_api.sync(
                body=properties,
                match=["ccm:replicationsource", "ccm:replicationsourceid"],
                type=_type,
                group=spider.name,
                group_by=group_by,
                reset_version=reset_version,
            )
        except ApiException as e:
            json_error = json.loads(e.body)
            if json_error["error"] == "java.lang.IllegalStateException":
                logging.warning("Node '" + properties['cm:name'][0] + "' probably blocked for sync: " + json_error["message"])
                return None
            raise e
        return response["node"]

    async def set_node_permissions(self, uuid, item):
        if "permissions" not in item:
            return
        permissions = {
            "inherited": True,  # let inherited = true to add additional permissions via edu-sharing
            "permissions": [],
        }
        if item["permissions"]["public"] is True:
            if "groups" in item["permissions"] or "mediacenters" in item["permissions"]:
                logging.error(
                    "Invalid state detected: Permissions public is set to true but groups or mediacenters are also set. Please use either public = true without groups/mediacenters or public = false and set group/mediacenters. No permissions will be set!"
                )
                return
            data = {
                "inherited": True,  # let inherited = true to add additional permissions via edu-sharing
                "permissions": [{
                    "authority": {
                        "authorityName": EduSharingConstants.GROUP_EVERYONE,
                        "authorityType": EduSharingConstants.AUTHORITYTYPE_EVERYONE,
                    },
                    "permissions": [
                        EduSharingConstants.PERMISSION_CONSUMER,
                        EduSharingConstants.PERMISSION_CCPUBLISH,
                    ],
                }],
            }
            print('p', end='', flush=True)
            if not await self.set_permissions(uuid, data):
                logging.error(
                    "Failed to set permissions, please check that the given groups/mediacenters are existing in the repository or set the autoCreate mode to true"
                )
                logging.error(item["permissions"])
            print('P', end='', flush=True)
            return
        # Makes not much sense, may no permissions at all should be set
        # if not 'groups' in item['permissions'] and not 'mediacenters' in item['permissions']:
        #    logging.error('Invalid state detected: Permissions public is set to false but neither groups or mediacenters are set. Please use either public = true without groups/mediacenters or public = false and set group/mediacenters. No permissions will be set!')
        #    return
        groups_to_sync: list[str] = []
        mediacenters_to_sync: list[str] = []
        if "groups" in item["permissions"]:
            if True is item["permissions"].get("autoCreateGroups", None):
                groups_to_sync = item["permissions"]['groups']
        if "mediacenters" in item["permissions"]:
            if True is item["permissions"].get("autoCreateMediacenters", None):
                mediacenters_to_sync = item["permissions"]["mediacenters"]
        async for group_uuid in self._group_manager.sync_groups(groups_to_sync, mediacenters_to_sync):
            permissions["permissions"].append(
                {
                    "authority": {
                        "authorityName": group_uuid,
                        "authorityType": EduSharingConstants.AUTHORITYTYPE_GROUP,
                    },
                    "permissions": [
                        EduSharingConstants.PERMISSION_CONSUMER,
                        EduSharingConstants.PERMISSION_CCPUBLISH,
                    ],
                }
            )
        if not await self.set_permissions(uuid, permissions):
            logging.error(
                "Failed to set permissions, please check that the given groups/mediacenters are existing in the repository or set the autoCreate mode to true"
            )
            logging.error(item["permissions"])

    @async_timed
    async def set_permissions(self, uuid, permissions) -> bool:
        try:
            await self.node_api.set_permission(
                repository=EduSharingConstants.HOME,
                node=uuid,
                body=permissions,
                send_mail=False,
                send_copy=False,
            )
            return True
        except ApiException:
            return False

    async def set_node_preview(self, uuid, item) -> bool:
        if "thumbnail" not in item:
            if get_project_settings().get("DISABLE_SCRAPY") is False:
                logging.warning("No thumbnail provided for " + uuid)
            return False
        key = (
            "large"
            if "large" in item["thumbnail"]
            else "small"
            if "small" in item["thumbnail"]
            else None
        )
        if not key:
            return False

        url = get_project_settings().get("EDU_SHARING_BASE_URL")
        path = f'rest/node/v1/nodes/-home-/{uuid}/preview?mimetype={item["thumbnail"]["mimetype"]}'
        headers = {"Accept": "application/json"}
        files = {"image": base64.b64decode(item["thumbnail"][key])}
        async with self.aio_client.post(url+path, headers=headers, files=files) as response:
            return response.ok


async def main():
    configuration = config()

    api_client = AsyncEsApiClient(configuration=configuration, header_name='Accept', header_value='application/json')
    properties = {
        "ccm:replicationsource": ['zum_klexikon_spider'],
        "ccm:replicationsourceid": ['6089'],
    }
    bulk_api = es.BULKV1Api(api_client)
    result = await bulk_api.find(properties)
    print(result["node"]["properties"])


if __name__ == '__main__':
    asyncio.run(main())
