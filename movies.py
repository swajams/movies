from flask import Flask, render_template, request, flash, redirect, url_for, jsonify,json
from entity import getFoodDrinksCombo, getFoodDrinksACarte, displayReview, Success, getFoodDetails, getBookedSeats ,updateSessions, bookingHistory, insertTicket, getSerialNo
from entity import Session, MovieEntity, RR, tempBooking
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import datetime, random


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
    Review = RR.getReview(movieID)
    AvgRating = RR.getAvgRating(movieID)
    if AvgRating is not None:
        Rate = round(AvgRating, 1)
    else:
        Rate = None

    if not movieD:
        abort(404)

    current_date = datetime.datetime.now()
  
    
    past_dates = []
    for date in dates:
        if date[0] > current_date:
            past_dates.append(date)
    for date in past_dates:
        print(date)     
        

    return render_template("movdetails.html", data=movieD, T=past_dates, Review=Review, Rating=Rate)
    




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
    holdSeats = tempBooking.getTempBooking(seatDetails.roomID, seatDetails.dateTime)
    if holdSeats == None:
        holdSeats = "{}"
    
    return render_template("seat.html", seatDetails = seatDetails, holdSeats = holdSeats)



@app.route('/processJsonFoodDrinks', methods=['POST'])
def processJsonFoodDrinks():
        if(request.method == 'POST'):
            global jsonData
            data = request.json
            print(data)
            jsonData = data
            oldList  = jsonData["bookedSeats"]
            newList = [item.replace("'", "\"") for item in oldList]
            print(newList)
            tempBooking.createTempBooking(jsonData["roomID"], jsonData["movieID"], json.dumps(newList), datetime.datetime.now(), jsonData["dateTime"])
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
    userID = 6666

    if request.method == 'POST':
        Rating = request.form.get("rate")
        Review = request.form.get("review")
        if Rating is not None and Review is not None:
            RR.setRatingReview(movieID=movieID, Rating=int(Rating), Review=Review, userID=userID)
            flash("Submitted Successfully!")
 
    return render_template('RatingReview.html', data=movieD)


def deleteTempSession():
    tempBooking.deleteExpiredBooking()
    
scheduler = BackgroundScheduler()
scheduler.add_job(func=deleteTempSession, trigger='interval', minutes=2) # Runs every hour
scheduler.start()


@app.route('/reviewPage', methods=['GET','POST'])
def reviewPage():
    if request.method == 'POST':
        serial_No = request.form.get('code') 
        print(f"serial_No = {serial_No}")
        get_serial = getSerialNo(serial_No)

        if get_serial == 0:
            return jsonify(
                found = False
            )
        else:
            for i in get_serial:
                return jsonify(
                    found = True,
                    name = i.reward_name,
                    description = i.description,
                    rewardType = i.rewardType,
                    discount = i.discount
                )
    return render_template('reviewpage.html')


@app.route('/bookingSuccess')
def bookingSuccess():
    global jsonData
    bookedSeats = json.loads(getBookedSeats(jsonData["sessionID"]).bookedSeats)
    #print("bookedSeats =", bookedSeats)
    #for i in jsonData["bookedSeats"]:

    ticket_types = []
    for i in range(0, int(jsonData["ticketType"]["adultTix"])):
        ticket_types.append("adultTix")
    for i in range(0, int(jsonData["ticketType"]["studentTix"])):
        ticket_types.append("studentTix")
    for i in range(0, int(jsonData["ticketType"]["seniorTix"])):
        ticket_types.append("seniorTix")
    for i in range(0, int(jsonData["ticketType"]["childTix"])):
        ticket_types.append("childTix")


    for i in range(0, len(jsonData["bookedSeats"])):
        bookedSeats.append(jsonData["bookedSeats"][i])
        print(bookedSeats[i])
        print("userID", "roomID", "movieID", "seatSelected", "dateTime", "ticketType", "status")
        #ticket_types = jsonData["ticketType"][i]
        print("Ticket type is " + ticket_types[i])
        print("----------------------")
        loyaltyPoints = random.randint(10, 100)
        flash(f"You have earned {loyaltyPoints} loyalty points !", category="success")
        insertTicket("3", jsonData["roomID"], int(jsonData["movieID"]), jsonData["bookedSeats"][i], jsonData["dateTime"], ticket_types[i] , "unwatched", loyaltyPoints)    


    strbookedSeats = json.dumps(bookedSeats)
    updateSessions(strbookedSeats,jsonData["sessionID"])
    booking = Success()
    return render_template('bookedDetails.html', booking=booking)


@app.route('/pastBooking')
def viewPastBooking():
    UID = 'U1'
    pastb = bookingHistory(UID)
    return render_template('pastBooking.html', pastb=pastb)


@app.route('/retrieve_food', methods =["POST"])
def retrieveFOOD():
    if request.method == "POST":
        foodid = request.form.get("foodid") #get data just now from the POST method, equivalent from line 71 in reviewpage.html
        details = getFoodDetails(foodid) #call the fn from entity.py, getFoodDetails is to execute the query
        name = ""
        for i in details: #iterate inside details then retrieve the name of the food from
            name = i.name #assign name of food to the name variable from db
            price = i.price
        return jsonify({"FoodName": name, "Price" : price}) #return the json back to html
    return render_template('reviewpage.html')

if __name__ == "__main__":
    app.run(debug=True)

 