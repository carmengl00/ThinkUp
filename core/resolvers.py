from typing import List
from users.models import CustomUser, FollowRequest, Follows
from django.contrib.auth import get_user_model
from gqlauth.models import UserStatus
from ideas.models import Idea
from gqlauth.core.utils import get_user
from strawberry.types import Info

def register_user(username: str, email: str, password: str) -> CustomUser:
    CustomUser = get_user_model()
    user = CustomUser.objects._create_user(username = username, email = email, password = password)

    status: "UserStatus" = getattr(user, "status")
    status.verified = True
    status.save()

    return user

def create_idea(text: str, visibility: str, info: Info) -> Idea:
    user = get_user(info)
    idea = Idea.objects.create(text = text, visibility = visibility, user = user)
    return idea

def update_visibility_idea(id: int, visibility: str, info: Info) -> Idea:
    user = get_user(info)
    idea = Idea.objects.get(id = id, user = user)
    idea.visibility = visibility
    idea.save()
    return idea

def my_ideas(info: Info) -> List[Idea]:
    user = get_user(info)
    return Idea.objects.filter(user = user)

def delete_idea(id: int, info: Info) -> bool:
    user = get_user(info)
    idea = Idea.objects.get(id = id, user = user)
    idea.delete()
    return True

def follow_request(required_username: str, info: Info) -> FollowRequest:
    requester = get_user(info)
    required = get_user_model().objects.get(username = required_username)
    return FollowRequest.objects.create_request(requester = requester, required = required)

def my_follow_request(info: Info) -> List[FollowRequest]:
    user = get_user(info)
    im_requester = FollowRequest.objects.filter(requester = user)
    im_required = FollowRequest.objects.filter(required = user)
    
    lista = list(im_requester) + list(im_required)
    
    return lista

def approve_follow_request(id: int, info: Info) -> Follows:
    user = get_user(info)
    request = FollowRequest.objects.get(id = id, required = user)
    request.delete()
    return Follows.objects.create(follower = request.requester, followed = request.required)

def reject_follow_request(id: int, info: Info) -> bool:
    user = get_user(info)
    request = FollowRequest.objects.get(id = id, required = user)
    request.delete()
    return True

def my_followers(info: Info) -> List[CustomUser]:
    user = get_user(info)
    followers = Follows.objects.filter(followed = user)
    return [f.follower for f in followers]
    
def my_followed(info: Info) -> List[CustomUser]:
    user = get_user(info)
    following = Follows.objects.filter(follower = user)
    return [f.followed for f in following]

def unfollow(username: str, info: Info) -> bool:
    user = get_user(info)
    followed = get_user_model().objects.get(username = username)
    follow = Follows.objects.filter(follower = user, followed = followed)
    if follow.exists():
        follow.delete()
    else:
        raise ValueError('You are not following this user')
    return True

def delete_follower(username: str, info: Info) -> bool:
    user = get_user(info)
    follower = get_user_model().objects.get(username = username)
    follow = Follows.objects.filter(follower = follower, followed = user)
    if follow.exists():
        follow.delete()
    else:
        raise ValueError('This user is not following you')
    return True

def search_user(username: str, info: Info) -> List[CustomUser]:
    user = get_user(info)
    return get_user_model().objects.filter(username__icontains = username).exclude(username = user.username)
    
    
def ideas_user(username: str, info: Info) -> List[Idea]:
    user = get_user(info)
    followed = get_user_model().objects.get(username = username)
    follow = Follows.objects.filter(follower = user, followed = followed)
    protected_ideas = []
    private_ideas = []
    if follow:
        protected_ideas = Idea.objects.filter(user = followed, visibility = 'protected')
    
    if followed == user:
        private_ideas = Idea.objects.filter(user = followed, visibility = 'private')
        protected_ideas = Idea.objects.filter(user = followed, visibility = 'protected')
        
    public_ideas = Idea.objects.filter(user = followed, visibility = 'public')
    lista = list(public_ideas) + list(protected_ideas) + list(private_ideas)
    return lista

def timeline(info: Info):
    user = get_user(info)
    following = Follows.objects.filter(follower = user)
    my_ideas = Idea.objects.filter(user = user)
    lista = list(my_ideas)
    for f in following:
        lista += ideas_user(f.followed.username, info)

    sorted_list = sorted(lista, key = lambda x: x.created_at, reverse = True)
    return sorted_list