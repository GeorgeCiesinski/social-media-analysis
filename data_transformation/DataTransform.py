"""
Author: Saif Gorges
Date: March 11 2021
"""

# Import dependencies
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import pylab

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
            columns={0: "Author", 1: "Comment", 2: "Datetime", 3: "ID", 4: "Number of Replies", 5: "Saved", 6: "Upvotes",
                     7: "Sentiment Polarity", 8: "Sentiment Description"})
        comment_df['Sentiment Polarity'] = pd.DataFrame(comment_df['Sentiment Polarity'].values.tolist())
        comment_df.head()

        # convert to datetime
        comment_df['Date'] = comment_df['Datetime'].apply(lambda t: t.replace(second=0, minute=0))

        # create bins column
        bins = [-1, -.75, -.5, -.25, 0, .25, .5, .75, 1]
        comment_df['Sentiment Range'] = pd.cut(comment_df['Sentiment Polarity'], bins)

        comment_df.head()

        # Transform dataframe to model stats for sentiment
        sentiment_stats = comment_df.groupby("Sentiment Range").agg(
            id_count=('ID', 'count'),
            score_sum=('Upvotes', 'sum'),
            score_avg=('Upvotes', 'mean'),
            replies_count=('Number of Replies', 'sum'),
            replies_avg_count=('Number of Replies', 'mean'),
        )
        sentiment_stats = sentiment_stats.reset_index()
        sentiment_stats['Sentiment Range'] = sentiment_stats['Sentiment Range'].astype(str)

        # Rename DataFrame
        sentiment_stats = sentiment_stats.rename(
            columns={"id_count": "Total Comments", "score_sum": "Total Upvotes", "score_avg":"Average Upvotes", "replies_count": "Total Replies", "replies_avg_count": "Average Replies"})

        logger.info('Successfully generated dataframes.')

        self.create_directory(submission_id)

        # Create timeline dataframe
        timeline_df = comment_df.groupby("Date").agg(
            id_count=('ID', 'count'),
            score_sum=('Upvotes', 'sum'),
            replies_count=('Number of Replies', 'sum'),
        )
        timeline_df = timeline_df.reset_index()

        # Completion notice
        logger.info('Scrape Complete. See outputs.')

        return comment_df, sentiment_stats, timeline_df

    @staticmethod
    def reply_timeline(submission_id, timeline_df):

        logger.info(f'Plotting reply_timeline for submission_id: {submission_id}.')

        # Creating axes object and defining plot for "Overall Sentiment & Upvotes
        ax = timeline_df.plot(kind='line', x='Date',
                              y='id_count', color='cornflowerblue',
                              linewidth=3, rot=45, label='Total Comments')

        ax2 = timeline_df.plot(kind='line', x='Date',
                               y='score_sum', secondary_y=True,
                               color='coral', linewidth=3, rot=45, label='Total Upvotes',
                               ax=ax)

        # Title of the plot
        plt.title("Total Comments and Upvotes vs Time")

        # Labeling x and y-axis
        ax.set_xlabel('Date - Hour (UTC)', color='black')
        ax.set_ylabel('Total Comments', color="cornflowerblue")
        ax2.set_ylabel('Total Upvotes', color='coral')

        # Save Plot
        plt.tight_layout()
        plt.savefig(f"output/graphs/{submission_id}/reply_timeline.png")

        logger.info('Plotting complete.')

    @staticmethod
    def sentiment_timeline(submission_id, comment_df):

        logger.info(f'Plotting sentiment_timeline for submission_id: {submission_id}.')

        # Create scatterplot for timeline vs sentiment
        ax1 = comment_df.plot.scatter(x='Date', y='Sentiment Polarity', c='Upvotes', colormap="viridis", rot=45, title='Sentiment over Time')
        ax1.set_xlabel('Date - Hour (UTC)', color='black')
        # Save Plot
        plt.tight_layout()
        plt.savefig(f"output/graphs/{submission_id}/sentiment_timeline.png")

        logger.info('Plotting complete.')

    @staticmethod
    def sentiment_pie(submission_id, comment_df):

        logger.info(f'Plotting sentiment_pie for submission_id: {submission_id}.')

        # Create pie graph for sentiment distribution
        sentiment_description_df = comment_df.groupby("Sentiment Description").agg(
            total_count=('ID', 'count')
        )

        sentiment_pie = sentiment_description_df.plot.pie(y='total_count', figsize=(5, 5), shadow=True, title='Sentiment Distribution', colors=["lightcoral","moccasin","lightgreen"], labeldistance=None,
                                                          autopct='%1.1f%%')
        pylab.ylabel('')
        # Save Plot
        plt.tight_layout()
        plt.savefig(f"output/graphs/{submission_id}/sentiment_pie.png")

        logger.info('Plotting complete.')

    @staticmethod
    def total_comments_and_replies(submission_id, sentiment_stats):

        logger.info(f'Plotting total_comments_and_replies for submission_id: {submission_id}.')

        # Creating axes object and defining plot
        sentiment_stats.plot(x="Sentiment Range", y=["Total Comments", "Total Replies"], kind="bar", color=["cornflowerblue","mediumturquoise"], figsize=(9, 8), title="Total Comments and Total Replies vs. Sentiment", rot=45)

        # Save Plot
        plt.tight_layout()
        plt.savefig(f"output/graphs/{submission_id}/total_comments_and_replies.png")

        logger.info('Plotting complete.')

    @staticmethod
    def total_comments_and_upvotes(submission_id, sentiment_stats):

        logger.info(f'Plotting total_comments_and_upvotes for submission_id: {submission_id}.')

        # Creating axes object and defining plot
        sentiment_stats.plot(x="Sentiment Range", y=["Total Comments", "Total Upvotes"], kind="bar", color=["cornflowerblue","coral"], figsize=(9, 8), title="Total Comments and Total Upvotes vs. Sentiment", rot=45)

        # Save Plot
        plt.tight_layout()
        plt.savefig(f"output/graphs/{submission_id}/total_comments_and_upvotes.png")

        logger.info('Plotting complete.')
