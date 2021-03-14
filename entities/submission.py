from entities.base import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship


class Submission(Base):

	__tablename__ = 'submission'

	id = Column(String, primary_key=True)
	title = Column(String)
	selftext = Column(String)
	score = Column(Integer)
	created_utc = Column(DateTime)

	# Relationships
	comment = relationship('Comment')  # One to many relationship
