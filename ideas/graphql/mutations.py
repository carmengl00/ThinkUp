from uuid import UUID
import strawberry

from strawberry.types import Info
from base.decorators import login_required
from ideas.graphql.types import IdeaType
from ideas.models import Notification, Idea
from users.models import CustomUser, Follows
from ideas.graphql.types import VisibilityEnum


@strawberry.type
class IdeasMutation:
    @strawberry.field
    @login_required
    def create_idea(self, text: str, visibility: VisibilityEnum, info: Info) -> IdeaType:
        user = info.context.request.user
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
    @login_required
    def update_visibility_idea(self, id: UUID, visibility: VisibilityEnum, info: Info) -> IdeaType:
        user = info.context.request.user
        idea = Idea.objects.get(id = id, user = user)
        idea.visibility = visibility
        idea.save()
        return idea


    @strawberry.field
    @login_required
    def delete_idea(self, id: UUID, info: Info) -> bool:
        user = info.context.request.user
        idea = Idea.objects.get(id = id, user = user)
        idea.delete()
        return True