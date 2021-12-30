import mysql.connector, requests, json

mydb = mysql.connector.connect(
    user="m2wv",
    password="O8aq5moyisi",
    host="m2wv.mysql.pythonanywhere-services.com",
    database="m2wv$census"
)


keyfile='/home/m2wv/mysite/census_key.txt'
with open(keyfile) as key:
    api_key=key.read().strip()

data_url = f'https://api.census.gov/data/2019/acs/acs5?get=NAME,B01003_001E&for=place:*&in=state:*&key={api_key}'
response=requests.get(data_url)
popdata=response.json()

mycursor = mydb.cursor()

states = {"PR":"Puerto Rico", "DC":"District of Columbia", "AL":"Alabama","AK":"Alaska","AZ":"Arizona","AR":"Arkansas","CA":"California","CO":"Colorado","CT":"Connecticut","DE":"Delaware","FL":"Florida","GA":"Georgia","HI":"Hawaii","ID":"Idaho","IL":"Illinois","IN":"Indiana","IA":"Iowa","KS":"Kansas","KY":"Kentucky","LA":"Louisiana","ME":"Maine","MD":"Maryland","MA":"Massachusetts","MI":"Michigan","MN":"Minnesota","MS":"Mississippi","MO":"Missouri","MT":"Montana","NE":"Nebraska","NV":"Nevada","NH":"New Hampshire","NJ":"New Jersey","NM":"New Mexico","NY":"New York","NC":"North Carolina","ND":"North Dakota","OH":"Ohio","OK":"Oklahoma","OR":"Oregon","PA":"Pennsylvania","RI":"Rhode Island","SC":"South Carolina","SD":"South Dakota","TN":"Tennessee","TX":"Texas","UT":"Utah","VT":"Vermont","VA":"Virginia","WA":"Washington","WV":"West Virginia","WI":"Wisconsin","WY":"Wyoming"}
real_states = dict((v,k) for k,v in states.items())
place = ""
state = ""
place_id = ""
state_id = ""
state_code = ""
sql = "INSERT INTO geography(state, state_code, place, state_id, place_id) VALUES (%s, %s, %s, %s, %s)"
for record in popdata:
    splitrec = record[0].split(", ")
    if len(splitrec) > 1:
        if ";" not in record[0]:
            place = splitrec[0]
            state = splitrec[1]
            state_code = real_states[state]
            place_id = record[3]
            state_id = record[2]
        else:
            place = splitrec[0]
            state = splitrec[1][splitrec[1].find("; ")+2:]
            state_code = real_states[state]
            place_id = record[3]
            state_id = record[2]
        val = (state, state_code, place, state_id, place_id)
        mycursor.execute(sql, val)
        mydb.commit()
