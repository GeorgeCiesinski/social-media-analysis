from scrapers.RedditScraper import RedditScraper

# Login to Praw
r = RedditScraper()

# Get submission dict
submission_url = 'https://www.reddit.com/r/redditdev/comments/ld59tj/wallsteeetbets_apis/'
submission_dict = r.extract_post_data(submission_url=submission_url)
print(submission_dict)

# Get list of comments
submission_object = submission_dict.get('submission_object')
list_of_comments = r.extract_post_comments_data(submission_object)

# for comment in list_of_comments:
#
# 	print(comment)

# Call Saif's sentiment analysis function to append data to submission_dict

# Use SQLAlchemy to store submission data into submission table, and comment data into comment table (relationship)