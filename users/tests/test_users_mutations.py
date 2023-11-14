import json
from django.test import RequestFactory, TestCase
import pytest
from core.schema import schema
from users.models import CustomUser, FollowRequest, Follows
from mixer.backend.django import mixer
from strawberry.django.views import GraphQLView

LOGIN = """
mutation login ($input: LoginInput!) {
    login(input: $input) {
        user{
            id
            email
        }
        token
        refreshToken
    }
}
"""

CHANGE_PASSWORD = """
mutation changePassword ($input: ChangePasswordInput!) {
    changePassword(input: $input){
        id
    }
}
"""

FOLLOW_REQUEST = """
mutation followRequest ($required_username: String!) {
    followRequest(requiredUsername: $required_username){
        id
        requester{
            id
        }
        required{
            id
        }
    }
}
"""

APPROVE_FOLLOW_REQUEST = """
mutation approveFollowRequest ($id: UUID!) {
    approveFollowRequest(id: $id){
        id
        follower{
            id
        }
        followed{
            id
        }
    }
}
"""

REJECT_FOLLOW_REQUEST = """
mutation rejectFollowRequest ($id: UUID!) {
    rejectFollowRequest(id: $id)
}
"""

UNFOLLOW = """
mutation unfollow ($username: String!) {
    unfollow(username: $username)
}
"""

DELETE_FOLLOWER = """
mutation deleteFollower ($username: String!) {
    deleteFollower(username: $username)
}
"""

@pytest.mark.django_db()
class TestUserSchema(TestCase):
    CORRECT_EMAIL = "test@test.com"
    CORRECT_USERNAME = "test"
    CORRECT_PASSWORD = "q&YsAp-Y8)KYd.H^"

    def setUp(self):
        self.request_factory = RequestFactory()
        self.user = mixer.blend(CustomUser, email="user@test.com")
        self.user.set_password(self.CORRECT_PASSWORD)
        self.user.save()

    def test_login(self):
        request = self.request_factory.post(
            "/graphql/",
            {
                "query": LOGIN,
                "variables": {
                    "input": {
                        "email": "user@test.com",
                        "password": self.CORRECT_PASSWORD,
                    }
                },
            },
            content_type="application/json",
        )
        response = GraphQLView.as_view(schema=schema)(request)
        data = json.loads(response.content.decode())
        login = data.get("data").get("login")
        assert login.get("user").get("id") == str(self.user.id)
        assert login.get("user").get("email") == "user@test.com"

    def test_change_password(self):
        request = self.request_factory.post(
            "/graphql/",
            {
                "query": CHANGE_PASSWORD,
                "variables": {
                    "input": {
                        "currentPassword": self.CORRECT_PASSWORD,
                        "password": self.CORRECT_PASSWORD,
                        "repeatPassword": None,
                    }
                },
            },
            content_type="application/json",
        )
        request.user = self.user
        response = GraphQLView.as_view(schema=schema)(request)
        data = json.loads(response.content.decode())
        
        change_password = data.get("data").get("changePassword")
        assert change_password.get("id") == str(self.user.id)

    def test_follow_request(self):
        requester = self.user
        required = mixer.blend(CustomUser, username = "required")
        request = self.request_factory.post(
            "/graphql/",
            {
                "query": FOLLOW_REQUEST,
                "variables": {
                    "required_username": required.username,
                },
            },
            content_type="application/json",
        )
        request.user = requester
        response = GraphQLView.as_view(schema=schema)(request)
        data = json.loads(response.content.decode())
        follow_request = data.get("data")
        assert len(follow_request) == 1
        assert follow_request.get("followRequest").get("requester").get("id") == str(requester.id)

    def test_approve_follow_request(self):
        requester = mixer.blend(CustomUser, username = "requester")
        required = self.user
        follow_request = mixer.blend(FollowRequest, requester = requester, required = required)
        request = self.request_factory.post(
            "/graphql/",
            {
                "query": APPROVE_FOLLOW_REQUEST,
                "variables": {
                    "id": str(follow_request.id),
                },
            },
            content_type="application/json",
        )
        request.user = required
        response = GraphQLView.as_view(schema=schema)(request)
        data = json.loads(response.content.decode())
        approve_follow_request = data.get("data")
        assert len(approve_follow_request) == 1
        assert approve_follow_request.get("approveFollowRequest").get("follower").get("id") == str(requester.id)
        assert approve_follow_request.get("approveFollowRequest").get("followed").get("id") == str(required.id)

    def test_reject_follow_request(self):
        requester = mixer.blend(CustomUser, username = "requester")
        required = self.user
        follow_request = mixer.blend(FollowRequest, requester = requester, required = required)
        request = self.request_factory.post(
            "/graphql/",
            {
                "query": REJECT_FOLLOW_REQUEST,
                "variables": {
                    "id": str(follow_request.id),
                },
            },
            content_type="application/json",
        )
        request.user = required
        response = GraphQLView.as_view(schema=schema)(request)
        data = json.loads(response.content.decode())
        reject_follow_request = data.get("data")
        assert len(reject_follow_request) == 1
        assert reject_follow_request.get("rejectFollowRequest") == True

    def test_unfollow(self):
        follower = self.user
        followed = mixer.blend(CustomUser, username = "follower")
        mixer.blend(Follows, follower = follower, followed = followed)
        request = self.request_factory.post(
            "/graphql/",
            {
                "query": UNFOLLOW,
                "variables": {
                    "username": followed.username,
                },
            },
            content_type="application/json",
        )
        request.user = follower
        response = GraphQLView.as_view(schema=schema)(request)
        data = json.loads(response.content.decode())
        unfollow = data.get("data")
        assert len(unfollow) == 1
        assert unfollow.get("unfollow") == True

    def test_delete_follower(self):
        follower = mixer.blend(CustomUser, username = "follower")
        followed = self.user
        mixer.blend(Follows, follower = follower, followed = followed)
        request = self.request_factory.post(
            "/graphql/",
            {
                "query": DELETE_FOLLOWER,
                "variables": {
                    "username": follower.username,
                },
            },
            content_type="application/json",
        )
        request.user = followed
        response = GraphQLView.as_view(schema=schema)(request)
        data = json.loads(response.content.decode())
        delete_follower = data.get("data")
        assert len(delete_follower) == 1
        assert delete_follower.get("deleteFollower") == True