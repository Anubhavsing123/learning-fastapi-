from db import engine
from table import user,post
from sqlalchemy import text
#using Raw sql(Text)
def raw_sql():
    with engine.connect() as cnn:
        stat=text("""
                    INSERT INTO users(name,email)
                    VALUES(:name,:email)""")
        cnn.execute(stat,{"name":"sanum","email":"qqumsikms"})
        cnn.commit()
#using Raw sql(Text)
def raw_sql1():
    with engine.connect() as cnn:
        stat=text("""
                    SELECT* FROM users WHERE email=:email
                    """)
        cnn.execute(stat,{"email":"qqumsikms"}).first()
        cnn.commit()

