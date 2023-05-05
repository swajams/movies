
from sqlalchemy import create_engine, text

DB_USER = 'root'
DB_PASS = 'E^^hnikh1984'
DB_NAME = 'movietest'

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@localhost/{DB_NAME}")
   
def getmovies():
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM movietest.movies"))
        return result.fetchall()

def moviedetails(movieID):
    with engine.connect() as conn:
        details = conn.execute(text(f"SELECT * FROM movietest.movies WHERE movieid = :movieID"), {"movieID" : movieID})
        return details.fetchone()      
         
def searchbar(search_query):
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM movietest.movies WHERE Name LIKE '%{search_query}%'"))
        return result.fetchall()
            
def getshowdate(movieID):
    with engine.connect() as conn:
         dates = conn.execute(text(f"SELECT dateTime FROM movietest.session WHERE MovieID = '{ movieID }'"))
         return dates.fetchall()
         
def getshowtime(movieID, date):
    with engine.connect() as conn:
        timing = conn.execute(text(f"SELECT dateTime FROM movietest.session WHERE MovieID = '{ movieID }' AND dateTime LIKE '%{ date }%'"))
        timings = [row[0].strftime('%H:%M') for row in timing.fetchall()]
        return timings
        
def getsessionid(movieID, date, selected_timing):
    with engine.connect() as conn:
        session = conn.execute(text(f"SELECT sessionID FROM movietest.session WHERE MovieID = '{ movieID }' AND dateTime LIKE '%{ date }%' AND dateTime LIKE '%{ selected_timing }%' "))
        print("entity")
        print(session)
        print("entity end")
        return session.fetchall()
         
         
         
         
         
         