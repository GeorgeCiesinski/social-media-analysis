from entities.base import Session
from entities.submission import Submission
from entities.comment import Comment

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
		comment_data = comments_dict.get('data')

		# Iterate through comment_data and add sentiment_result list
		for comment in comment_data:

			new_comment = Comment(
				id=comments_dict.get('id'),
				submission_id=submission.id,
				author=comments_dict.get('author'),
				body=comments_dict.get('body'),
				score=comments_dict.get('score'),
				saved=comments_dict.get('saved'),
				number_of_replies=comments_dict.get('number_of_replies'),
				created_utc=comments_dict.get('created_utc'),
			)

			self.session.add(new_comment)

		self.session.commit()
