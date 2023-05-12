from flask import Flask, render_template, request, flash, redirect, url_for, jsonify,json
from entity import displaySeat, getFoodDrinksCombo, getFoodDrinksACarte, getReview, getAvgRating, setRatingReview
from entity import Session, MovieEntity

app = Flask(__name__)
app.secret_key = 'my_secret_key'

@app.route("/")
def main():
    data = MovieEntity.getmovies()
    return render_template("home.html", data=data)

@app.route("/movdetails/<int:movieID>")
def movd(movieID):
    dates = Session.getshowdate(movieID)
    movieD = MovieEntity.moviedetails(movieID)
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
    data = MovieEntity.searchbar(search_query)
    if len(data) == 0:
        message = "No results found for your search query."
    else:
        message = ""
    return render_template("home.html", data=data, message = message)


@app.route("/moviedetails/timing/<int:movieID>", methods=['POST'])
def returntiming(movieID):
    date = request.form['selected_date']
    timings = Session.getshowtime(movieID, date)
    movieD = MovieEntity.moviedetails(movieID)
    return render_template("timing.html", date=date, timing = timings, data = movieD)

@app.route("/seat/<int:movieID>", methods=['POST'])
def sessioncontroller(movieID):
    date = request.args.get('date')
    selected_time = request.form['selected_time']
    sessionID = Session.getsessionid(movieID, date, selected_time)
    print(sessionID[0].sessionID)
    seatDetails = Session.display_seat(sessionID[0].sessionID)
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
    
@app.route("/RatingReview/<int:movieID>", methods=['GET', 'POST'])
def RatingReview(movieID):
    movieD = MovieEntity.moviedetails(movieID)
    userID = 9999

    if request.method == 'POST':
        Rating = request.form.get("rate")
        Review = request.form.get("review")
        if Rating is not None and Review is not None:
            setRatingReview(movieID=movieID, Rating=int(Rating), Review=Review, userID=userID)
            flash("Submitted Successfully!")
 
    return render_template('RatingReview.html', data=movieD)


if __name__ == "__main__":
    app.run(debug=True)