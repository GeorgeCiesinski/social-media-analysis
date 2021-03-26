from entities.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey


class Comment(Base):

	__tablename__ = 'comment'

	id = Column(String, primary_key=True)
	# ForeignKey enforces the existence of Submission row
	submission_id = Column(String, ForeignKey('submission.id'))  # SQL Table name / column (not class)
	author = Column(String)
	body = Column(String)
	score = Column(Integer)
	saved = Column(Boolean)
	number_of_replies = Column(Integer)
	created_utc = Column(DateTime)

	# Relationships
	# Can be used to find comment.sentiment
	sentiment = relationship('Sentiment', cascade='all, delete', backref='comment')
