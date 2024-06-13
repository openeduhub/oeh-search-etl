# Open Edu Hub Search ETL

- make sure you have python3 installed (<https://docs.python-guide.org/starting/installation/>)
- (Python 3.9.1 or newer is required)
- Instal docker (https://docs.docker.com/engine/install/). This project uses Docker to start up the containers for `headless chrome`, `Splash` and `Pyppeteer`-integration.
- Preferable to use in Unix-based systems but a new documentation will be uploaded for Windows systems. For example:
```bash
source .venv/bin/activate   # (on Linux Unix)
.venv\Scripts\activate.bat  # (on Windows)
```
- A crawler can be run with `scrapy crawl <spider-name>`. It assumes that you have an edu-sharing 6.0 instance in your `.env` settings configured which can accept the data.
- If a crawler has [Scrapy Spider Contracts](https://docs.scrapy.org/en/latest/topics/contracts.html#spiders-contracts) implemented, you can test those by running `scrapy check <spider-name>`


## Building a Crawler

- We use Scrapy as a framework. Please check out the guides for Scrapy spider (https://docs.scrapy.org/en/latest/intro/tutorial.html)
- To create a new spider, create a file inside `converter/spiders/<myname>_spider.py`
- We recommend inheriting the `LomBase` class in order to get out-of-the-box support for our metadata model
- You may also Inherit a Base Class for crawling data, if your site provides LRMI metadata, the `LrmiBase` is a good start. If your system provides an OAI interface, you may use the `OAIBase`
- As a sample/template, please take a look at the `sample_spider.py`
- To learn more about the LOM standard we're using, you'll find useful information at https://en.wikipedia.org/wiki/Learning_object_metadata

## Run the web service for the Generic crawler via Docker

A web service that implements the FastAPI web framework is added to the project.

The Dockerfile will perform the following tasks:
- Copy the source folders, Scrapy configuration files and the requirements.txt file for the python dependencies
- Install the python dependencies
- Install the Java JDK version 17 
- Generate the Z-API python library
- Copy the web service source folder and install its requirements.txt file which installs FastAPI and Uvicorn
- Set the entrypoint script file: entrypoint.sh this file is the script which runs the crawler in any of its modes:
    - Crawl all the URLs that are listed in the generic_spider.py file with or without parameters (arguments that the crawler could need by setting the ARGS variable). To run the crawler in this mode you should delete the API_MODE variable (unset API_MODE)
    - Start the webservice by setting the API_MODE variable (=true or false)


Then run the following lines in a terminal:

```bash
git clone https://github.com/openeduhub/oeh-search-etl
cd oeh-search-etl
git checkout add_web_service_package
cd oeh-search-etl
git checkout add_KIdra_services
# edit the environment variables (with vi for example) in converter/.env.example then make sure that this values are set correctly:
# MODE = "json"
# Z_API_KEY=<your_z_api_key>
# If you need to save the metadata into the edu-sharing repository, then set the following variables:
# EDU_SHARING_BASE_URL = "https://repository.pre-staging.openeduhub.net/edu-sharing/"
# EDU_SHARING_USERNAME = "<your_username>"
# EDU_SHARING_PASSWORD = "<your_password>"
cp converter/.env.example converter/.env
docker compose build --no-cache scrapy
export API_MODE=true
export EDU_SHARING_BASE_URL=https://repository.pre-staging.openeduhub.net/edu-sharing/
export EDU_SHARING_USERNAME=<your_username>
export EDU_SHARING_PASSWORD=<your_password>
export Z_API_KEY=<your_z_api_key>
docker compose up

```
And each time the web service is required you have to run the three `export` command lines and the `docker compose up` line. Now you should have access to the FastAPI environment in http://0.0.0.0:80/docs# because this ip address (http://0.0.0.0) and port (80) is exposed to outside the container, then the same port in the container can be accessed by the host.

### Use the web extension

When you deploy the web service for the generic crawler you can test it by opening the Web extension (https://github.com/openeduhub/metadata-browser-plugin/tree/add_metadata_form and clone the `add_metadata_form` branch ) and press the first button `Meine Empfehlungen` (`My recommendations`) to get the metadata from the web service. You can edit the metadata values that the crawler generates and send them to the pre-staging edu-sharing repository by pressing `Weiter` button.


### Debugging the generic crawler or web service locally

The instructions below (using Docker) should have been run also for this section because the containers for the headless browser (`image: browserless/chrome`) and the splash server (`image: scrapinghub/splash:master`) should be running.

In order to get authenticate to the Z_API web services (such as AI-prompts) it is mandatory to set the "Z_API_KEY" variable in the .env.example right before running the line `cp converter/.env.example converter/.env`:
```bash
Z_API_KEY = "<your_z_api_key>"
```

You have two options here:
- To persist the metadata in the pre-staging edu-sharing repository you should provide this values in the .env.example right before running the line `cp converter/.env.example converter/.env`:
```bash
MODE = "edu-sharing"
EDU_SHARING_BASE_URL = "https://repository.pre-staging.openeduhub.net/edu-sharing/"
EDU_SHARING_USERNAME = "<your_username>"
EDU_SHARING_PASSWORD = "<your_password>"
Z_API_KEY = "<your_z_api_key>"
```
- Or if you want to make tests locally and save the results of the page tree in a file, then change to:
```bash
MODE = "json"
```

Then open a new terminal in the same folder (oeh-search-etl) and run the following lines to install the generic crawler and components locally:
```bash
sudo apt install python3-dev python3-pip python3-venv libpq-dev -y
sudo apt install wget python3-lxml libxml2-dev libxslt-dev openjdk-17-jre-headless npm -y
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
sudo ./generate-z-api.sh
source .venv/bin/activate
pip3 install -r web_service_plugin/requirements.txt
export PYTHONPATH=$PYTHONPATH:`pwd`
export PYTHONPATH="${PYTHONPATH}/z_api"
# Modify the variables (MODE, Z_API_KEY, API_MODE, EDU_SHARING_BASE_URL, EDU_SHARING_USERNAME, EDU_SHARING_PASSWORD) in converter/.env.example as is shown above
cp converter/.env.example converter/.env
```

Then run this line to crawl a page tree and save the results in a json file:

```bash
.venv/bin/python -m scrapy.cmdline crawl generic_spider -a urltocrawl=<your_url> -a ai_enabled=False -a find_sitemap=True -O <output_file>
```

For example to crawl a page tree for the Biology website: https://biologie-lernprogramme.de/ without AI generated metadata and with the tool to find the sitemap:

```bash
.venv/bin/python -m scrapy.cmdline crawl generic_spider -a urltocrawl=https://biologie-lernprogramme.de/ -a ai_enabled=False -a find_sitemap=True -O ../../Page_tree_logs/biologie_lernprogramme/generic_spider.json
```


### To start the web service locally:

In the same folder (oeh-search-etl), run:
```bash
python3 web_service_plugin/main.py
```

By running the last line `python3 web_service_plugin/main.py` you should have access to the FastAPI environment in the localhost by http://127.0.0.1:5500/docs#. Note that this "local" IP address and port is different that if you use Docker compose (http://0.0.0.0:80/docs#).

Each request to the generic crawler takes a long time to fetch the crawled metadata, and in any case, the terminals get updated status of the web services that are runnung.

If the web service fails consider to stop and restart the services by pressing `Ctrl+C` in each terminal:
- The first terminal with the Headless-chrome and Splash instances. Then press `Ctrl+C` and restart the instances: `docker compose up`
- And the second terminal with the web service supported by FastAPI. Then press `Ctrl+C` and restart the web service: `python3 web_service_plugin/main.py`


## Still have questions? Check out our GitHub-Wiki!
If you need help getting started or setting up your work environment, please don't hesitate to visit our GitHub Wiki at https://github.com/openeduhub/oeh-search-etl/wiki
