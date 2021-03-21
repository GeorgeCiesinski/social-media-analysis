from entities.base import Session
from entities.submission import Submission
from entities.comment import Comment
from entities.sentiment import Sentiment

# exceptions
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

# logging
from logs.Logger import base_logger


logger = base_logger.getChild(__name__)


class DatabaseManager:

	# Handle session setup and destruction
	def __init__(self):
		self.session = Session()

	def __del__(self):
		self.session.close()

	def check_submission_exists(self, submission_dict):
		"""
		Checks if a submission id already exists in database, and returns True or False.

		:param dict submission_dict: Dict containing submission information
		:return bool submission_exists: Value representing whether submission exists in database
		"""

		submission_id = submission_dict.get('id')

		submission = None

		# Check if the submission exists using id
		try:
			submission = self.session.query(Submission) \
				.filter(Submission.id == submission_id) \
				.one()
		except(NoResultFound, MultipleResultsFound) as e:
			logger.warning('Could not find submission_id in the database.')
			logger.warning(e)

		return submission

	'''
	DATABASE INSERTION
	'''

	def insert_submission(self, submission_dict):
		"""
		Creates a submission object, inserts into the database, and returns the object with newly generated id.

		:param dict submission_dict: Dict containing submission information
		:return Submission submission: An instance of the Submission object
		"""

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
		"""
		Iterates through the list of comments and creates comment objects. Inserts the comment objects into the
		database.

		:param dict comments_dict: Dict containing a list of comment dicts
		:param Submission submission: An instance of the Submission object
		"""

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
		"""
		Iterates through the list of comments, extracts sentiment data,  and creates sentiment objects. Inserts the
		sentiment objects into the database.

		:param dict comments_dict: Dict containing a list of comment dicts
		"""

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

	'''
	DATABASE EXTRACTION
	'''

	def extract_submission(self, submission):
		"""

		:param dict submission:
		:return dict submission_dict:
		"""

		# Todo: Make submission submission dict instead, maybe get rid of return?

		# Get submission id
		submission_id = submission.get('id')

		try:
			# Extract result from database
			result = self.session.query(Submission) \
				.filter(Submission.id == submission_id) \
				.one()
			submission_dict = result.asdict()

		except (NoResultFound, MultipleResultsFound) as e:
			_error_message = f'Unable to find submission {submission_id} in database.'
			logger.error(_error_message)
			logger.error(e)
			submission_dict = {
				'error': _error_message
			}

		return submission_dict

	def extract_comments(self, submission):

		# Get submission id
		submission_id = submission.get('id')

		# Extract result from database
		result = self.session.query(Comment) \
			.filter(Comment.submission_id == submission_id) \
			.all()

		print(isinstance(result, list))
		print(type(result))

		comments_dict = {
			'data': [
				item.asdict()
				for item in result
			]
		}

		return comments_dict

	def extract_sentiment(self, comments_dict):

		pass

	def create_comments_dict(self, submission_id):

		pass

	'''
	DATABASE DELETION
	'''

	def delete_submission(self):

		pass

	def delete_comments(self):

		pass

	def delete_sentiment(self):

		pass