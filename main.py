from scrapers.RedditScraper import RedditScraper
from sentiment_analysis import SentimentAnalysis


# Login to Praw
r = RedditScraper()

# Get submission dict
submission_url = input('Enter the post url: ')
submission_dict = r.extract_post_data(submission_url=submission_url)

# Get list of comments_dicts
submission_object = submission_dict.get('submission_object')
comments_dict = r.extract_post_comments_data(submission_object)

# Call sentimentanalysis to analyze the comments and append the dicts
SentimentAnalysis.list_parser(comments_dict)

# Temporarily output data for debugging
# Todo: Update to remove once SQLAlchemy is working
print("Scrape Complete. See outputs.")

# Output submission data
with open('output/submission_dict.txt', "w+") as text_file:
	text_file.write(str(submission_dict))

# Output comment data
with open('output/comments_dict.txt', "w+") as text_file:
	text_file.write(str(comments_dict))

# Use SQLAlchemy to store submission data into submission table, and comment data into comment table (relationship)