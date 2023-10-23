from gqlauth.core.utils import get_user
from strawberry.types import Info
from users.models import Follows
from ideas.models import Idea, Notification
from typing import List
from django.contrib.auth import get_user_model

# Mutations
def create_idea(text: str, visibility: str, info: Info) -> Idea:
    user = get_user(info)
    idea = Idea.objects.create(text = text, visibility = visibility, user = user)
    followers = Follows.objects.filter(followed = user)
    for f in followers:
        if idea.visibility == 'public' or idea.visibility == 'protected':
            Notification.objects.create(idea = idea, user = f.follower)
    return idea

def update_visibility_idea(id: int, visibility: str, info: Info) -> Idea:
    user = get_user(info)
    idea = Idea.objects.get(id = id, user = user)
    idea.visibility = visibility
    idea.save()
    return idea

def delete_idea(id: int, info: Info) -> bool:
    user = get_user(info)
    idea = Idea.objects.get(id = id, user = user)
    idea.delete()
    return True

# Queries
def my_ideas(info: Info) -> List[Idea]:
    user = get_user(info)
    sorted_list = sorted(Idea.objects.filter(user = user), key = lambda x: x.created_at, reverse = True)
    return sorted_list

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

def timeline(self, info: Info) -> List[Idea]:
    user = get_user(info)
    following = Follows.objects.filter(follower = user)
    my_ideas = Idea.objects.filter(user = user)
    lista = list(my_ideas)
    for f in following:
        lista += self.ideas_user(f.followed.username, info)

    sorted_list = sorted(lista, key = lambda x: x.created_at, reverse = True)
    return sorted_list

def my_notifications(info: Info) -> List[Notification]:
    user = get_user(info)
    return Notification.objects.filter(user = user)
