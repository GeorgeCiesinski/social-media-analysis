"""
Author: Saif Gorges
Date: March 11 2021
"""

# Import dependencies
import pandas as pd
import matplotlib.pyplot as plt
import json
from pandas import json_normalize
from pprint import pprint

comment_dict = {'data': [{'id': 'grl2104', 'author': 'RedPandaBearCat',
                          'body': '>\\>> easily get Jobs and Internships after 2 months of learning\n\nWell, it could work if such person has appropriate background in similar/related field and/or specific talent, e.g. being applied mathematician and re-training for a junior role in data science.\n\nOr being front-end developer (JavaScript / React) and re-training for a junior role in back-end  (Node.js / Express) with the same language (JavaScript) within the same organization.\n\nEven then, 2 months? That seems to be too short. Or it may be an exaggeration. Or maybe the aforementioned person is extremely talented.',
                          'score': 25, 'saved': False, 'number_of_replies': 1, 'created_utc': '2021-03-20 12:49:21',
                          'sentiment': {'polarity': 0.18148148148148147, 'sentiment': 'Positive'}},
                         {'id': 'grl9vb3', 'author': 'Snoo-65620',
                          'body': '2 months = 60 days \\* 12h/day = 720h . You can do FullStackOpen or FCC fully or by skipping minor parts. Still 12h/day its damn hard, and even if you make it there is no guarantee of a job, since you still have to prepare for the interview, build portfolio, more projects etc.  I suggest aiming to get a job after 3 months at the very least with a more duable workload of 8h/day.',
                          'score': 12, 'saved': False, 'number_of_replies': 1, 'created_utc': '2021-03-20 14:14:11',
                          'sentiment': {'polarity': 0.05366666666666666, 'sentiment': 'Positive'}},
                         {'id': 'grlc9bl', 'author': 'amymhaddad11',
                          'body': 'I highly recommend learning the fundamentals of programming, which I outline in Programmer’s Pyramid: [programmerspyramid.com](https://programmerspyramid.com/)\n\nIt’s a free learning tool that I created. The Pyramid is organized by topic, and contains links to problems, programs, books, and courses. For each topic, I explain how to use the provided resources and offer tips to help you learn the content.\n\nThe skills and concepts contained in the Pyramid will certainly help you on your programming journey.',
                          'score': 13, 'saved': False, 'number_of_replies': 0, 'created_utc': '2021-03-20 14:37:14',
                          'sentiment': {'polarity': 0.006071428571428582, 'sentiment': 'Positive'}},
                         {'id': 'grlohh7', 'author': 'ericjmorey',
                          'body': ">I have a lot of time constraints, so going through the above mentioned courses is not viable for me.\n\nIt's unlikely you have the time to learn the skills needed. I wish I had better news for you.",
                          'score': 4, 'saved': False, 'number_of_replies': 0, 'created_utc': '2021-03-20 16:25:53',
                          'sentiment': {'polarity': 0.0, 'sentiment': 'Neutral'}},
                         {'id': 'grlsqkj', 'author': 'theprogrammingsteak',
                          'body': 'Since you have limited time I would focus on mainly either front end ofñr backend. For skills I would say, Debugging, setting break points, stepping in and out if methods, inspecting variables in debugger, etc.',
                          'score': 3, 'saved': False, 'number_of_replies': 0, 'created_utc': '2021-03-20 17:02:00',
                          'sentiment': {'polarity': 0.047619047619047616, 'sentiment': 'Positive'}},
                         {'id': 'grlxet1', 'author': 'OstGeneralen',
                          'body': '2 Months of learning definitely seems too short to pick up everything that I would expect from an application for internship. Not saying it\'s impossible, but absolutely not the most common scenario.\n\nI started out as an intern myself and I had at that time spent 5 years in schools + a university specialising in the field that I was applying for.\n\nOthers have already given you some good answers for the programming skills. I just thought I\'d pop in to also mention some "softer" ones:\n\n* Communication - Showing that you are good at communicating and willing to ask questions is something that is always appreciated from interns (even if you yourself as the intern may think you\'re "annoying" etc. I know that I sure did)\n* Build a network - Start sending out connection requests on LinkedIn etc. to people in the industry. Make sure you have an up to date profile. You\'ll more than likely start getting approached by recruiters. Even if you\'re not ready yet, it\'ll give you some great info on what is commonly looked for in applicants.\n* Build a portfolio - Create some small-ish pojects and create a portfolio where potential employers can look through them. It doesn\'t hurt if you format these in a short blog-post kind of way where you explain your thought process a bit more in depth (don\'t overdo it though, they won\'t have time to read through pages upon pages of information)',
                          'score': 3, 'saved': False, 'number_of_replies': 1, 'created_utc': '2021-03-20 17:41:33',
                          'sentiment': {'polarity': 0.1471014492753623, 'sentiment': 'Positive'}},
                         {'id': 'grm53u5', 'author': 'sobakablevanula',
                          'body': "I know it's an english platform, but russian company yandex has some book recommendations for students, who want to get an internship. There are books about c++, java, python, math and others(you can just translate the titles). I'm studying based on them right now. Maybe this can help you.\nhttps://yandex.ru/jobs/internship/",
                          'score': 1, 'saved': False, 'number_of_replies': 0, 'created_utc': '2021-03-20 18:42:55',
                          'sentiment': {'polarity': 0.09523809523809523, 'sentiment': 'Positive'}},
                         {'id': 'grky8eh', 'author': 'otherreddituser2017', 'body': 'Following', 'score': -4,
                          'saved': False, 'number_of_replies': 0, 'created_utc': '2021-03-20 11:59:18',
                          'sentiment': {'polarity': 0.0, 'sentiment': 'Neutral'}}]}
pprint(comment_dict)

# Create empty lists
author = []
body = []
created_utc = []
id = []
number_of_replies = []
saved = []
score = []
sentiment_polarity = []
sentiment_description = []

# Parse through json file and append lists
for x in range(len(comment_dict['data'])):
    author.append(comment_dict['data'][x]['author'])
    body.append(comment_dict['data'][x]["body"])
    created_utc.append(comment_dict['data'][x]["created_utc"])
    id.append(comment_dict['data'][x]['id'])
    number_of_replies.append(comment_dict['data'][x]["number_of_replies"])
    saved.append(comment_dict['data'][x]['saved'])
    score.append(comment_dict['data'][x]["score"])
    sentiment_polarity.append(comment_dict['data'][x]["sentiment"]["polarity"])
    sentiment_description.append(comment_dict['data'][x]["sentiment"]["sentiment"])

# Create and clean dataframe
comment_df = pd.DataFrame(
    zip(author, body, created_utc, id, number_of_replies, saved, score, sentiment_polarity, sentiment_description))

# rename columns
comment_df = comment_df.rename(
    columns={0: "Author", 1: "Comment", 2: "Date", 3: "ID", 4: "Number of Replies", 5: "Saved", 6: "Upvotes",
             7: "Sentiment Polarity", 8: "Sentiment Description"})
comment_df['Sentiment Polarity'] = pd.DataFrame(comment_df['Sentiment Polarity'].values.tolist())
comment_df.head()

# create bins column
bins = [-1, -.75, -.5, -.25, 0, .25, .5, .75, 1]
comment_df['Sentiment Range'] = pd.cut(comment_df['Sentiment Polarity'], bins)

comment_df.head()

# Transform dataframe to model stats for sentiment
sentiment_stats = comment_df.groupby("Sentiment Range").agg(
    id_count=('ID', 'count'),
    score_sum=('Upvotes', 'sum'),
    replies_count=('Number of Replies', 'sum'),
)
sentiment_stats = sentiment_stats.reset_index()
sentiment_stats['Sentiment Range'] = sentiment_stats['Sentiment Range'].astype(str)

# Rename DataFrame
sentiment_stats = sentiment_stats.rename(
    columns={"id_count": "Total Count", "score_sum": "Total Upvotes", "replies_count": "Total Replies"})
sentiment_stats

# Creating axes object and defining plot
ax = sentiment_stats.plot(kind='bar', x='Sentiment Range',
                          y='Total Count', color='Blue',
                          linewidth=3, rot=90)

ax2 = sentiment_stats.plot(kind='line', x='Sentiment Range',
                           y='Total Upvotes', secondary_y=True,
                           color='Red', linewidth=3, rot=90,
                           ax=ax)

# Title of the plot
plt.title("Overall Sentiment & Upvotes")

# Labeling x and y-axis
ax.set_xlabel('Sentiment Range', color='black')
ax.set_ylabel('Sentiment Count', color="b")
ax2.set_ylabel('Total Upvotes', color='r')

# Defining display layout
plt.tight_layout()

# Show plot
plt.savefig("Graphs/overall_sentiment_and_upvotes.png")
plt.show()

# Creating axes object and defining plot
ax = sentiment_stats.plot(kind='bar', x='Sentiment Range',
                          y='Total Replies', color='Blue',
                          linewidth=3, rot=90)

ax2 = sentiment_stats.plot(kind='line', x='Sentiment Range',
                           y='Total Replies', secondary_y=True,
                           color='Green', linewidth=3, rot=90,
                           ax=ax)

# Title of the plot
plt.title("Overall Sentiment & Total Replies")

# Labeling x and y-axis
ax.set_xlabel('Sentiment Range', color='black')
ax.set_ylabel('Sentiment Count', color="b")
ax2.set_ylabel('Total Replies', color='g')

# Defining display layout
plt.tight_layout()

# Show plot
plt.savefig("Graphs/overall_sentiment_and_replies.png")
plt.show()

# Create scatterplot for timeline vs sentiment

ax1 = comment_df.plot.scatter(x='Date', y='Sentiment Polarity', c='Upvotes', colormap="viridis", rot=90)
plt.savefig("Graphs/sentiment_timeline.png")

# Create DataFrame for sentiment description

sentiment_description_df = comment_df.groupby("Sentiment Description").agg(
    total_count=('ID', 'count')
)
# sentiment_description_df = sentiment_description_df.rename(columns={"total_count": "Sentiment"})
sentiment_description_df

# Create pie graph for sentiment distribution

sentiment_pie = sentiment_description_df.plot.pie(y='total_count', figsize=(5, 5))
plt.savefig("Graphs/sentiment_pie.png")
sentiment_pie