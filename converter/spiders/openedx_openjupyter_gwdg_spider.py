import pprint
from typing import Iterable, Any

import scrapy
from scrapy import Request
from scrapy.http import Response

from converter.web_tools import WebEngine


class OpenedxOpenjupyterGwdgSpider(scrapy.Spider):
    name: str = "openedx_openjupyter_gwdg_spider"
    friendlyName: str = "Open-Jupyter (GWDG) edX"
    version: str = "0.0.1"  # last update: 2024-03-20
    custom_settings: dict = {
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_DEBUG": True,
        "WEB_TOOLS": WebEngine.Playwright,
        "ROBOTSTXT_OBEY": False,
    }
    open_edx_api_url: str = "https://edx.open-jupyter.gwdg.de/api/"
    # API docs: https://courses.edx.org/api-docs/

    def start_requests(self) -> Iterable[Request]:
        # Dummy Request: check if the edX URL is available, afterward use the API to fetch individual courses
        yield scrapy.Request(url="https://edx.open-jupyter.gwdg.de/", callback=self.openedx_request_courses)

    def openedx_request_courses(self, response: scrapy.http.Response):
        _api_courses_endpoint = f"{self.open_edx_api_url}courses/v1/courses/"
        yield scrapy.Request(url=_api_courses_endpoint, priority=2, callback=self.openedx_handle_course_list)

    def openedx_handle_course_list(self, response: scrapy.http.TextResponse):
        # see: https://courses.edx.org/api-docs/#/courses/courses_v1_courses_list
        if response.status == 200:
            response_dict: dict = response.json()
            try:
                results: list[dict] = response_dict["results"]
                pagination: dict = response_dict["pagination"]
                # ToDo:
                #  - check 'pagination' object:
                #       - count
                #       - next
                #       - num_pages
                #       - previous
                #  - iterate through all API pages if necessary
            except KeyError as ke:
                raise ke
            if results:
                # happy case -> request individual course details
                self.logger.debug(
                    f"Open edX 'courses' API returned {len(results)} courses. "
                    f"Trying to fetch course details next..."
                )
                for result_item in results:
                    course_dict: dict = result_item
                    course_id: str = course_dict["id"]
                    # ATTENTION: While the Open edX API
                    if course_id:
                        # the course_id string might look like this: "course-v1:OpenJupyter+DS101+SoSe2023"
                        _api_course_details_endpoint: str = f"{self.open_edx_api_url}courses/v1/courses/{course_id}"
                        yield scrapy.Request(
                            url=_api_course_details_endpoint,
                            callback=self.openedx_handle_course_details,
                            cb_kwargs={"course_dict": course_dict},
                        )
                    else:
                        self.logger.error(
                            f"Cannot query 'Open edX' API course details endpoint without a valid course 'id'!"
                        )
                    pass
                pass
            else:
                self.logger.warning(
                    f"Open edX API returned HTTP Status 200 for {response.url}, "
                    f"but the 'results' object was missing!"
                )
        else:
            # ToDo: error-handling for unexpected API responses
            # Possible HTTP Response Codes according to the API specs:
            # * 200 on success, with a list of course discovery objects as returned
            #   by `CourseDetailView`.
            # * 400 if an invalid parameter was sent or the username was not provided
            #   for an authenticated request.
            # * 403 if a user who does not have permission to masquerade as
            #   another user specifies a username other than their own.
            # * 404 if the specified user does not exist, or the requesting user does
            #   not have permission to view their courses.
            pass
        pass

    def openedx_handle_course_details(self, response: scrapy.http.TextResponse, **kwargs):
        # see: https://courses.edx.org/api-docs/#/courses/courses_v1_courses_read
        # the API request for course details has an additional (necessary) property:
        # 'overview' contains a "possibly verbose HTML textual description of the course"
        if response.status == 200 and response.cb_kwargs:
            course_details: dict = response.json()
            try:
                course_dict: dict = response.cb_kwargs["course_dict"]
            except KeyError as ke:
                raise ke
            if isinstance(course_details, dict) and isinstance(course_dict, dict):
                course_dict_merged = course_dict | course_details
                course_url: str = f"https://edx.open-jupyter.gwdg.de/courses/{course_dict_merged['id']}/about"
                # ToDo: confirm later if this URL structure is stable across all courses
                yield scrapy.Request(
                    url=course_url, callback=self.parse, cb_kwargs={"course_dict_merged": course_dict_merged}
                )
        else:
            self.logger.error(f"Retrieving course details from open edX API failed for item {response.url}")
            pass
        pass

    def parse(self, response: Response, **kwargs: Any) -> Any:
        try:
            # if response.cb_kwargs:
            #     if "course_dict" in response.cb_kwargs:
            course_dict = response.cb_kwargs["course_dict_merged"]
        except KeyError:
            # ToDo: log error if course_dict was not available (-> no metadata extraction possible)
            self.logger.error(
                f"Dropping item {response.url} since no metadata dictionary was available in Scrapy's "
                f"'cb_kwargs'. (The 'parse()'-method expected a metadata dictionary from two 'open edX' "
                f"API endpoints!)"
            )
            return None
        # ToDo: metadata extraction from open edX
        #  - 'effort'                                   ?
        #  - 'end'                                      "ccm:license_to"
        #  - 'enrollment_end'                           ?
        #  - 'enrollment_start'                         ?
        #  - 'hidden'                                   "BaseItem.status" -> 'ccm:editorial_state"
        #  - 'id'                                       "BaseItem.sourceId"
        #  - 'media' (object):
        #    - 'media.banner_image.uri_absolute'        ?
        #    - 'media.course_image.uri'                 "ccm:oeh_course_url_image" ?
        #    - 'media.course_video.uri                  "ccm:oeh_course_url_video" ?
        #    - 'media.image.raw'                        "BaseItem.thumbnail" ?
        #  - 'name'                                     "LomBase.title"
        #  - 'number'                                   ? (Kurs Katalognummer)
        #  - 'org'                                      "LifecycleItem" (role: 'publisher' -> organization)
        #  - 'overview'                                 "LomGeneralItem.description"
        #  - 'pacing'                                   ? ("ccm:oeh_course_coursemode"? learningMode vocab)
        #  - 'short_description'                        ? ("ccm:oeh_course_description_short"?)
        #  - 'start'                                    "ccm:license_from"?
        #  - 'start_type'                               (not saved, only used for interpretation of 'start' value)

        if "effort" in course_dict:
            # ToDo: 'effort' is describing the
            effort: str | None = course_dict["effort"]

        # Course start / end dates are in ISO 8601 notation:
        if "end" in course_dict:
            course_end_date: str | None = course_dict["end"]
        if "start" in course_dict:
            course_start_date: str | None = course_dict["start"]
        if "start_type" in course_dict:
            course_start_type: str | None = course_dict["start_type"]
            # ToDo: 'start_type' can be used to interpret 'start' date. 3 possible values:
            #  - "string": manually set by the course author
            #  - "timestamp": generated from the 'start' timestamp
            #  - "empty": no start date is specified

        # course enrollment dates are in ISO 8601 notation
        if "enrollment_end" in course_dict:
            course_enrollment_end: str | None = course_dict["enrollment_start"]
        if "enrollment_start" in course_dict:
            course_enrollment_start: str | None = course_dict["enrollment_end"]

        if "hidden" in course_dict:
            course_is_hidden: bool = course_dict["hidden"]

        if "id" in course_dict:
            course_id: str = course_dict["id"]

        if "media" in course_dict:
            media: dict = course_dict["media"]
            if "banner_image" in media:
                if "uri_absolute" in media["banner_image"]:
                    course_banner_image_absolute_uri: str | None = media["banner_image"]["uri_absolute"]
            if "course_image" in media:
                if "uri" in media["course_image"]:
                    course_image_uri_relative: str | None = media["course_image"]["uri"]
                    # ToDo: build absolute URL to course image
            if "course_video" in media:
                if "uri" in media["course_video"]:
                    course_video_uri_relative: str | None = media["course_video"]["uri"]
                    # ToDo: build absolute URL to course video
            if "image" in media:
                if "raw" in media["image"]:
                    course_media_image_raw_url: str | None = media["image"]["raw"]

        if "name" in course_dict:
            course_name: str = course_dict["name"]

        if "number" in course_dict:
            course_catalogue_number: str | None = course_dict["number"]

        if "org" in course_dict:
            course_organization: str | None = course_dict["org"]
            # e.g. "org": "Georg-August-UniversityOfGoettingen"
            # ToDo: resolve organization information with additional details from 'organization'-API-endpoint?
            #  see: https://courses.edx.org/api-docs/#/organizations/organizations_v0_organizations_read

        if "overview" in course_dict:
            course_description_overview: str | None = course_dict["overview"]

        if "pacing" in course_dict:
            # ToDo: learningMode Vocab -> "ccm:oeh_course_coursemode"?
            course_pacing: str = course_dict["pacing"]

        if "short_description" in course_dict:
            course_description_short: str | None = course_dict["short_description"]

        # ToDo: fill Item with ItemLoaders
        # ToDo: implement CourseItem in items.py
        self.logger.debug(f"Item {response.url} contained the following metadata:\n"
                          f"{pprint.pformat(course_dict)}")
        pass
