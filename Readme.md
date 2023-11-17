# Open Edu Hub Search ETL

- make sure you have python3 installed (<https://docs.python-guide.org/starting/installation/>)
- (Python 3.9.1 or newer is required)
- go to project root
- Run
```
sudo apt install python3-dev python3-pip python3-venv libpq-dev -y
python3 -m venv .venv
```

`source .venv/bin/activate` (on Linux Unix)

`.venv\Scripts\activate.bat` (on Windows)

`pip3 install -r requirements.txt`

If you have Docker installed, use `docker-compose up` to start up the multi-container for `Splash` and `Pyppeteer`-integration. 

As a last step, set up your config variables by copying the `.env.example`-file and modifying it if necessary: 

`cp converter/.env.example converter/.env`

- A crawler can be run with `scrapy crawl <spider-name>`. It assumes that you have an edu-sharing 6.0 instance in your `.env` settings configured which can accept the data.
- If a crawler has [Scrapy Spider Contracts](https://docs.scrapy.org/en/latest/topics/contracts.html#spiders-contracts) implemented, you can test those by running `scrapy check <spider-name>`


## Run via Docker
```bash
git clone https://github.com/openeduhub/oeh-search-etl
cd oeh-search-etl
cp .env.example .env
# modify .env with your edu sharing instance
docker compose build scrapy
export CRAWLER=your_crawler_id_spider # i.e. wirlernenonline_spider
docker compose up
```

## Building a Crawler

- We use Scrapy as a framework. Please check out the guides for Scrapy spider (https://docs.scrapy.org/en/latest/intro/tutorial.html)
- To create a new spider, create a file inside `converter/spiders/<myname>_spider.py`
- We recommend inheriting the `LomBase` class in order to get out-of-the-box support for our metadata model
- You may also Inherit a Base Class for crawling data, if your site provides LRMI metadata, the `LrmiBase` is a good start. If your system provides an OAI interface, you may use the `OAIBase`
- As a sample/template, please take a look at the `sample_spider.py`
- To learn more about the LOM standard we're using, you'll find useful information at https://en.wikipedia.org/wiki/Learning_object_metadata

## Run the web service for the generic crawler via Docker

A web service that implements the FastAPI web framework is added to the project. In order to start the web service it is enough to set API_MODE variable in any of this options:
- export API_MODE=0 (to start the webservice into the Docker container). This still needs to be tested.
- export API_MODE=1 (to start the webservice locally in your machine)

The web service is started at localhost (127.0.0.1) at the 5500 port.

The Dockerfile will perform the following tasks:
- Copy the source folders, Scrapy configuration files and the requirements.txt file for the python dependencies
- Install the python dependencies
- Install the Java JDK version 11 
- Generate the Z-API python library
- Copy the web service source folder and install its requirements.txt file which installs FastAPI and Uvicorn
- Set the entrypoint script file: entrypoint.sh this file is the script which runs the crawler in any of its modes:
    - Crawl all the URLs that are listed in the generic_spider.py file with or without parameters (arguments that the crawler could need by setting the ARGS variable). To run the crawler in this mode you should delete the API_MODE variable (unset API_MODE)
    - Start the webservice by setting the API_MODE variable (=0 or 1 as was stated above)

To persist the metadata in the pre-staging edu-sharing repository you should provide this values in the .env.example file beforehand:
- MODE = "edu-sharing"
- EDU_SHARING_BASE_URL = "https://repository.pre-staging.openeduhub.net/edu-sharing/"
- EDU_SHARING_USERNAME = "<your_username>"
- EDU_SHARING_PASSWORD = "<your_password>"
- Z_API_KEY="<the_Z_API_key>"

Then run the following lines in a terminal:

```bash
git clone https://github.com/openeduhub/oeh-search-etl
cd oeh-search-etl
git checkout add_web_service_package
gedit converter/.env.example     # edit the variables as stated above in instructions, save it and close it
cp converter/.env.example converter/.env
docker compose build scrapy
export API_MODE=1
docker compose up
```
Then open a new terminal in the same folder (oeh-search-etl) and run the following line in order to start the web service locally:
```bash
sudo apt install python3-dev python3-pip python3-venv libpq-dev -y
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
sudo apt-get update && \
    apt-get install -y openjdk-11-jre-headless && \
    apt-get clean;
sudo ./generate-z-api.sh
source .venv/bin/activate
pip3 install -r web_service_plugin/requirements.txt
export PYTHONPATH=$PYTHONPATH:`pwd`
export PYTHONPATH="${PYTHONPATH}/z_api"
python3 web_service_plugin/main.py
```

Now you should have access to the FastAPI environment in http://127.0.0.1:5500/docs#

{"themesUrl":"https://repository.pre-staging.openeduhub.net/edu-sharing/themes/default/","lastCacheUpdate":1700193600023,"version":{"repository":"9999.99999999","renderservice":"9999.99999999.9999","major":1,"minor":1},"services":[{"name":"ADMIN","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/admin/v1"}]},{"name":"BULK","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":1},"endpoint":"/bulk/v1"}]},{"name":"COLLECTION","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/collection/v1"}]},{"name":"COMMENT","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/comment/v1"}]},{"name":"RATING","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/rating/v1"}]},{"name":"CONFIG","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/config/v1"}]},{"name":"IAM","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/iam/v1"}]},{"name":"AUTHENTICATION","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/authentication/v1"}]},{"name":"MDS","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/mds/v1"}]},{"name":"MEDIACENTER","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/mediacenter/v1"}]},{"name":"NETWORK","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/network/v1"}]},{"name":"NODE","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/node/v1"}]},{"name":"ORGANIZATION","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/organization/v1"}]},{"name":"SEARCH","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/search/v1"}]},{"name":"USAGE","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/usage/v1"}]},{"name":"RENDERING","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/rendering/v1"}]},{"name":"STATISTIC","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/statistic/v1"}]},{"name":"TRACKING","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/tracking/v1"}]},{"name":"ARCHIVE","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/archive/v1"}]},{"name":"CLIENTUTILS","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/clientUtils/v1"}]},{"name":"TOOL","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/tool/v1"}]},{"name":"REGISTER","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/register/v1"}]},{"name":"SHARING","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/sharing/v1"}]}]}
{"themesUrl":"https://repository.pre-staging.openeduhub.net/edu-sharing/themes/default/","lastCacheUpdate":1700193600023,"version":{"repository":"9999.99999999","renderservice":"9999.99999999.9999","major":1,"minor":1},"services":[{"name":"ADMIN","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/admin/v1"}]},{"name":"BULK","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":1},"endpoint":"/bulk/v1"}]},{"name":"COLLECTION","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/collection/v1"}]},{"name":"COMMENT","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/comment/v1"}]},{"name":"RATING","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/rating/v1"}]},{"name":"CONFIG","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/config/v1"}]},{"name":"IAM","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/iam/v1"}]},{"name":"AUTHENTICATION","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/authentication/v1"}]},{"name":"MDS","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/mds/v1"}]},{"name":"MEDIACENTER","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/mediacenter/v1"}]},{"name":"NETWORK","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/network/v1"}]},{"name":"NODE","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/node/v1"}]},{"name":"ORGANIZATION","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/organization/v1"}]},{"name":"SEARCH","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/search/v1"}]},{"name":"USAGE","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/usage/v1"}]},{"name":"RENDERING","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/rendering/v1"}]},{"name":"STATISTIC","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/statistic/v1"}]},{"name":"TRACKING","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/tracking/v1"}]},{"name":"ARCHIVE","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/archive/v1"}]},{"name":"CLIENTUTILS","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/clientUtils/v1"}]},{"name":"TOOL","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/tool/v1"}]},{"name":"REGISTER","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/register/v1"}]},{"name":"SHARING","instances":[{"version":{"repository":null,"renderservice":null,"major":1,"minor":0},"endpoint":"/sharing/v1"}]}]}


## Still have questions? Check out our GitHub-Wiki!
If you need help getting started or setting up your work environment, please don't hesitate to visit our GitHub Wiki at https://github.com/openeduhub/oeh-search-etl/wiki
