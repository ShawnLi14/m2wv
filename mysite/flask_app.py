
#imports
from flask import Flask, redirect, render_template, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from census import getPop
from census import getACSVal

#app declaration
app = Flask(__name__)
app.config["DEBUG"] = True

#database connection
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="m2wv",
    password="O8aq5moyisi",
    hostname="m2wv.mysql.pythonanywhere-services.com",
    databasename="m2wv$census",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

from geography import Geography
from cityratings import Ratings

#urls
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        states = getStates()
        return render_template("main_page.html", **locals())
    #comment = Comment(content=request.form["contents"])
    #db.session.add(comment)
    #db.session.commit()
    #return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/results', methods=["GET","POST"])
def results():
    resultCity = request.form["city"]
    stateid = request.form["states"]
    placeid = request.form["places"]
    placeName = request.form["placeName"]
    stateName = request.form["stateName"]

    ratings = Ratings.query.all()
    destPlace = ""
    destPlaceid = ""
    destPlaceDesc = ""
    destPlaceIsAscend = False
    destPlaceUrl = ""
    recCities = [""] * 5

    rats = []
    if resultCity == "none":
        prefs = request.form.getlist('prefs')
        for row in ratings:
            sum = 0
            for pref in prefs:
                sum += getattr(row, pref)
            rats.append((row, sum))
        rats.sort(key = lambda x: x[1])
        row = rats[-1][0]
        destPlace = row.place
        destPlaceid = row.placeid
        destPlaceDesc = row.description
        destPlaceIsAscend = row.ascend
        destPlaceUrl = row.url
        recCities[0] = rats[-2][0].place
        recCities[1] = rats[-3][0].place
        recCities[2] = rats[-4][0].place
        recCities[3] = rats[-5][0].place
        recCities[4] = rats[-6][0].place
    else:
        rating = Ratings.query.filter_by(place=resultCity)
        destPlace = rating.first().place
        destPlaceid = rating.first().placeid
        destPlaceDesc = rating.first().description
        destPlaceIsAscend = rating.first().ascend
        destPlaceUrl = rating.first().url

    if destPlace == "":
        rating = Ratings.query.filter_by(place="Morgantown")
        destPlace = rating.first().place
        destPlaceid = rating.first().placeid
        destPlaceDesc = rating.first().description
        destPlaceIsAscend = rating.first().ascend
        destPlaceUrl = rating.first().url
    profile = [True, True, True, True, True, True, True, True, True, False]
    colsets = ["NAME,DP05_0001E","NAME,DP05_0037E","NAME,DP05_0038E","NAME,DP05_0044E","NAME,DP05_0039E","NAME,DP05_0058E","NAME,DP05_0018E","NAME,DP04_0134E","NAME,DP04_0089E","NAME,B25103_001E"]
    colnames = ["Population","\xa0\xa0White", "\xa0\xa0Black or African American", "\xa0\xa0Asian","\xa0\xa0Native American", "\xa0\xa0Two or More Races","Median Age","Median Rent","Median House Value","Median Property Tax Paid"]
    originalStats = [""] * len(colsets)
    destinationStats = [""] * len(colsets)
    for col in range(0,len(colsets)):
        prof = ""
        if profile[col]: prof = "profile"
        val = getACSVal(dname='acs5/' + prof,year = "2019", cols = colsets[col], state = stateid, place = placeid)
        mval = getACSVal(dname='acs5/' + prof,year = "2019", cols = colsets[col], state = "54", place = destPlaceid)
        if col > 0 and col < 6:
            originalStats[col] = str(round((float(val)/float(originalStats[0]))*100,2)) + "%";
            destinationStats[col] = str(round((float(mval)/float(destinationStats[0]))*100,2)) + "%";
        else:
            # (col > 6) and round(float(val)/float(mval)*100,1)-100 > 0:
            if col > 6 and int(val) > int(mval):
                originalStats[col] = val
                #destinationStats[col] = mval + " (You'll save " + str(round((float(val)-float(mval))/float(mval)*100,2)) + "%)"
                destinationStats[col] = mval + " (" + str(round((float(val)-float(mval))*100/float(val))) + "% savings)"
            else:
                originalStats[col] = val
                destinationStats[col] = mval
    return render_template("result.html", **locals())

def getStates():
    states = Geography.query.with_entities(Geography.state, Geography.state_id).distinct()
    return states

#ajax urls
@app.route('/getPlaces')
def getPlaces():
    statename = request.args.get("state")
    resultset = Geography.query.filter_by(state=statename)
    payload = []
    for result in resultset:
        payload.append(result.place)
        payload.append(result.place_id)
    return jsonify(payload)

@app.route('/getPopulation')
def getPopulation():
    placeid = request.args.get("placeid")
    stateid = request.args.get("stateid")
    pop = getPop(year = "2019", state = stateid, place = placeid)
    mpop = getPop(year = "2019", state = "54", place = "55756")
    return jsonify(pop)

@app.route('/getCensusData', methods=["POST"])
def getCensusData():
    #colsets = ["NAME,DP04_0134E","NAME,DP04_0089E"]
    #colnames = ["Rent","House Value"]
    #out = [""] * 2;
    #placeid = request.args.get("placeid")
    #stateid = request.args.get("stateid")
    #for col in range(0,len(colsets)):
    #    val = getACSVal(dname='acs5/profile',year = "2019", cols = colsets[col], state = stateid, place = placeid)
    #    mval = getACSVal(dname='acs5/profile',year = "2019", cols = colsets[col], state = "54", place = "55756")
    #    out[col] = colnames[col] + ": " + val + "<br>&ensp;Morgantown value: " + mval + "<br>"
    return redirect(url_for('index'))


