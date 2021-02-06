import pytest
from scrapers.RedditScraper import RedditScraper


def test_praw_login():

	# Login to Praw
	r = RedditScraper()
	user_name = r.reddit.user.me()

	assert user_name == 'social-bot'


def test_extract_post_data_id():

	# Login to Praw
	r = RedditScraper()

	# Get submission dict
	submission_dict = r.extract_post_data(submission_id='5om5sh')

	# Check if dict has errors
	assert submission_dict.get('error') is None


def test_extract_post_data_id_fail():

	# Login to Praw
	r = RedditScraper()

	# Get submission dict
	submission_dict = r.extract_post_data(submission_id='a1s2d3f4')

	# Check if dict has errors
	assert submission_dict.get('error') is not None


def test_extract_post_data_url():

	# Login to Praw
	r = RedditScraper()

	_submission_url = 'https://www.reddit.com/r/redditdev/comments/5om5sh/praw_how_do_i_get_submission_info/'

	# Get submission dict
	submission_dict = r.extract_post_data(submission_url=_submission_url)

	# Check if dict has errors
	assert submission_dict.get('error') is None
