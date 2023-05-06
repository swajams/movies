from flask import Flask, render_template, request, flash, redirect, url_for
from entity import getmovies, moviedetails, searchbar, getshowdate, getshowtime, getsessionid, getReview, getAvgRating


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
    Rating = round(AvgRating[0], 1)
    print(Review)
    print(Rating)  
    if not movieD:
        abort(404)
    return render_template("movdetails.html", data = movieD, T = dates, Review = Review, Rating = Rating )

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

@app.route("/booking/<int:movieID>", methods=['POST'])
def sessioncontroller(movieID):
    date = request.args.get('date')
    selected_time = request.form['selected_time']
    sessionID = getsessionid(movieID, date, selected_time)
    print(date)
    print(selected_time)
    print("Session ID : ")
    print(sessionID)
    return render_template("booking.html")





if __name__ == "__main__":
    app.run(debug=True)