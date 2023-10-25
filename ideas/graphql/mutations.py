import strawberry

from gqlauth.core.utils import get_user
from strawberry.types import Info
from ideas.graphql.types import IdeaType
from ideas.models import Notification, Idea
from users.models import CustomUser, Follows
from ideas.graphql.types import VisibilityEnum


@strawberry.type
class IdeasMutation:
    @strawberry.field
    def create_idea(text: str, visibility: VisibilityEnum, info: Info) -> IdeaType:
        user = get_user(info)
        if user and isinstance(user, CustomUser):
            idea = Idea.objects.create(text=text, visibility=visibility, user=user)
            followers = Follows.objects.filter(followed=user)
            for f in followers:
                if visibility in (VisibilityEnum.PUBLIC, VisibilityEnum.PROTECTED):
                    Notification.objects.create(idea=idea, user=f.follower)
            return idea
        else:
            raise Exception("Usuario no válido")


    @strawberry.field
    def update_visibility_idea(id: int, visibility: VisibilityEnum, info: Info) -> IdeaType:
        user = get_user(info)
        idea = Idea.objects.get(id = id, user = user)
        idea.visibility = visibility
        idea.save()
        return idea


    @strawberry.field
    def delete_idea(id: int, info: Info) -> bool:
        user = get_user(info)
        idea = Idea.objects.get(id = id, user = user)
        idea.delete()
        return True