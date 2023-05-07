from flask import Flask, render_template, request, flash, redirect, url_for, jsonify,json
from entity import getmovies, moviedetails, searchbar, getshowdate, getshowtime, getsessionid, getReview, getAvgRating, displaySeat, getFoodDrinksCombo, getFoodDrinksACarte


app = Flask(__name__)
app.secret_key = 'my_secret_key'

@app.route("/")
def main():
    data = getmovies()
    return render_template("home.html", data=data)

@app.route("/movdetails/<int:movieID>")
def movd(movieID):
    dates = getshowdate(movieID)
    movieD = moviedetails(movieID)
    Review = getReview(movieID)
    AvgRating = getAvgRating(movieID)
    if AvgRating is not None:
        Rate = round(AvgRating, 1)
    else:
        Rate = None
   
    if not movieD:
        abort(404)
    return render_template("movdetails.html", data = movieD, T = dates, Review = Review, Rating = Rate )

@app.route("/search", methods=['POST'])
def search():
    search_query = request.form['search_query']
    data = searchbar(search_query)
    if len(data) == 0:
        message = "No results found for your search query."
    else:
        message = ""
    return render_template("home.html", data=data, message = message)


@app.route("/moviedetails/timing/<int:movieID>", methods=['POST'])
def returntiming(movieID):
    date = request.form['selected_date']
    timings = getshowtime(movieID, date)
    movieD = moviedetails(movieID)
    return render_template("timing.html", date=date, timing = timings, data = movieD)

@app.route("/seat/<int:movieID>", methods=['POST'])
def sessioncontroller(movieID):
    date = request.args.get('date')
    selected_time = request.form['selected_time']
    sessionID = getsessionid(movieID, date, selected_time)
    print(date)
    print(selected_time)
    print("Session ID : ")
    print(sessionID[0].sessionID)
    seatDetails = displaySeat(sessionID[0].sessionID)
    print(seatDetails)
    return render_template("seat.html", seatDetails = seatDetails)



@app.route('/processJsonFoodDrinks', methods=['POST'])
def processJsonFoodDrinks():
    global jsonData
    if(request.method == 'POST'):
        data = request.json
        print(data)
        jsonData = data
        return jsonify(data)


@app.route('/getJsonData', methods=['GET'])
def getJsonData():
    global jsonData  # Access the global variable
    if jsonData is not None:
        return jsonify(jsonData)
    else:
        return 'No JSON data available'




@app.route('/foodDrinks')
def foodDrinks():
    combo = getFoodDrinksCombo()
    aCarte = getFoodDrinksACarte()
    return render_template('foodDrinks.html', combo = combo, aCarte = aCarte)




if __name__ == "__main__":
    app.run(debug=True)