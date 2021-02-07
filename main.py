from scrapers.RedditScraper import RedditScraper
from sentiment_analysis import SentimentAnalysis


# Login to Praw
r = RedditScraper()

# Get submission dict
submission_url = input('Enter the post url: ')
submission_dict = r.extract_post_data(submission_url=submission_url)
print(submission_dict)

# Get list of comments_dicts
submission_object = submission_dict.get('submission_object')
list_of_comments = r.extract_post_comments_data(submission_object)

# Call sentimentanalysis to analyze the comments and append the dicts
SentimentAnalysis.list_parser(list_of_comments)

print(list_of_comments)

with open('output/comment_list.txt', "w+") as text_file:
	text_file.write(str(list_of_comments))

# Use SQLAlchemy to store submission data into submission table, and comment data into comment table (relationship)