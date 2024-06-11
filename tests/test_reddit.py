import json
from datetime import datetime
from typing import List

import pytest
from socialMediaPipeline.social_media_pipeline import RedditPostData, SocialMediaData, pipeline_factory
from socialMediaPipeline.transform import transformation_factory
from socialMediaPipeline.utils.db import db_factory


class TestRedditPipeline:
    """A class to test the RedditPipeline class."""

    @pytest.fixture
    def mock_reddit_data(self) -> List[SocialMediaData]:
        """Function to generate 10 fake Reddit data, of type
        SocialMediaData objects. These tests are hardcoded.

        Returns:
            List[SocialMediaData]: List of SocialMediaData objects that
            replicate what we get from the extract method.
        """
        list_of_reddit_data = []
        for idx, elt in enumerate(
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 8]
        ):
            list_of_reddit_data.append(
                SocialMediaData(
                    id=f"id{str(idx)}",
                    source="reddit",
                    social_data=RedditPostData(
                        title=f"title{str(idx)}",
                        score=idx,
                        url=f"url{str(idx)}",
                        comms_num=elt,
                        created=str(datetime.now())[:19],
                        text=f"text{str(idx)}",
                    ),
                )
            )
        return list_of_reddit_data

    def test_transform(self, mock_reddit_data: List[SocialMediaData]) -> None:
        """Function to test the transform method of the RedditPipeline class.

        Args:
            mock_reddit_data (List[SocialMediaData]): List of SocialMediaData
            objects that replicate what we get from the extract method.
        """
        # Create a RedditPipeline object
        _, reddit_pipeline = pipeline_factory('reddit')
        # Call the transform method on the RedditPipeline object
        # and pass in the mock
        transformed_data = reddit_pipeline.transform(
            mock_reddit_data,
            transformation_factory('sd'),
        )
        # Assert that the transformed data is a list of RedditPostData objects
        assert isinstance(transformed_data, list)
        assert transformed_data[0].social_data.comms_num == 8  # type: ignore
        assert len(transformed_data) == 1

    def test_load(self, mock_reddit_data: List[SocialMediaData]) -> None:
        """Function to test the load method of the RedditPipeline class.

        Args:
            mock_reddit_data (List[SocialMediaData]): List of SocialMediaData
            objects that replicate what we get from the extract method.
        """
        # Create a RedditPipeline object
        _, reddit_pipeline = pipeline_factory('reddit')
        # Call the transform method on the RedditPipeline object
        # and pass in the mock
        transformed_data = reddit_pipeline.transform(
            mock_reddit_data,
            transformation_factory('no_tx'),
        )
        # Call the load method on the RedditPipeline object
        # and pass in the transformed data
        db = db_factory(db_file="data/test.db")
        reddit_pipeline.load(
            transformed_data, db_cursor_context=db.managed_cursor()
        )
        # Read social_posts table from database
        with db.managed_cursor() as cur:
            cur.execute("SELECT * FROM social_posts WHERE source = 'reddit'")
            rows = cur.fetchall()

        # Assert that the length of the rows is the same as the
        # length of the mock
        assert len(rows) == len(transformed_data)
        # Assert that the text of the first element of the rows
        # is the same as the text of the first element of the mock
        assert (
            json.loads(rows[0][2].replace("\'", "\"")).get('text')
            == transformed_data[0].social_data.text
        )
