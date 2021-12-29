import numpy as np
import pandas as pd
from logzero import logger

import settings


def fill_na(df: pd.DataFrame, last_prop_idx, replacement_value=0):
    df.iloc[:, last_prop_idx + 1 :] = df.iloc[:, last_prop_idx + 1 :].fillna(
        replacement_value
    )
    return df


def cols_to_int64(df: pd.DataFrame):
    logger.debug('Converting non-decimal columns to Int64Dtype')
    for column in df.columns:
        if df[column].dtype == 'float64':
            if all((df[column] / np.floor(df[column])).dropna() == 1):
                df[column] = df[column].astype(pd.Int64Dtype())
    return df


def fix_twitter_col(df: pd.DataFrame, twitter_base_url, twitter_col='twitter'):
    logger.debug('Adding url to Twitter nicknames')
    df[twitter_col] = df[twitter_col].str.replace('@', twitter_base_url)
    return df


def sort_stats_cols(df: pd.DataFrame, last_prop_idx):
    logger.debug('Sorting player stats columns')
    sorted_columns = list(df.columns[: last_prop_idx + 1]) + sorted(
        df.columns[last_prop_idx + 1 :]
    )
    return df[sorted_columns]


def wrangle_dataframe(
    df: pd.DataFrame,
    twitter_base_url=settings.TWITTER_BASE_URL,
    player_props_selection=settings.PLAYER_PROPS_SELECTION,
):
    last_prop_idx = df.columns.get_loc(list(player_props_selection.keys())[-1])
    df = cols_to_int64(df)
    df = fix_twitter_col(df, twitter_base_url)
    df = sort_stats_cols(df, last_prop_idx)
    return df
