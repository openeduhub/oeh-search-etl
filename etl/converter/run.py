"""
Debugging entry point for VSCode.

Add the following to the `configurations` array in `.vscode/launch.json`:

    {
        "name": "Run scrapy",
        "type": "python",
        "request": "launch",
        "program": "${workspaceFolder}/etl/converter/run.py",
        "console": "integratedTerminal"
    }
"""


import os
from scrapy.cmdline import execute


def run():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    execute(
        [
            "scrapy",
            "crawl",
            "-a",
            "cleanrun=true",
            '-o',
            'out/items.json',
            "wirlernenonline_spider",
        ]
    )


if __name__ == "__main__":
    run()
