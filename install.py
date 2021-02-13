from entities.submission import Submission
from entities.comment import Comment
from entities.sentiment import Sentiment

from entities.base import Base, engine, Session
from sqlalchemy.orm import configure_mappers


class Install:

	def __init__(self):
		# Create the tables
		Base.metadata.create_all(engine)
		print("Created all DDLs")


if __name__ == '__main__':
	Install()
