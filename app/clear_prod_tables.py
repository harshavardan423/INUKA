
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy import text
import os
from sqlalchemy import create_engine


# Replace [USERNAME] and [PASSWORD] with your actual environment variable names
username = os.getenv("DB_USERNAME")
password =os.getenv("DB_PASSWORD")
print(f"Username: {username}")
print(f"Password: {password}")



connection_string = f"mysql+mysqlconnector://{username}:{password}@aws.connect.psdb.cloud:3306/inuka"
engine = create_engine(connection_string, echo=True)
print("DB : PROD")


with engine.connect() as connection:
    # connection.execute(text("CREATE TABLE example (id INTEGER, name VARCHAR(20))"))
    # connection.execute(text("CREATE TABLE newtable (id INTEGER, name VARCHAR(20))"))

    connection.execute(text("DROP TABLE answer"))
    connection.execute(text("DROP TABLE applicant"))
    connection.execute(text("DROP TABLE insights_post"))
    connection.execute(text("DROP TABLE job"))
    connection.execute(text("DROP TABLE question"))
    connection.execute(text("DROP TABLE team_member"))

    # connection.execute(text("DROP TABLE example"))
    # connection.execute(text("DROP TABLE newtable"))