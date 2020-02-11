"""
*****************************************************************************************************
model_utils.feature_eng

This package contains customized utilities for engineering features for Sentiment Analysis models:
    - date_feats (generates date features for model)
    - my_stopwords (dictionary of stopwords for model pre-processing)
    - tb_sentiment (generates sentiment and subjectivity scores for labeling)
    - sentiment_label (generates the labels for sentiment analysis: ['positive','neutral','negative']
    - char_count (counts the number of characters in a text string)
    - apply_func (apply a function to a pandas series (row-wise) and return the resulting DataFrame)
    - drop_high_corr (Drop highly correlated features from a DataFrame)
created: 12/31/19
last updated: 2/11/20
*****************************************************************************************************
"""
import pandas as pd
import numpy as np
from spacy.lang.en import English
import re
from textblob import TextBlob


# load spacy NLP model: nlp
# nlp = spacy.load('en_core_web_md')
nlp = English()


def lemma_nopunc(text):
    """
    This function lemmatizes tokens and removes punctuation from a string based on the spaCy NLP medium model.

    @param text: string to be lemmatized and stripped of punctuation
    @return: returns cleaned string.
    """

    # lemmatize tokens: lemmas
    lemmas = [token.lemma_ for token in nlp(str(text))
              if token.is_alpha and token.lemma_ != '-PRON-']

    # Remove punctuation: no_punc
    no_punc = ' '.join(re.sub(r'[^\w\s]', '', t) for t in lemmas)

    return no_punc


# define stopwords variable: my_stopwords
my_stopwords = lemma_nopunc([
    'a',
    'about',
    'above',
    'after',
    'again',
    'all',
    'also',
    'am',
    'an',
    'and',
    'any',
    'are',
    'as',
    'at',
    'be',
    'because',
    'been',
    'before',
    'being',
    'below',
    'between',
    'both',
    'but',
    'by',
    'can',
    'com',
    'could',
    'did',
    'do',
    'does',
    'doing',
    'down',
    'during',
    'each',
    'else',
    'ever',
    'few',
    'film',
    'films',
    'for',
    'from',
    'further',
    'get',
    'had',
    'has',
    'have',
    'having',
    'he',
    "he'd",
    "he'll",
    "he's",
    'her',
    'here',
    "here's",
    'hers',
    'herself',
    'him',
    'himself',
    'his',
    'how',
    "how's",
    'however',
    'http',
    'i',
    "i'd",
    "i'll",
    "i'm",
    "i've",
    'if',
    'in',
    'into',
    'is',
    'it',
    "it's",
    'its',
    'itself',
    'just',
    "let's",
    'like',
    'me',
    'more',
    'most',
    'movie',
    'movies',
    'my',
    'myself',
    'of',
    'off',
    'on',
    'once',
    'only',
    'or',
    'other',
    'otherwise',
    'ought',
    'our',
    'ours',
    'ourselves',
    'out',
    'over',
    'own',
    'same',
    'shall',
    'she',
    "she'd",
    "she'll",
    "she's",
    'should',
    'since',
    'so',
    'some',
    'such',
    'than',
    'that',
    "that's",
    'the',
    'their',
    'theirs',
    'them',
    'themselves',
    'then',
    'there',
    "there's",
    'these',
    'they',
    "they'd",
    "they'll",
    "they're",
    "they've",
    'this',
    'those',
    'through',
    'to',
    'too',
    'under',
    'until',
    'up',
    'very',
    'was',
    'watch',
    'we',
    "we'd",
    "we'll",
    "we're",
    "we've",
    'were',
    'what',
    "what's",
    'when',
    "when's",
    'where',
    "where's",
    'which',
    'while',
    'who',
    "who's",
    'whom',
    'why',
    "why's",
    'with',
    'would',
    'www',
    'you',
    "you'd",
    "you'll",
    "you're",
    "you've",
    'your',
    'yours',
    'yourself',
    'yourselves'
]).split()


def date_feats(df, date_col):
    """
    This function generates new date features from an existing date Series in a pandas DataFrame.
    It returns the pandas DataFrame passed in by the user with new date features.

    args:
        - df: pandas DataFrame
        - date_col: name of date column used to generate new features
    reqs:
        import pandas as pd
    returns:
        pandas.DataFrame
    """
    # convert df[date_col] to datetime data type: df[date_col]
    df[date_col] = pd.to_datetime(df[date_col])
    # scrape month from df[date_col]: df['month']
    df['month'] = df[date_col].dt.month
    # scrape day from df[date_col]: df['day']
    df['day'] = df[date_col].dt.day
    # scrape dayofweek from df[date_col]: df['dayofweek']
    df['dayofweek'] = df[date_col].dt.dayofweek
    # scrape hour from df[date_col]: df['hour']
    df['hour'] = df[date_col].dt.hour
    # reset index: df
    df = df.reset_index()
    print('Generated Date Features & reset index!')
    print()
    print(df.columns)
    print()
    # return df
    return df


def tb_sentiment(text):
    """
    This function generates sentiment labels from an existing text Series.
    It returns the sentiment and subjectivity scores generated by TextBlob.

    args:
        - text: text to be scored by TextBlob
    reqs:
        from textblob import TextBlob
    returns:
        TextBlob(text).sentiment
    """
    return TextBlob(text).sentiment


def sentiment_label(df, col_for_label, label_col):
    """
    This function generates the labels for sentiment analysis: ['positive','neutral','negative']
    by utilizing a np.where function.
    It returns a DataFrame containing the the new label column.

    np.where logic:
        - if df[col_for_label] >= 0.05, return 'positive'
        - otherwise if df[col_for_label] is greater than -0.05 & less than 0.05, return 'neutral'
        - otherwise if df[col_for_label] <= -0.05, return 'negative'
        - else, return np.nan
    args:
        - df: pandas DataFrame
        - col_for_label: name of column to be used to generate labels
        - label_col: name of column that will hold newly generated labels
        import numpy as np
    returns:
        pandas.DataFrame
    """
    df[label_col] = np.where(
        df[col_for_label] >= 0.05,
        'positive',
        np.where(
            (df[col_for_label] > -0.05) & (df[col_for_label] < 0.05),
            'neutral',
            np.where(
                df[col_for_label] <= -0.05,
                'negative',
                np.nan
            )
        )
    )

    print('Computed labels for Modeling')
    print()
    print(df[label_col].unique())
    print()
    print(df[label_col].value_counts())
    print()
    return df


def char_count(df, text, new_pd_series):
    """
    This function counts the number of characters per row of text in a DataFrame series.
    The function generates a new pandas Series containing the number of characters per row.
    It returns a DataFrame containing the new column.
    params:
        - df: pandas DataFrame
        - text: name of column used to count characters
        - new_pd_series: name of column that will hold newly generated counts
    returns:
        pandas.DataFrame
    """
    df[new_pd_series] = df[text].apply(len)

    print(df[new_pd_series].head())
    print()

    return df


def apply_func(df, pd_series, new_pd_series, func):
    """
    Apply a function to a pandas series (row-wise) and return the resulting DataFrame with the new pandas series,
    containing the applied result.

    @param df:
    @param pd_series:
    @param new_pd_series:
    @param func:
    @return:
    """
    df[new_pd_series] = df[pd_series].apply(func)
    print(df[new_pd_series].head())
    print()
    print(df.columns)
    print()

    return df


def drop_high_corr(df):
    """
    Drop highly correlated features (any feature that has > .79 correlation with another feature) from a DataFrame
    @param df:
    @return:
    """
    # Calculate the correlation matrix and take the absolute value: corr_matrix
    corr_matrix = df.corr().abs()

    # Create a True/False mask and apply it: tri_df
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    tri_df = corr_matrix.mask(mask)

    # List column names of highly correlated features (r > 0.79): to_drop
    to_drop = [c for c in tri_df.columns if any(tri_df[c] > 0.79)]

    # Drop the features in the to_drop list: reduced_df
    reduced_df = df.drop(to_drop, axis=1)

    print("The reduced dataframe has {} columns.".format(reduced_df.shape[1]))

    return reduced_df
