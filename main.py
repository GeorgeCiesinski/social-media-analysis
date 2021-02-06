from scrapers.RedditScraper import RedditScraper

# Login to Praw
r = RedditScraper()

submission_dict = r.extract_post_data(submission_id='5om5sh')
print(submission_dict)

r.extract_post_comments_data(submission_dict.get('submission_object'))

# Call Saif's sentiment analysis function to append data to submission_dict

# Use SQLAlchemy to store submission data into submission table, and comment data into comment table (relationship)