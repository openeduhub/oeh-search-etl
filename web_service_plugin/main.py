import uvicorn
import fastapi as fapi
import fastapi.middleware.cors as fapicors
import pydantic as pd
import asyncio
import subprocess
import json


class Data(pd.BaseModel):
    url: str


class Result(pd.BaseModel):
    title: str = ""
    description: str = ""
    keywords: list = []
    disciplines: list = []
    educational_context: list = []
    license: list = []
    license_author: list = []
    new_lrt: list = []


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

        result = subprocess.run([f'scrapy',
                                 'crawl',
                                 'generic_spider',
                                 '-a',
                                 'urltocrawl=' + data.url, '-o', '-:json'],
                                cwd='../', capture_output=True)

        bytes_result = result.stdout
        str_result = bytes_result.decode('utf-8')
        json_results = json.loads(str_result)
        json_result = json_results[0]

        dict_license = json_result['license']
        license_author = []
        license = []
        if 'author' in dict_license.keys():
            license_author = dict_license['author']
        else:
            license = [k + " : " + v for (k, v) in dict_license.items()]

        title = json_result['lom']['general']['title']
        description = json_result['lom']['general']['description']
        keywords = json_result['lom']['general']['keyword']

        valuespaces = json_result['valuespaces']
        educational_context = valuespaces['educationalContext'] if 'educationalContext' in valuespaces.keys() else []
        disciplines = valuespaces['discipline'] if 'discipline' in valuespaces.keys() else []
        new_lrt = valuespaces['new_lrt'] if 'new_lrt' in valuespaces.keys() else []

        return Result(
            title=title,
            description=description,
            keywords=keywords,
            disciplines=disciplines,
            educationalContext=educational_context,
            license=license,
            license_author=license_author,
            new_lrt=new_lrt
        )

    return app


async def start_ws_service():
    config = uvicorn.Config("web_service_plugin.main:create_app", port=5500, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    print("MAIN---------------------------------------------------------------")
    # asyncio.run(start_ws_service())
