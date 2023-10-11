"""
Debugging entry point for VSCode.

Add the following to the `configurations` array in `.vscode/launch.json`:

    {
        "name": "Run scrapy",
        "type": "python",
        "request": "launch",
        "program": "${workspaceFolder}/converter/run.py",
        "console": "integratedTerminal"
    }
"""


import os
from scrapy.cmdline import execute

import asyncio
import uvicorn
import fastapi as fapi
import fastapi.middleware.cors as fapicors
import pydantic as pd
import scrapy.crawler as cw
import scrapy.utils.project as sproj
from converter.spiders.generic_spider import GenericSpider
from scrapy import signals
from scrapy.signalmanager import dispatcher
import json



def run():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    execute(
        [
            "scrapy",
            "crawl",
            "-a",
            "cleanrun=true",
            "-o",
            "out/items.json",
            "wirlernenonline_spider",
        ]
    )


class Data(pd.BaseModel):
    url: str

class Result(pd.BaseModel):
    resultjson: str = ""


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
    def _ping():
        pass


    @app.post("/metadata")
    async def metadata(data: Data) -> Result:
        print("TARGET_URL", data.url)
        project_settings = sproj.get_project_settings()
        results = []
        def crawler_results(signal, sender, item, response, spider):
            # results.append(item)
            # dict_result = dict(results[0])
            # json_results = json.dumps(str(dict_result), indent=4)
            return Result(
                resultjson="json_results",
            )

        dispatcher.connect(crawler_results, signal=signals.item_scraped)

        c = cw.CrawlerProcess(project_settings)
        GenericSpider.start_urls = ['https://de.wikipedia.org/wiki/G%C3%B6ttingen']
        c.crawl(GenericSpider)
        # list_ports = os.system("lsof -i :5500")
        # if list_ports != 0:
        c.start()

    return app

async def start_ws_service():
    config = uvicorn.Config("run:create_app", port=5500, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    # run()
    list_ports = os.system("lsof -i :5500")
    if list_ports != 0:
        asyncio.run(start_ws_service())
