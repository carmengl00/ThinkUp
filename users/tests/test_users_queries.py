import json

import pytest
from mixer.backend.django import mixer
from base.factory_test_case import TestBase

USERS_ITEMS = """"
    pageInfo {
        page
        pageSize
        totalResults
    }
    edges {
        node {
            uuid
            username
            email
            firstName
            lastName
        }
    }"""


@pytest.mark.django_db
class TestUsersQueries(TestBase):
    def test_users_query(self):
        mixer.cycle(5).blend("users.CustomUser")

        response = self.post(
            query = USERS_ITEMS,
            user = self.user,
            variables={"input": {"page": 1, "pageSize": 5}}
        )

        data = json.loads(response.content.decode())
        assert len(data["data"]["users"]["edges"]) == 5