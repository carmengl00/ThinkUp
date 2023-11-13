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
        mixer.blend(CustomUser, username = "user1")
        mixer.blend(CustomUser, username = "user2")
        mixer.blend(CustomUser, username = "user3")

        response = self.post(query=USERS_ITEMS, user=self.user)

        data = json.loads(response.content.decode())
        users = data.get("data").get("users")
        assert len(users) == 4

        assert users[0].get("username") == "user3"
        assert users[1].get("username") == "user2"
        assert users[2].get("username") == "user1"


    def test_my_follow_request_query(self):
        requester1 = mixer.blend(CustomUser, username = "requester1")
        required = self.user
        mixer.blend(FollowRequest, requester=requester1, required=required)

        requester2 = mixer.blend(CustomUser, username = "requester2")
        mixer.blend(FollowRequest, requester=requester2, required=required)

        response = self.post(query=MY_FOLLOW_REQUEST_QUERY, user=self.user)

        data = json.loads(response.content.decode())
        myFollowRequest = data.get("data").get("myFollowRequest")
        assert len(myFollowRequest) == 2

        assert myFollowRequest[0].get("requester").get("username") == requester1.username
        assert myFollowRequest[1].get("requester").get("username") == requester2.username

    def test_my_followers_query(self):
        follower1 = mixer.blend(CustomUser, username = "follower1")
        mixer.blend(Follows, followed=self.user, follower=follower1)

        follower2 = mixer.blend(CustomUser, username = "follower2")
        mixer.blend(Follows, followed=self.user, follower=follower2)

        response = self.post(query=MY_FOLLOWERS_QUERY, user=self.user)

        data = json.loads(response.content.decode())
        myFollowers = data.get("data").get("myFollowers")
        assert len(myFollowers) == 2

        assert myFollowers[0].get("username") == follower1.username
        assert myFollowers[1].get("username") == follower2.username


    def test_my_followed_query(self):
        followed1 = mixer.blend(CustomUser, username = "followed1")
        mixer.blend(Follows, follower=self.user, followed=followed1)

        followed2 = mixer.blend(CustomUser, username = "followed2")
        mixer.blend(Follows, follower=self.user, followed=followed2)

        response = self.post(query=MY_FOLLOWED_QUERY, user=self.user)

        data = json.loads(response.content.decode())
        myFollowed = data.get("data").get("myFollowed")
        assert len(myFollowed) == 2

        assert myFollowed[0].get("username") == followed1.username
        assert myFollowed[1].get("username") == followed2.username


    def test_search_user_query(self):

        test_user_1 = mixer.blend(CustomUser, username = "test_user")
        test_user_2 = mixer.blend(CustomUser, username = "user_test")
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
        edges = data.get("data").get("searchUser").get("edges")
        assert len(edges) == 2
        assert edges[0].get("username") == test_user_2.username
        assert edges[1].get("username") == test_user_1.username
