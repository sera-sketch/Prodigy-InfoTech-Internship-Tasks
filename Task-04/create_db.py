from sqlalchemy import create_engine, text

# connect WITHOUT database first
engine = create_engine("mysql+pymysql://root:root123@localhost")

with engine.connect() as connection:
    connection.execute(text("CREATE DATABASE fastapi_db"))
    print("Database created successfully!")