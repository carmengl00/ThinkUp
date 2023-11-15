import json

import pytest
from mixer.backend.django import mixer
from base.factory_test_case import TestBase
from core.schema import schema
from ideas.models import Idea, VisibilityType
from users.models import CustomUser

from strawberry.django.views import GraphQLView

CREATE_IDEA = """
    mutation($text: String!, $visibility: VisibilityType!) {
        createIdea(text: $text, visibility: $visibility) {
            id
            text
            visibility
            user{
                username
            }
        }
    }
"""
UPDATE_VISIBILITY_IDEA = """
    mutation($id: UUID!, $visibility: VisibilityType!) {
        updateVisibilityIdea(id: $id, visibility: $visibility) {
            id
            text
            visibility
            user{
                username
            }
        }
    }
"""
DELETE_IDEA = """
    mutation($id: UUID!) {
        deleteIdea(id: $id)
    }
"""

@pytest.mark.django_db
class TestIdeasMutations(TestBase):
    def test_create_idea(self):
        variables = {
            "text": "Idea 1",
            "visibility": "PUBLIC",
        }
        request = self.request_factory.post(
            "/graphql/",
            {
                "query": CREATE_IDEA,
                "variables": variables,
            },
            content_type="application/json",
        )
        request.user = self.user
        response = GraphQLView.as_view(schema=schema)(request)
        data = json.loads(response.content.decode())
        user = CustomUser.objects.get(id=self.user.id)

        idea = data.get("data")
        assert len(idea) == 1
        assert idea.get("createIdea").get("user").get("username") == user.username

    def test_create_idea_without_text(self):
        variables = {
            "visibility": "PUBLIC",
        }
        request = self.request_factory.post(
            "/graphql/",
            {
                "query": CREATE_IDEA,
                "variables": variables,
            },
            content_type="application/json",
        )
        request.user = self.user
        response = GraphQLView.as_view(schema=schema)(request)
        data = json.loads(response.content.decode())
        idea = data.get("data")
        assert idea == None

    def test_update_visibility_idea(self):
        idea = mixer.blend(Idea, user = self.user, text = "idea 1", visibility = VisibilityType.PRIVATE)
        variables = {
            "id": str(idea.id),
            "visibility": "PUBLIC",
        }
        request = self.request_factory.post(
            "/graphql/",
            {
                "query": UPDATE_VISIBILITY_IDEA,
                "variables": variables,
            },
            content_type="application/json",
        )

        request.user = self.user
        response = GraphQLView.as_view(schema=schema)(request)
        data = json.loads(response.content.decode())
        idea = data.get("data")
        assert len(idea) == 1

        user = CustomUser.objects.get(id=self.user.id)
        assert idea.get("updateVisibilityIdea").get("user").get("username") == user.username

    def test_update_incorrect_visibility_idea(self):
        idea = mixer.blend(Idea, user = self.user, text = "idea 1", visibility = VisibilityType.PRIVATE)
        variables = {
            "id": str(idea.id),
            "visibility": "INCORRECT",
        }
        request = self.request_factory.post(
            "/graphql/",
            {
                "query": UPDATE_VISIBILITY_IDEA,
                "variables": variables,
            },
            content_type="application/json",
        )

        request.user = self.user
        response = GraphQLView.as_view(schema=schema)(request)
        data = json.loads(response.content.decode())
        idea = data.get("data")
        assert idea == None

    def test_delete_idea(self):
        idea = mixer.blend(Idea, user = self.user, text = "idea 1", visibility = VisibilityType.PRIVATE)
        variables = {
            "id": str(idea.id),
        }
        request = self.request_factory.post(
            "/graphql/",
            {
                "query": DELETE_IDEA,
                "variables": variables,
            },
            content_type="application/json",
        )

        request.user = self.user
        response = GraphQLView.as_view(schema=schema)(request)
        data = json.loads(response.content.decode())
        idea = data.get("data").get("deleteIdea")
        assert idea == True

    def test_delete_idea_unauthenticated(self):
        idea = mixer.blend(Idea, user = self.user, text = "idea 1", visibility = VisibilityType.PRIVATE)
        variables = {
            "id": str(idea.id),
        }
        request = self.request_factory.post(
            "/graphql/",
            {
                "query": DELETE_IDEA,
                "variables": variables,
            },
            content_type="application/json",
        )

        response = GraphQLView.as_view(schema=schema)(request)
        data = json.loads(response.content.decode())
        idea = data.get("data")
        assert idea == None
