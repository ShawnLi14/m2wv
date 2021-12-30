import requests, json

def getPop(year="2019",state="54",place=""):
    dsource='acs'
    dname='acs5'
    cols='NAME,B01003_001E'
    keyfile='/home/m2wv/mysite/census_key.txt'

    base_url = f'https://api.census.gov/data/{year}/{dsource}/{dname}'

    with open(keyfile) as key:
        api_key=key.read().strip()

    data_url = f'{base_url}?get={cols}&for=place:{place}&in=state:{state}&key={api_key}'
    response=requests.get(data_url)
    popdata=response.json()

    return popdata[len(popdata)-1][1]

def getACSVal(dname='acs5',year="2019",cols='NAME,B01003_001E',state="54",place=""):
    dsource='acs'
    keyfile='/home/m2wv/mysite/census_key.txt'

    base_url = f'https://api.census.gov/data/{year}/{dsource}/{dname}'

    with open(keyfile) as key:
        api_key=key.read().strip()

    data_url = f'{base_url}?get={cols}&for=place:{place}&in=state:{state}&key={api_key}'
    print(data_url)
    response=requests.get(data_url)
    data=response.json()

    return data[len(data)-1][1]
