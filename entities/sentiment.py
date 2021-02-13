from entities.base import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship


class Sentiment(Base):

	__tablename__ = 'sentiment'

	id = Column(Integer, primary_key=True, autoincrement=True)
	comment_id = Column(String, ForeignKey('comment.id'))
	polarity = Column(Float)
	sentiment = Column(String)

	# Relationship
	comment = relationship('Comment', uselist=False)

