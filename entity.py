
from sqlalchemy import create_engine, text

DB_USER = 'root'
DB_PASS = 'password'
DB_NAME = 'moviedb'

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@localhost/{DB_NAME}")
   
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
        
def getReview(movieID):
    with engine.connect() as conn:
        R = conn.execute(text(f"SELECT review FROM moviedb.ratingreview WHERE MovieID = '{ movieID }'"))
        return R.fetchall()

def getAvgRating(movieID):
    with engine.connect() as conn:
        Rating =  conn.execute(text(f"SELECT AVG(rating) FROM moviedb.ratingreview WHERE MovieID = '{ movieID }' "))
        return Rating.fetchone()[0]
         
         
def displaySeat(sessionID):
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM moviedb.session inner join moviedb.room on moviedb.session.roomID = moviedb.room.roomID inner join moviedb.movies on moviedb.session.movieid = moviedb.movies.movieID where sessionID = "+ "'"+sessionID+"'"))
        return result.all()

def getFoodDrinksCombo():
    with engine.connect() as conn:
        result = conn.execute(text(f"select * from moviedb.food where name like 'combo%'"))
        return result.all()

def getFoodDrinksACarte():
    with engine.connect() as conn:
        result = conn.execute(text(f"select * from moviedb.food where name not like 'combo%'"))
        return result.all()

         
         