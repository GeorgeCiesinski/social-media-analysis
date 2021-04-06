"""
Author: Saif Gorges
Date: March 11 2021
"""

# Import dependencies
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from logs.Logger import base_logger

logger = base_logger.getChild(__name__)


class DataTransform:

    @staticmethod
    def create_directory(submission_id):

        # Create the new submission id directory
        Path(f"output/graphs/{submission_id}").mkdir(parents=True, exist_ok=True)

    def create_df(self, submission_id, comments_dict):

        logger.info(f'Generating dataframes for submission: {submission_id}.')

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

        # Extract list of comments from comments_dict
        list_of_comments = comments_dict.get('data')

        # Exit function if list_of_comments is empty
        if list_of_comments is None:
            logger.error('Unable to find comments in comment dict. Aborting data frame creation.')
            return None, None

        # Parse through json file and append lists
        for comment in list_of_comments:
            print(comment)
            author.append(comment['author'])
            body.append(comment['body'])
            created_utc.append(comment['created_utc'])
            id.append(comment['id'])
            number_of_replies.append(comment['number_of_replies'])
            saved.append(comment['saved'])
            score.append(comment['score'])
            sentiment_polarity.append(comment['sentiment']['polarity'])
            sentiment_description.append(comment['sentiment']['sentiment'])

        # Create and clean dataframe
        comment_df = pd.DataFrame(
            zip(author, body, created_utc, id, number_of_replies, saved, score, sentiment_polarity,
                sentiment_description))

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

        logger.info('Successfully generated dataframes.')

        self.create_directory(submission_id)

        return comment_df, sentiment_stats

    @staticmethod
    def overall_sentiment_upvotes(submission_id, sentiment_stats):

        # Creating axes object and defining plot for "Overall Sentiment & Upvotes
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

        # Save Plot
        plt.savefig(f"output/graphs/{submission_id}/overall_sentiment_and_upvotes.png")

    @staticmethod
    def overall_sentiment_replies(submission_id, sentiment_stats):

        # Creating axes object and defining plot
        ax = sentiment_stats.plot(kind='bar', x='Sentiment Range',
                                  y='Total Count', color='Blue',
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

        # Save Plot
        plt.savefig(f"output/graphs/{submission_id}/overall_sentiment_and_replies.png")

    @staticmethod
    def sentiment_timeline(submission_id, comment_df):

        # Create scatterplot for timeline vs sentiment
        ax1 = comment_df.plot.scatter(x='Date', y='Sentiment Polarity', c='Upvotes', colormap="viridis", rot=90)

        # Save Plot
        plt.savefig(f"output/graphs/{submission_id}/sentiment_timeline.png")

    @staticmethod
    def sentiment_pie(submission_id, comment_df):

        # Create pie graph for sentiment distribution
        sentiment_description_df = comment_df.groupby("Sentiment Description").agg(
            total_count=('ID', 'count')
        )

        sentiment_pie = sentiment_description_df.plot.pie(y='total_count', figsize=(5, 5), shadow=True,
                                                          autopct='%1.1f%%')

        # Save Plot
        plt.savefig(f"output/graphs/{submission_id}/sentiment_pie.png")
