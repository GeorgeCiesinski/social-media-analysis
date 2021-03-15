"""
Author: Saif Gorges
Date: March 11 2021
"""

import pandas as pd
import json
from pandas import json_normalize
from pprint import pprint

comment_dict = {'data': [{'id': 'gqmqjsa', 'author': 'ronigusija', 'body': 'What app is this', 'score': 3, 'saved': False, 'number_of_replies': 0, 'sentiment': [0.0, ' Neutral']}, {'id': 'gqmr1wm', 'author': 'Bravo2020-', 'body': 'Awesome 👌 stay positive!', 'score': 1, 'saved': False, 'number_of_replies': 0, 'sentiment': [0.6420454545454546, ' Positive']}, {'id': 'gqmso2f', 'author': 'hockjd', 'body': 'Way to go! 28% return is meaningful to anyone. Good job.', 'score': 1, 'saved': False, 'number_of_replies': 0, 'sentiment': [0.6, ' Positive']}, {'id': 'gqmvzwj', 'author': 'Punkag', 'body': "Congrats, buddy. That's a great milestone!", 'score': 1, 'saved': False, 'number_of_replies': 0, 'sentiment': [1.0, ' Positive']}, {'id': 'gqmz0jj', 'author': 'Positive_Principle52', 'body': 'Well done 👏👏', 'score': 1, 'saved': False, 'number_of_replies': 0, 'sentiment': [0.0, ' Neutral']}, {'id': 'gqn0eib', 'author': 'oneilg25', 'body': "Good work! Two weeks ago I was up 700.... now I'm down 1500 🙃🙃\n\nPlay it smarter than me!", 'score': 1, 'saved': False, 'number_of_replies': 0, 'sentiment': [0.3402777777777778, ' Positive']}, {'id': 'gqn0vei', 'author': 'zazone23', 'body': 'Congratulations!!!! Hitting your first 500 is exciting!', 'score': 1, 'saved': False, 'number_of_replies': 0, 'sentiment': [0.3125, ' Positive']}, {'id': 'gqmy1m0', 'author': 'Professional-Amoeba2', 'body': 'Anyone can type in whatever they want in this app. FAKEEEEEER', 'score': -1, 'saved': False, 'number_of_replies': 0, 'sentiment': [0.0, ' Neutral']}]}

pprint(comment_dict)

author = []
body = []
id = []
number_of_replies = []
saved = []
score = []
sentiment = []

for x in range(len(comment_dict['data'])):
    author.append(comment_dict['data'][x]['author'])
    body.append(comment_dict['data'][x]["body"])
    id.append(comment_dict['data'][x]['id'])
    number_of_replies.append(comment_dict['data'][x]["number_of_replies"])
    saved.append(comment_dict['data'][x]['saved'])
    score.append(comment_dict['data'][x]["score"])
    sentiment.append(comment_dict['data'][x]["sentiment"])

comment_df = pd.DataFrame(zip(author,body,id,number_of_replies,saved,score,sentiment))
comment_df = comment_df.rename(columns={0: "Author", 1: "Comment", 2: "ID", 3: "Number of Replies", 4: "Saved", 5:"Score", 6:"Sentiment"})
comment_df.head()