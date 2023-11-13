import json

import pytest
from mixer.backend.django import mixer
from base.factory_test_case import TestBase
from users.models import CustomUser, FollowRequest, Follows

USERS_ITEMS = """
    query {
        users {
            id
            username
            email
        }
    }
"""

MY_FOLLOW_REQUEST_QUERY = """
    query {
        myFollowRequest {
            id
            requester {
                id
                username
                email
            }
            required {
                id
                username
                email
            }
        }
    }
"""

MY_FOLLOWERS_QUERY = """
    query {
        myFollowers {
            id
            username
            email
        }
    }
"""

MY_FOLLOWED_QUERY = """
    query {
        myFollowed {
            id
            username
            email
        }
    }
"""

SEARCH_USER_QUERY = """
    query($username: String!, $pagination: PaginationInput!) {
        searchUser(username: $username, pagination: $pagination) {
            pageInfo {
                page
			    pages
            }
            edges {
                id
                username
                email
            }
        }
    }
"""

@pytest.mark.django_db
class TestUsersQueries(TestBase):
    def test_users_query(self):
        mixer.cycle(5).blend(CustomUser)

        response = self.post(query=USERS_ITEMS, user=self.user)

        data = json.loads(response.content.decode())
        assert len(data.get("data").get("users")) == 6

    def test_my_follow_request_query(self):
        requester = mixer.blend(CustomUser)
        required = self.user
        mixer.blend(FollowRequest, requester=requester)
        mixer.blend(FollowRequest, required=required)

        response = self.post(query=MY_FOLLOW_REQUEST_QUERY, user=self.user)

        data = json.loads(response.content.decode())
        assert len(data.get("data").get("myFollowRequest")) == 1

    def test_my_followers_query(self):
        follower = mixer.blend(CustomUser)
        mixer.cycle(5).blend(Follows, followed=self.user, follower=follower)

        response = self.post(query=MY_FOLLOWERS_QUERY, user=self.user)

        data = json.loads(response.content.decode())
        assert len(data.get("data").get("myFollowers")) == 5

    def test_my_followed_query(self):
        followed = mixer.blend(CustomUser)
        mixer.cycle(5).blend(Follows, follower=self.user, followed=followed)

        response = self.post(query=MY_FOLLOWED_QUERY, user=self.user)

        data = json.loads(response.content.decode())
        assert len(data.get("data").get("myFollowed")) == 5

    def test_search_user_query(self):

        mixer.blend(CustomUser, username = "test_user")
        mixer.blend(CustomUser, username = "user_test")
        mixer.blend(CustomUser, username = "other_user")
        mixer.blend(CustomUser, username = "other_user_2")
        mixer.blend(CustomUser, username = "user")

        variables = {
            "username": "test",
            "pagination": {
                "page": 1,
                "pageSize": 5,
            },
        }

        response = self.post(
            query=SEARCH_USER_QUERY,
            variables=variables,
            user=self.user,
        )

        data = json.loads(response.content.decode())
        print("DATA", data)
        edges = data.get("data").get("searchUser").get("edges")
        assert len(edges) == 2

        usernames = [edge.get("username") for edge in edges]
        assert "test_user" in usernames
        assert "user_test" in usernames
