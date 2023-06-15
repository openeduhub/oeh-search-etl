#!/bin/bash
python -m venv chatgpt-api
rm -rf tmp
mkdir tmp && cd tmp
openapi-generator generate -g python -o z_api -i https://ai-prompt-service.staging.openeduhub.net/v3/api-docs --package-name z_api
cd z_api && python setup.py install --user
cd ../../
cp -r tmp/z_api/z_api/ z_api
rm -rf tmp