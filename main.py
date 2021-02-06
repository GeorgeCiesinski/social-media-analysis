from scrapers.RedditScraper import RedditScraper

# Login to Praw
r = RedditScraper()

submission_dict = r.extract_post_data(submission_id='a1s2d3f4')
print(submission_dict)
