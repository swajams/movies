
from sqlalchemy import create_engine, text

DB_USER = 'root'
DB_PASS = 'password'
DB_NAME = 'moviedb'

 
engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@localhost/{DB_NAME}")
   
class MovieEntity:

    def getmovies():
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT * FROM moviedb.movies"))
            return result.fetchall()

    def moviedetails(movieID):
        with engine.connect() as conn:
            details = conn.execute(text(f"SELECT * FROM moviedb.movies WHERE movieid = :movieID"), {"movieID" : movieID})
            return details.fetchone()      
         
    def searchbar(search_query):
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT * FROM moviedb.movies WHERE Name LIKE '%{search_query}%'"))
            return result.fetchall()


class RR:     

    def getReview(movieID):
        with engine.connect() as conn:
            R = conn.execute(text(f"SELECT review FROM moviedb.ratingreview WHERE MovieID = '{ movieID }'"))
            return R.fetchall()     

    def getAvgRating(movieID):
        with engine.connect() as conn:
            Rating =  conn.execute(text(f"SELECT AVG(rating) FROM moviedb.ratingreview WHERE MovieID = '{ movieID }' "))
            return Rating.fetchone()[0]
            
    def setRatingReview(movieID, Rating, Review, userID):
        with engine.connect() as conn:
            conn.execute(text("INSERT INTO ratingreview (movieid, review, rating, userid) VALUES (:movieID, :Review, :Rating, :userID)"),
                         {"movieID": movieID, "Rating": Rating, "Review": Review, "userID": userID})
        conn.commit()
  
def getFoodDrinksCombo():
    with engine.connect() as conn:
        result = conn.execute(text(f"select * from moviedb.food where name like 'combo%'"))
        return result.all()

def getFoodDrinksACarte():
    with engine.connect() as conn:
        result = conn.execute(text(f"select * from moviedb.food where name not like 'combo%'"))
        return result.all()

def displayReview():
    with engine.connect() as conn:
        result = conn.execute(text(f"select * from moviedb.rewards INNER JOIN moviedb.generatedrewards ON moviedb.rewards.rewardID = moviedb.generatedrewards.rewardID "))
        return result.all()

def Success():
    with engine.connect() as conn:
        result = conn.execute(text(f"select * from moviedb.movies INNER JOIN moviedb.ticket ON moviedb.movies.movieid = moviedb.ticket.movieid"))
        return result.all()

def getBookedSeats(sessionID):
    with engine.connect() as conn:
        result = conn.execute(text(f"select bookedSeats from moviedb.session where sessionID = " + "'" + sessionID + "'"))
        return result.fetchone()

def updateSessions(bookedSeats, sessionID):
    with engine.connect() as conn:
        conn.execute(text(f"UPDATE moviedb.session set bookedSeats = " + "'" + bookedSeats + "'" + "where sessionID =" + "'" + sessionID + "'"))
        conn.commit()

def insertTicket(userID, roomID, movieID, seatSelected, dateTime, ticketType, status, loyaltyPoints):
    with engine.connect() as conn:
        print(ticketType)
        query = text(f"INSERT INTO moviedb.ticket (userID, roomID, movieid, seatSelected, dateTime, ticketType, status) VALUES ('{userID}', '{roomID}', '{movieID}', '{seatSelected}', '{dateTime}', '{ticketType}', '{status}' );")
        conn.execute(query)
        conn.commit()
        query = text(f"UPDATE moviedb.customer SET loyalty_point = loyalty_point + '{loyaltyPoints}' WHERE uid = '{userID}';")
        conn.execute(query)
        conn.commit()

def getSerialNo(serialNo):
    with engine.connect() as conn:
        result = conn.execute(text(f"select * from moviedb.generatedrewards inner join moviedb.rewards on moviedb.generatedrewards.rewardID = moviedb.rewards.rewardID where serialNo = '{serialNo}';"))
        return result.all()

def getFoodDetails(foodid):
    with engine.connect() as conn:
        result = conn.execute(text(f"select * from moviedb.food where itemID = '{foodid}' "))
        return result.all()

#def insert(rewardID, serialNo):
#    with engine.connect() as conn:
#        query = text(f"INSERT INTO moviedb.generatedreward (rewardID, serialNo) VALUES ('{rewardID}', '{serialNo}');")
#        conn.execute(query)
#        conn.commit()

def bookingHistory(userID):
    with engine.connect() as conn:
        result = conn.execute(text(f"select * from moviedb.movies INNER JOIN moviedb.ticket ON moviedb.movies.movieid = moviedb.ticket.movieid where userID = '{userID}' "))
        return result.all()

class Session:
    def __init__(self, sessionID,roomID, movieID, bookedSeats, dateTime, status):
        self.sessionID = sessionID
        self.roomID = roomID
        self.movieID = movieID
        self.bookedSeats = bookedSeats
        self.dateTime = dateTime
        self.status = status

    def display_seat(sessionID):
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT * FROM moviedb.session inner join moviedb.room on moviedb.session.roomID = moviedb.room.roomID inner join moviedb.movies on moviedb.session.movieid = moviedb.movies.movieID where sessionID = "+ "'"+sessionID+"'"))
            data = result.fetchone() 
            return data    

    def getshowdate(movieID):
        with engine.connect() as conn:
             dates = conn.execute(text(f"SELECT dateTime FROM moviedb.session WHERE MovieID = '{ movieID }'"))
             return dates.fetchall() 

    def getshowtime(movieID, date):
        with engine.connect() as conn:
            timing = conn.execute(text(f"SELECT dateTime FROM moviedb.session WHERE MovieID = '{ movieID }' AND dateTime LIKE '%{ date }%'"))
            timings = [row[0].strftime('%H:%M') for row in timing.fetchall()]
            return timings     

    def getsessionid(movieID, date, selected_timing):
        with engine.connect() as conn:
            session = conn.execute(text(f"SELECT sessionID FROM moviedb.session WHERE MovieID = '{ movieID }' AND dateTime LIKE '%{ date }%' AND dateTime LIKE '%{ selected_timing }%' "))
            return session.fetchall()
        
class tempBooking:
    def createTempBooking(roomID, movieID, holdSeats, createdTime ,dateTime):
        with engine.connect() as conn:
            conn.execute(text("INSERT INTO moviedb.tempbooking (roomID, movieID, holdSeats, createdTime ,dateTime) VALUES (:roomID, :movieID, :holdSeats, :createdTime ,:dateTime)"),
                         {"roomID": roomID, "movieID": movieID, "holdSeats": holdSeats, "createdTime" : createdTime ,"dateTime": dateTime})
            conn.commit()

    def getTempBooking(roomID, dateTime):
        print(roomID)
        print(dateTime)
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT holdSeats FROM moviedb.tempbooking WHERE roomID = '{ roomID }' AND dateTime = '{ dateTime }' "))
            return result.fetchall()

    def deleteExpiredBooking():
        with engine.connect() as conn:
            conn.execute(text(f"delete from moviedb.tempbooking WHERE createdTime <= DATE_SUB(NOW(), INTERVAL 10 MINUTE);"))
            conn.commit()
    