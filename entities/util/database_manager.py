from sqlalchemy.orm import joinedload
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

			# Extract sentiment dict from comment dict
			_sentiment_dict = _comment.get('sentiment')

			new_sentiment = Sentiment(
				comment_id=_comment.get('id'),
				polarity=_sentiment_dict.get('polarity'),
				sentiment=_sentiment_dict.get('sentiment')
			)

			self.session.add(new_sentiment)

		self.session.commit()

	'''
	DATABASE EXTRACTION
	'''

	def extract_submission(self, submission_dict):
		"""
		Receives partial submission_dict, which must at least include the id. Finds the submission in the database
		and replaces the data in the dict with data from the database. Does not return anything as submission_dict is
		mutable.

		:param dict submission_dict: Partial or complete submission_dict containing at least the id.
		"""

		# Todo: Make submission submission dict instead, maybe get rid of return?

		# Get submission id
		submission_id = submission_dict.get('id')

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

	def extract_comments(self, submission_dict):
		"""
		Receives partial submission_dict, which must at least include the id. Creates a comments_dict and populates it
		with comments with the same id. Returns comments_dict. DOES NOT INCLUDE SENTIMENT DATA.

		:param dict submission_dict: Partial or complete submission_dict containing at least the id.
		:return dict comments_dict: Dict containing data, which is a list of individual comment dicts.
		"""

		# Get submission id
		submission_id = submission_dict.get('id')

		# Extract result from database
		result = self.session.query(Comment) \
			.filter(Comment.submission_id == submission_id) \
			.all()

		# Store comments as dicts in a list stored in the 'data' key.
		comments_dict = {
			'data': [
				item.asdict()
				for item in result
			]
		}

		return comments_dict

	def extract_sentiment(self, comment_id):
		"""
		TBA, function is incomplete.

		:param str comment_id: A string id representing the comment the sentiment is for.
		:return list sentiment: A list containing the polarity and sentiment.
		"""

		# Todo: complete this later

		pass

	def extract_comments_sentiment(self, submission_dict):
		"""
		Receives partial submission_dict, which must at least include the id. Creates a comments_dict and populates it
		with comments with the same id as well as their sentiment data. Returns comments_dict.

		:param dict submission_dict: Partial or complete submission_dict containing at least the id.
		:return dict comments_dict: Dict containing comment and sentiment data.
		"""

		# Get submission id
		submission_id = submission_dict.get('id')

		result = self.session.query(Comment).options(
			joinedload(Comment.sentiment)
		).all()

		# Store comments as dicts in a list stored in the 'data' key.
		comments_dict = {
			'data': [
				# Use asdict to return a dict of columns/keys and values
				item.asdict(
					follow={
						# append sentiment data from joinedload query to Comment dict
						'sentiment': {
							# Only include polarity and sentiment columns
							'only': [
								'polarity',
								'sentiment'
							]
						}
					}
				)
				for item in result
			]
		}

		return comments_dict

	'''
	DATABASE DELETION
	'''

	def delete_submission(self, submission_dict):
		"""
		Deletes the submission from the submission table, as well as child entries in the comment and sentiment tables.
		Adds a new key to submission_dict indicating whether the delete was successful or not.

		:param submission_dict:
		"""

		submission_id = submission_dict.get('id')

		submission = None

		# Check if the submission exists using id
		try:
			submission = self.session.query(Submission) \
				.filter(Submission.id == submission_id) \
				.one()
		except(NoResultFound, MultipleResultsFound) as e:
			logger.warning(f'Could not find submission_id {submission_id} in the database.')
			logger.warning(e)

		# Delete the Submission
		try:
			self.session.delete(submission)
			self.session.commit()

			submission_dict['submission_deleted'] = True

		except Exception as e:
			# If an unexpected exception occurred, handle it
			logger.error('Unexpected exception occurred:')
			logger.error(e)

			submission_dict['submission_deleted'] = False
