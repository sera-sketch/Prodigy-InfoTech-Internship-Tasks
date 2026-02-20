from sqlalchemy import create_engine, text

DATABASE_URL = "mysql+pymysql://root:root123@localhost/fastapi_db"

engine = create_engine(DATABASE_URL)

with engine.connect() as connection:
    connection.execute(text("DROP TABLE users"))
    print("Users table deleted successfully!")