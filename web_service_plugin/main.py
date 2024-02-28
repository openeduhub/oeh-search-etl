import logging

import uvicorn
import fastapi as fapi
import fastapi.middleware.cors as fapicors
import pydantic as pd
import asyncio
import subprocess
import json
from rdflib import Graph
import rdflib
import os

class Data(pd.BaseModel):
    url: str

class PingResult(pd.BaseModel):
    message: str = ""

class Result(pd.BaseModel):
    title: str = ""
    description: str = ""
    keywords: str = ""
    disciplines: str = ""
    educational_context: str = ""
    license: dict = {}
    # license_author: list = []
    new_lrt: str = ""
    kidra_disciplines: str = ""
    curriculum: str = ""
    text_difficulty: str = ""
    text_reading_time: str = ""

class ValidatedResults(pd.BaseModel):
    url: str = ""
    title: str = ""
    description: str = ""
    keywords: list = []
    disciplines: list = []
    educational_context: list = []
    license: dict = {}
    new_lrt: list = []

class SaveResults(pd.BaseModel):
    code: str = ""
    message: str = ""

def create_app() -> fapi.FastAPI:
    app = fapi.FastAPI()

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
        """
            Test
        """
        return PingResult(
            message="Pong"
        )

    @app.post("/metadata")
    async def metadata(data: Data) -> Result:
        """
        Fetch metadata

        Parameters
        ----------
        url : str
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
        bytes_result = subprocess.check_output([f'scrapy',
                                 'crawl',
                                 'generic_spider',
                                 '-a',
                                 'urltocrawl=' + data.url, '-o', '-:json'],
                                  stderr=DEVNULL)

        str_result = bytes_result.decode('utf-8')
        json_results = json.loads(str_result)
        json_result = json_results[0]

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

    @app.post("/set_metadata")
    async def set_metadata(data: ValidatedResults) -> SaveResults:
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
        bytes_result = subprocess.check_output([crawl_command], shell=True,
                                               stderr=DEVNULL)

        str_result = bytes_result.decode('utf-8')

        if str_result == '':
            return SaveResults(
                code="0",
                message="Successfully inserted in Edu-sharing"
            )
        else:
            return SaveResults(
                code="1",
                message="Error inserting data in Edu-sharing"
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
