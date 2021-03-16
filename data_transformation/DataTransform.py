"""
Author: Saif Gorges
Date: March 11 2021
"""

#Import dependencies
import pandas as pd
import matplotlib.pyplot as plt
import json
from pandas import json_normalize
from pprint import pprint

comment_dict = {'data': [{'id': 'gqys1yp', 'author': 'autotldr', 'body': 'This is the best tl;dr I could make, [original](https://www.reuters.com/article/us-britain-crime-murder/london-police-face-backlash-after-dragging-mourners-from-vigil-for-murdered-woman-idUSKBN2B605T) reduced by 40%. (I\'m a bot)\n*****\n> 4 Min Read.LONDON - London police faced a backlash from the public on Sunday and an official inquiry into their actions after using heavy-handed tactics to break up an outdoor vigil for a woman whose suspected killer is a police officer.\n\n> Police had denied permission for a vigil on Saturday evening at London&#039;s Clapham Common, near where Everard was last seen alive, citing regulations aimed at preventing the spread of the coronavirus.\n\n> &quot;Last night people were very, very upset, there was a great deal of emotion, completely understandably, and the police, being as they are operationally independent, will be having to explain that to the Home Secretary,&quot; safeguarding minister Victoria Atkins told Sky News.London police chief Cressida Dick backed her officers and said that they needed to make a very difficult judgement.\n\n\n*****\n[**Extended Summary**](http://np.reddit.com/r/autotldr/comments/m590hb/london_police_face_backlash_after_dragging/) | [FAQ](http://np.reddit.com/r/autotldr/comments/31b9fm/faq_autotldr_bot/ "Version 2.02, ~563958 tl;drs so far.") | [Feedback](http://np.reddit.com/message/compose?to=%23autotldr "PM\'s and comments are monitored, constructive feedback is welcome.") | *Top* *keywords*: **police**^#1 **officer**^#2 **very**^#3 **Saturday**^#4 **women**^#5', 'score': 1, 'saved': False, 'number_of_replies': 0, 'created_utc': '2021-03-15 01:01:52', 'sentiment': [0.20071428571428576, ' Positive']}, {'id': 'gqysxox', 'author': 'askewurchin', 'body': 'They didn\'t "drag mourners"....\n\nThey arrested FOUR women who had turned up to hijack a vigil and turn it into a protest they knew was illegal and then refused to leave.', 'score': 1, 'saved': False, 'number_of_replies': 1, 'created_utc': '2021-03-15 01:10:23', 'sentiment': [-0.3, ' Negative']}, {'id': 'gqyq3jv', 'author': 'mike_pants', 'body': 'Stay classy, police.', 'score': 1, 'saved': False, 'number_of_replies': 1, 'created_utc': '2021-03-15 00:42:58', 'sentiment': [0.1, ' Positive']}, {'id': 'gqypr9z', 'author': 'Titsoritdidnthappen2', 'body': 'Only thing police hate more than black people is being inconvenienced.', 'score': 1, 'saved': False, 'number_of_replies': 1, 'created_utc': '2021-03-15 00:39:39', 'sentiment': [-0.11666666666666667, ' Negative']}]}

#Create empty lists
author = []
body = []
id = []
number_of_replies = []
saved = []
score = []
sentiment = []

#Parse through json file and append lists
for x in range(len(comment_dict['data'])):
    author.append(comment_dict['data'][x]['author'])
    body.append(comment_dict['data'][x]["body"])
    id.append(comment_dict['data'][x]['id'])
    number_of_replies.append(comment_dict['data'][x]["number_of_replies"])
    saved.append(comment_dict['data'][x]['saved'])
    score.append(comment_dict['data'][x]["score"])
    sentiment.append(comment_dict['data'][x]["sentiment"])

#Create and clean dataframe
comment_df = pd.DataFrame(zip(author,body,id,number_of_replies,saved,score,sentiment))
comment_df = comment_df.rename(columns={0: "Author", 1: "Comment", 2: "ID", 3: "Number of Replies", 4: "Saved", 5:"Score", 6:"Sentiment"})
comment_df['Sentiment'] = pd.DataFrame(comment_df['Sentiment'].values.tolist())
comment_df.head()

bins = [-1,-.75,-.5,-.25, 0,.25,.5,.75, 1]
comment_df['Sentiment Range'] = pd.cut(comment_df['Sentiment'], bins)
comment_df.head()

comment_sentiment_prebar = comment_df.groupby("Sentiment Range")["ID"].count()
comment_sentiment_bar = comment_sentiment_prebar.reset_index()
comment_sentiment_bar['Sentiment Range'] = comment_sentiment_bar['Sentiment Range'].astype(str)

plt.bar(comment_sentiment_bar["Sentiment Range"],comment_sentiment_bar["ID"])
plt.title("Overall Sentiment")
plt.xlabel("Sentiment Range")
plt.ylabel("Count")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("Graphs/overall_sentiment.png")
plt.show()