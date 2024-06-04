import logging
import os
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from typing import Callable, List, Tuple

import praw
import tweepy
from dotenv import load_dotenv
from metadata import log_metadata
from utils.db import DatabaseConnection

load_dotenv()


@dataclass
class RedditPostData:

    title: str
    score: int
    url: str
    comms_num: int
    created: str
    text: str


@dataclass
class TwitterTweetData:

    text: str


@dataclass
class SocialMediaData:

    id: str
    source: str
    social_data: RedditPostData | TwitterTweetData


class SocialMediaPipeline(ABC):
    @abstractmethod
    def extract(
        self, id: str, num_records: int, client
    ) -> List[SocialMediaData]:
        pass

    @abstractmethod
    def transform(
        self,
        social_data: List[SocialMediaData],
        transform_function: Callable[
            [List[SocialMediaData]], List[SocialMediaData]
        ],
    ) -> List[SocialMediaData]:
        pass

    @abstractmethod
    def load(
        self,
        social_data: List[SocialMediaData],
        db_cursor_context: DatabaseConnection,
    ) -> None:
        pass

    @abstractmethod
    def run(
        self,
        db_cursor_context: DatabaseConnection,
        client,
        transform_function: Callable[
            [List[SocialMediaData]], List[SocialMediaData]
        ],
        id: str,
        num_records: int,
    ):
        pass


def pipeline_factory(source: str) -> Tuple[praw.Reddit | tweepy.Client, SocialMediaPipeline]:
    factory = {
        'reddit': (
            praw.Reddit(
                client_id=os.environ['REDDIT_CLIENT_ID'],
                client_secret=os.environ['REDDIT_CLIENT_SECRET'],
                user_agent=os.environ['REDDIT_USER_AGENT'],
            ),
            RedditETL(),
        ),
        'twitter': (
            tweepy.Client(bearer_token=os.environ['BEARER_TOKEN']),
            TwitterETL(),
        ),
    }
    if source in factory:
        return factory[source]
    else:
        raise ValueError(
            f"source {source} is not supported. Please pass a valid source."
        )
