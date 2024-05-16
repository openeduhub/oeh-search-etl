import json
import logging
import os
import subprocess

import fastapi as fapi
import fastapi.middleware.cors as fapicors
from fastapi.responses import JSONResponse
from fastapi import status
import pydantic as pd
import rdflib
import uvicorn
from rdflib import Graph
from starlette.responses import JSONResponse

import converter.env as env
import sys
import traceback
from ..converter.util.sitemap import find_generate_sitemap

# verify presence of the key!
env.get("Z_API_KEY", allow_null=False)

class Data(pd.BaseModel):
    url: str = ""
    ai_enabled: bool = True

class PingResult(pd.BaseModel):
    message: str = ""

class Result(pd.BaseModel):
    title: str = ""
    description: str = ""
    keywords: str = ""
    disciplines: str = ""
    educational_context: str = ""
    intendedenduserrole: str = ""
    license: dict = {}
    new_lrt: str = ""
    kidra_disciplines: str = ""
    curriculum: str = ""
    text_difficulty: str = ""
    text_reading_time: float = 0.0

class ValidatedResults(pd.BaseModel):
    url: str = ""
    title: str = ""
    description: str = ""
    curriculum: list = []
    intendedenduserrole: list = []
    keywords: list = []
    disciplines: list = []
    educational_context: list = []
    license: dict = {}
    new_lrt: list = []

class StandardResult(pd.BaseModel):
    code: str = ""
    message: str = ""

class SitemapResult(pd.BaseModel):
    urls:list = []

def create_app() -> fapi.FastAPI:
    description = f"""
                    The web services deployed here exposes the main functions of the generic crawler and are intended to be used by the web extension **https://github.com/openeduhub/metadata-browser-plugin/tree/add_metadata_form**
                    """
    tags_metadata = [
        {
            "name": "Ping",
            "description": "Test service",
        },
        {
            "name": "Get metadata",
            "description": "Get metadata",
        },
        {
            "name": "Save metadata",
            "description": "Save metadata in the repository specified when in Docker compose.",
            "externalDocs": {
                "description": "Github docs",
                "url": "https://github.com/openeduhub/oeh-search-etl/tree/add_KIdra_services",
            },
        },
    ]
    app = fapi.FastAPI(
        title = "Generic crawler",
        summary = "Web services for the generic crawler",
        description = description,
        openapi_tags=tags_metadata
    )

    origins = ['*']

    app.add_middleware(
        fapicors.CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/_ping")
    def _ping() -> PingResult:
        return PingResult(
            message="Pong"
        )

    @app.post("/metadata")
    async def metadata(data: Data):
        """
        Fetch metadata

        Parameters
        ----------
        data.url: str
            The url to be crawled.

        Returns
        -------
        title : str
        description : str
        keywords : str
        disciplines : str
        educational_context : str
        license : str
        new_lrt : str
        kidra_disciplines : str
        curriculum : str
        text_difficulty : str
        text_reading_time : str
        """

        DEVNULL = open(os.devnull, 'wb')
        try:
            bytes_result = subprocess.check_output([f'scrapy',
                                                    'crawl',
                                                    'generic_spider',
                                                    '-a', 'urltocrawl=' + data.url,
                                                    '-a', 'ai_enabled=' + str(data.ai_enabled),
                                                    '-o', '-:json'],
                                                   stderr=DEVNULL)
        except (subprocess.CalledProcessError, Exception) as e:
            error_traceback = error_logger()
            error_str = 'Call of native spider failed in metadata web service: '+error_traceback
            logging.error(error_str)
            # logging.error(e.output.decode('utf-8'))
            return JSONResponse(
                status_code=500,
                content={
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": error_str
                }
            )

        str_result = bytes_result.decode('utf-8')
        try:
            json_results = json.loads(str_result)
            # Todo: parse not just the first json result but parse All the results for the page tree crawling
            json_result = json_results[0]
            if data.ai_enabled:
                license = json_result['license']
                title = json_result['lom']['general']['title']
                description = json_result['lom']['general']['description']
                keywords = json_result['lom']['general']['keyword']
                valuespaces = json_result['valuespaces']
                educational_context = valuespaces['educationalContext'] if 'educationalContext' in valuespaces.keys() else []
                disciplines = valuespaces['discipline'] if 'discipline' in valuespaces.keys() else []
                new_lrt = valuespaces['new_lrt'] if 'new_lrt' in valuespaces.keys() else []
                kidra_raw = json_result['kidra_raw']
                curriculum = kidra_raw["curriculum"]
                text_difficulty = kidra_raw["text_difficulty"]
                text_reading_time = kidra_raw["text_reading_time"]
                kidraDisciplines = []
                if 'kidraDisciplines' in kidra_raw:
                    kidraDisciplines = kidra_raw["kidraDisciplines"]

                keywords = join(keywords)
                disciplines = join(disciplines)
                educational_context = join(educational_context)
                new_lrt = join(new_lrt)
                curriculum = join(curriculum)
                kidraDisciplines = join(kidraDisciplines)

                return Result(
                    title=title,
                    description=description,
                    keywords=keywords,
                    disciplines=disciplines,
                    educational_context=educational_context,
                    license=license,
                    new_lrt=new_lrt,
                    kidra_disciplines=kidraDisciplines,
                    curriculum=curriculum,
                    text_difficulty=text_difficulty,
                    text_reading_time=text_reading_time
                )
            else:
                license = json_result['license']
                title = json_result['lom']['general']['title']
                description = json_result['lom']['general']['description']
                keywords = json_result['lom']['general']['keyword'] if 'keyword' in json_result['lom']['general'].keys() else []
                valuespaces = json_result['valuespaces']
                educational_context = valuespaces['educationalContext'] if 'educationalContext' in valuespaces.keys() else []
                disciplines = valuespaces['discipline'] if 'discipline' in valuespaces.keys() else []
                new_lrt = valuespaces['new_lrt'] if 'new_lrt' in valuespaces.keys() else []

                keywords = join(keywords)
                disciplines = join(disciplines)
                educational_context = join(educational_context)
                new_lrt = join(new_lrt)

                return Result(
                    title=title,
                    description=description,
                    keywords=keywords,
                    disciplines=disciplines,
                    educational_context=educational_context,
                    license=license,
                    new_lrt=new_lrt
                )
        except Exception as e:
            error_traceback = error_logger()
            error_str = 'Native spider returned invalid json' + error_traceback
            logging.error(error_str)
            # logging.error(e.output.decode('utf-8'))
            return JSONResponse(
                status_code=500,
                content={
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": error_str
                }
            )


    @app.post("/set_metadata")
    async def set_metadata(data: ValidatedResults):
        """
        Insert metadata into edu-sharing repository

        Parameters
        ----------
        url : str
        title : str
        description : str
        keywords : list
        disciplines : list
        educational_context : list
        license : dict
        new_lrt : list

        Returns
        -------
        code : str
        message : str
        """
        data_str = json.dumps(dict(data))
        crawl_command = f"scrapy crawl generic_spider -a validated_result='{data_str}'"
        DEVNULL = open(os.devnull, 'wb')
        try:
            bytes_result = subprocess.check_output([crawl_command], shell=True,
                                               stderr=DEVNULL)

        except Exception as e:
            error_traceback = error_logger()
            error_str = 'Call of native spider failed in set_metadata web service: ' + error_traceback
            logging.error(error_str)
            return JSONResponse(
                status_code=500,
                content={
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": error_str
                }
            )

        str_result = bytes_result.decode('utf-8')

        if str_result == '':
            return StandardResult(
                code="0",
                message="Successfully inserted in Edu-sharing"
            )
        else:
            logging.error("Error inserting data in Edu-sharing")
            return JSONResponse(
                status_code=500,
                content={
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": "Error inserting data in Edu-sharing"
                }
            )

    @app.post("/get_sitemap")
    async def get_sitemap(data: Data):
        """
        Find or generate the sitemap

        Parameters
        ----------
        url : str

        Returns
        -------
        urls : list
        """

        found_urls = find_generate_sitemap(data.url, 6)

        return SitemapResult(
            urls = found_urls
        )

    return app

def start_ws_service():
    config = uvicorn.Config("web_service_plugin.main:create_app", port=5500, log_level="info")
    server = uvicorn.Server(config)
    server.run()


def mapping_disciplines(discipline_urls):
    graph = Graph()
    graph.parse('./vocabs/discipline.ttl', format='ttl')
    list_graph = list(graph)
    disciplines = []
    for element in list_graph:
        for discipline_url in discipline_urls:
            if element[0].lower() == discipline_url:
                literal = element[2]
                if type( literal ) == rdflib.term.Literal:
                    if literal.language == 'de':
                        disciplines.append(literal.value)
    return disciplines


def mapping_eduContext(discipline_urls):
    graph = Graph()
    graph.parse('./vocabs/educationalContext.ttl', format='ttl')
    list_graph = list(graph)
    disciplines = []
    for element in list_graph:
        for discipline_url in discipline_urls:
            ref = element[0]
            if ref.lower() == discipline_url.lower():
                literal = element[2]
                if type( literal ) == rdflib.term.Literal:
                    if literal.language == 'de':
                        disciplines.append(literal.value)
    return disciplines

def mapping_lrt(urls):
    graph = Graph()
    graph.parse('./vocabs/new_lrt.ttl', format='ttl')
    list_graph = list(graph)
    disciplines = []
    for element in list_graph:
        for discipline_url in urls:
            ref = element[0]
            if ref.lower() == discipline_url.lower():
                literal = element[2]
                if type( literal ) == rdflib.term.Literal:
                    if literal.language == 'de':
                        disciplines.append(literal.value)
    return disciplines

def join(array):
    joined_str = ""
    if len(array) > 0:
        joined_str = array[0]
        for i in array[1:]:
            joined_str = joined_str+", "+i
    return joined_str


if __name__ == "__main__":
    start_ws_service()

def error_logger() -> str:
    _, value_, traceback_ = sys.exc_info()
    traceback_list = traceback.extract_tb(traceback_)
    traceback_list = ''.join(str(t) for t in traceback_list)
    return str(value_)+'. '+traceback_list
