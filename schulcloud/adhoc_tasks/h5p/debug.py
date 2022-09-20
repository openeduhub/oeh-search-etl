import base64
import requests
import requests.auth


url = 'https://repository.dev-edusharing.staging.dbildungscloud.org/edu-sharing/rest/'
username = 'BrandenburgUserDev'
password = base64.b64decode('N2Vsb2poQnE5alpYbWl2a2J0bW4=')
session = requests.Session()
session.auth = requests.auth.HTTPBasicAuth(username, password)
session.headers = {'Accept': 'application/json'}

query_params = '&'.join([
    'contentType=FILES',
    'skipCount=0',
    'maxItems=12',
    'sortProperties=score',
    'sortAscending=false',
    'propertyFilter=-all-'
])
body = {
    'criterias': [
        {
            'property': 'ccm:ph_invited',
            'values': ["GROUP_county-12051", "GROUP_public", "GROUP_LowerSaxony-public", "GROUP_Brandenburg-public", "GROUP_Thuringia-public"]
        },
        {
            "property": "ccm:hpi_searchable",
            "values": ["1"]
        },
        {
            "property": "ngsearchword",
            "values": ["h5p"]
        }
    ],
    'facettes': ['cclom:general_keyword']
}
response = session.post(
    f'{url}search/v1/queriesV2/-home-/mds_oeh/ngsearch/?{query_params}',
    json=body
)
