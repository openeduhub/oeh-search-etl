#!/bin/bash
# Creating a venv within the "venv_z_api"-directory (for easier distinction from our "normal" venv)
python3 -m venv venv_z_api
# activating the venv:
source ./venv_z_api/bin/activate
# confirm that you are within your venv, then install the requirements.txt:
pip3 install -r requirements.txt

# deleting the "tmp"-directory (if there was one from a previous execution of this script)
rm -rf tmp
# create a temporary "tmp"-directory which will be used by the OpenAPI Generator (API Client)
mkdir tmp
# switch to directory (or: exit here if changing directories fails)
cd tmp || exit
#
# make sure that you have the OpenAPI Generator installed (and the PATH exposed within your ".profile")
# before running this command, otherwise the following steps WILL NOT WORK:
echo "Java version ---------------------- : " $(java -version)
# openapi-generator generate -g python-experimental -o z_api --skip-validate-spec -i https://ai-prompt-service.staging.openeduhub.net/v3/api-docs --package-name z_api
java -jar openapi-generator-cli.jar generate -g python-experimental -o z_api --skip-validate-spec -i https://ai-prompt-service.staging.openeduhub.net/v3/api-docs --package-name z_api
cd z_api
python3 setup.py install --user
# change directories to project root:
cd ../../
# move the only relevant sub-directory to the "z_api"-directory at project root:
cp -r tmp/z_api/z_api/ z_api
# delete the temporary folder after everything is done:
rm -rf tmp