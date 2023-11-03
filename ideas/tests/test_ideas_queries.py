import json

import pytest
from mixer.backend.django import mixer
from base.factory_test_case import TestBase
from unittest.mock import patch
from ideas.models import Idea

IDEAS_ITEMS = """
    pageInfo {
        page
        pageSize
        totalResults
    }
    edges {
        node {
            id
            title
            description
            user {
                uuid
            }
        }
    }"""


@pytest.mark.django_db
class TestIdeasQueries(TestBase):
    @patch("gqlauth.core.middlewares.django_jwt_middleware")
    def test_my_ideas(self, mock):
        mock.return_value=lambda get_response: get_response
        mixer.cycle(5).blend(Idea, user=self.user)

        response = self.post(
            query=IDEAS_ITEMS,
            user=self.user,
            variables={"input": {"page": 1, "pageSize": 5}}
        )

        data = json.loads(response.content.decode())
        assert len(data["data"]["myIdeas"]["edges"]) == 5
        assert data["data"]["myIdeas"]["pageInfo"]["totalResults"] == 5
