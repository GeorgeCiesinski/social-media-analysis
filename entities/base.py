import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc as sqla_exc

connection_path = 'config/connection_string.txt'

engine = None

try:
	with open(connection_path, "r") as text_file:
		connection_string = text_file.read()
		engine = create_engine(connection_string, echo=True)
except FileNotFoundError:
	logging.error(f"The {connection_path} file is missing.")
except sqla_exc.ArgumentError:
	logging.error(f"Unable to connect to the database using the credentials in {connection_path}")

# Start up the session
Session = sessionmaker(bind=engine)

# Initialize the declarative_base for ORM
Base = declarative_base()
