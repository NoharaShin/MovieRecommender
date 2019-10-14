"""Class from which every other movie recommendation class should inherit from."""
import os
from pathlib import Path

import pandas as pd


APP_PATH = Path(os.path.abspath(__file__)).parent.parent
MOVIES_DATASET = os.path.join(APP_PATH, 'datasets', 'movies.csv')


class Recommender(object):
    """
    Recommender is an abstract class designed to be implemented by other movie recommendation system classes.
    It has a unique member which is the movie dataset loaded as a pandas DataFrame, and defines 2 methods common to any
    inheriting class.
    """
    def __init__(self, dataset_path=None):
        """
        :param dataset_path: Path the to movies dataset CSV file.
        :type dataset_path: str
        """
        if dataset_path is None:
            dataset_path = MOVIES_DATASET

        self.movies_df = pd.read_csv(dataset_path).fillna('')

    def _get_title_from_index(self, index):
        """
        Return the movie title matching the provided index from the `movies_df` DataFrame.
        :param index: Index of the movie for which to get the title from the DataFrame.
        :type index: int
        :return: Title of the movie matching to provided index.
        :rtype: str
        """
        return self.movies_df[self.movies_df.index == index]['title'].values[0]

    def _get_index_from_title(self, title):
        """
        Return the index matching the provided movie title from the `movies_df` DataFrame.
        :param title: Title of the movie for which to get the index from the DataFrame.
        :type title: str
        :return: Index of the movie matching the provided title.
        :rtype: int
        """
        return self.movies_df[self.movies_df.title == title]['index'].values[0]
