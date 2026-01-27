#db file to create_engine (conection of database)
from sqlalchemy import create_engine
DATABASE_URL="sqlite:///../sqlite.db"
engine=create_engine(DATABASE_URL,echo=True)#echo is used to show all the 
#sql query log in the terminal
