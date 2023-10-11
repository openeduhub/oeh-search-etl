import uvicorn
import fastapi as fapi
import fastapi.middleware.cors as fapicors
import pydantic as pd
import asyncio
import subprocess


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

        result = subprocess.run([f'scrapy', 'crawl', 'generic_spider', '-o', '-:json'],
                        cwd='../', capture_output=True)

        result.stdout

        return Result(
            resultjson="json_results",
        )

    return app

async def start_ws_service():
    config = uvicorn.Config("web_service_plugin.main:create_app", port=5500, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(start_ws_service())
