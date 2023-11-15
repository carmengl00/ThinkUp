import json

import pytest
from mixer.backend.django import mixer
from base.factory_test_case import TestBase
from ideas.models import Idea, Notification, VisibilityType
from users.models import CustomUser, Follows

IDEAS_ITEMS = """
    query($pagination: PaginationInput!) {
        myIdeas(pagination: $pagination) {
            pageInfo {
                page
			    pages
            }
            edges {
                id
                text
                createdAt
                updatedAt
                visibility
                user{
                    username
                }
            }
        }
    }
"""
IDEAS_USER = """
    query($id: UUID!, $pagination: PaginationInput!) {
        ideasUser(id: $id, pagination: $pagination) {
            pageInfo {
                page
                pages
            }
            edges {
                id
                text
                createdAt
                updatedAt
                visibility
                user{
                    username
                }
            }
        }
    }
"""
TIMELINE = """
    query($pagination: PaginationInput!) {
        timeline(pagination: $pagination) {
            pageInfo {
                page
			    pages
            }
            edges {
                id
                text
                createdAt
                updatedAt
                visibility
                user{
                    username
                }
            }
        }
    }
"""

NOTIFICATIONS = """
    query($pagination: PaginationInput!) {
        myNotifications(pagination: $pagination) {
            pageInfo {
                page
                pages
            }
            edges {
                id
                idea{
                    text
                }
                user{
                    username
                }
            }
        }
    }
"""

@pytest.mark.django_db
class TestIdeasQueries(TestBase):
    def test_my_ideas(self):
        mixer.blend(Idea, user=self.user, text="idea 1")
        mixer.blend(Idea, user=self.user, text="idea 2")
        mixer.blend(Idea, user=self.user, text="idea 3")

        variables = {
            "pagination": {
                "page": 1,
                "pageSize": 5,
            },
        }

        response = self.post(
            query=IDEAS_ITEMS,
            user=self.user,
            variables= variables
        )

        data = json.loads(response.content.decode())
        ideas = data.get("data").get("myIdeas").get("edges")
        assert len(ideas) == 3

        assert ideas[0].get("text") == "idea 3"
        assert ideas[1].get("text") == "idea 2"
        assert ideas[2].get("text") == "idea 1"

    def test_my_ideas_unauthenticated(self):
        mixer.blend(Idea, user=self.user, text="idea 1")
        mixer.blend(Idea, user=self.user, text="idea 2")
        mixer.blend(Idea, user=self.user, text="idea 3")

        variables = {
            "pagination": {
                "page": 1,
                "pageSize": 5,
            },
        }

        response = self.post(
            query=IDEAS_ITEMS,
            variables= variables
        )

        data = json.loads(response.content.decode())
        assert data.get("data") == None

    def test_ideas_user(self):
        user2 = mixer.blend(CustomUser, username = "user2")
        mixer.blend(Idea, user=user2, text="idea 1")
        mixer.blend(Idea, user=user2, text="idea 2")
        mixer.blend(Idea, user=user2, text="idea 3")

        variables = {
            "id": str(user2.id),
            "pagination": {
                "page": 1,
                "pageSize": 5,
            },
        }

        response = self.post(
            query=IDEAS_USER,
            user=self.user,
            variables= variables
        )

        data = json.loads(response.content.decode())
        ideas = data.get("data").get("ideasUser").get("edges")
        assert len(ideas) == 3

        assert ideas[0].get("text") == "idea 3"
        assert ideas[1].get("text") == "idea 2"
        assert ideas[2].get("text") == "idea 1"

    def test_ideas_without_id(self):
        user2 = mixer.blend(CustomUser, username = "user2")
        mixer.blend(Idea, user=user2, text="idea 1")
        mixer.blend(Idea, user=user2, text="idea 2")
        mixer.blend(Idea, user=user2, text="idea 3")

        variables = {
            "pagination": {
                "page": 1,
                "pageSize": 5,
            },
        }

        response = self.post(
            query=IDEAS_USER,
            user=self.user,
            variables= variables
        )

        data = json.loads(response.content.decode())
        assert data.get("data") == None
        assert data.get("errors")[0].get("message") == "Variable '$id' of required type 'UUID!' was not provided."

    def test_timeline(self):
        user2 = mixer.blend(CustomUser, username = "user2")
        mixer.blend(Idea, user=user2, text="idea 1", visibility = VisibilityType.PUBLIC)
        mixer.blend(Idea, user=user2, text="idea 2", visibility = VisibilityType.PROTECTED)
        mixer.blend(Idea, user=user2, text="idea 3", visibility = VisibilityType.PRIVATE)
        mixer.blend(Idea, user=self.user, text="idea 4")
        mixer.blend(Idea, user=self.user, text="idea 5")

        mixer.blend(Follows, follower=self.user, followed=user2)

        variables = {
            "pagination": {
                "page": 1,
                "pageSize": 5,
            },
        }

        response = self.post(
            query=TIMELINE,
            user=self.user,
            variables= variables
        )

        data = json.loads(response.content.decode())
        ideas = data.get("data").get("timeline").get("edges")
        assert len(ideas) == 4

        assert ideas[0].get("text") == "idea 5"
        assert ideas[1].get("text") == "idea 4"
        assert ideas[2].get("text") == "idea 2"
        assert ideas[3].get("text") == "idea 1"

    def test_timeline_unauthenticated(self):
        user2 = mixer.blend(CustomUser, username = "user2")
        mixer.blend(Idea, user=user2, text="idea 1", visibility = VisibilityType.PUBLIC)
        mixer.blend(Idea, user=user2, text="idea 2", visibility = VisibilityType.PROTECTED)
        mixer.blend(Idea, user=user2, text="idea 3", visibility = VisibilityType.PRIVATE)
        mixer.blend(Idea, user=self.user, text="idea 4")
        mixer.blend(Idea, user=self.user, text="idea 5")

        mixer.blend(Follows, follower=self.user, followed=user2)

        variables = {
            "pagination": {
                "page": 1,
                "pageSize": 5,
            },
        }

        response = self.post(
            query=TIMELINE,
            variables= variables
        )

        data = json.loads(response.content.decode())
        assert data.get("data") == None

    def test_my_notifications(self):
        mixer.blend(Notification, user=self.user, idea=mixer.blend(Idea, user=self.user, text="idea 1"))
        mixer.blend(Notification, user=self.user, idea=mixer.blend(Idea, user=self.user, text="idea 2"))

        variables = {
            "pagination": {
                "page": 1,
                "pageSize": 5,
            },
        }

        response = self.post(
            query=NOTIFICATIONS,
            user=self.user,
            variables= variables
        )

        data = json.loads(response.content.decode())
        ideas = data.get("data").get("myNotifications").get("edges")
        assert len(ideas) == 2

        assert ideas[0].get("idea").get("text") == "idea 1"
        assert ideas[1].get("idea").get("text") == "idea 2"

    def test_my_notifications_unauthenticated(self):
        mixer.blend(Notification, user=self.user, idea=mixer.blend(Idea, user=self.user, text="idea 1"))
        mixer.blend(Notification, user=self.user, idea=mixer.blend(Idea, user=self.user, text="idea 2"))

        variables = {
            "pagination": {
                "page": 1,
                "pageSize": 5,
            },
        }

        response = self.post(
            query=NOTIFICATIONS,
            variables= variables
        )

        data = json.loads(response.content.decode())
        assert data.get("data") == None
        