from entities.base import Session
from entities.submission import Submission
from entities.comment import Comment
from entities.sentiment import Sentiment

# exceptions
from sqlalchemy.exc import IntegrityError

# logging
from logs.Logger import base_logger


logger = base_logger.getChild(__name__)


class DatabaseManager:

	# Handle session setup and destruction
	def __init__(self):
		self.session = Session()

	def __del__(self):
		self.session.close()

	def check_submission_id(self, submission_dict):

		# Todo: Check if the submission exists using id
		pass

	def insert_submission(self, submission_dict):

		# Insert Submission Data

		_new_submission = Submission(
			id=submission_dict.get('id'),
			title=submission_dict.get('title'),
			selftext=submission_dict.get('selftext'),
			score=submission_dict.get('score'),
			created_utc=submission_dict.get('created_utc'),
		)

		self.session.add(_new_submission)

		try:
			self.session.commit()
		except IntegrityError as e:
			# In case of integrity error, log error and return None
			logger.error('Unable to insert Submission into database due to Integrity Error.')
			logger.error(e)
			return None

		return _new_submission

	def insert_comments(self, comments_dict, submission):

		# Extract comment_data from comments_dict
		_comment_data = comments_dict.get('data')

		# Iterate through comment_data and add sentiment_result list
		for _comment in _comment_data:

			new_comment = Comment(
				id=_comment.get('id'),
				submission_id=submission.id,
				author=_comment.get('author'),
				body=_comment.get('body'),
				score=_comment.get('score'),
				saved=_comment.get('saved'),
				number_of_replies=_comment.get('number_of_replies'),
				created_utc=_comment.get('created_utc'),
			)

			self.session.add(new_comment)

		self.session.commit()

	def insert_sentiment(self, comments_dict):

		# Extract comment_data from comments_dict
		_comment_data = comments_dict.get('data')

		# Iterate through comment_data and add sentiment_result list
		for _comment in _comment_data:
			new_sentiment = Sentiment(
				comment_id=_comment.get('id'),
				polarity=_comment.get('sentiment')[0],
				sentiment=_comment.get('sentiment')[1]
			)

			self.session.add(new_sentiment)

		self.session.commit()
