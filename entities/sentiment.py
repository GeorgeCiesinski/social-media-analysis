from entities.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float


class Sentiment(Base):

	__tablename__ = 'sentiment'

	id = Column(Integer, primary_key=True, autoincrement=True)
	comment_id = Column(String, ForeignKey('comment.id'))
	polarity = Column(Float)
	sentiment = Column(String)
