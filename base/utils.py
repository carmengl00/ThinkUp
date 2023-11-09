from strawberry.types import Info
from typing import Any
from rest_framework.request import Request
from graphql import GraphQLResolveInfo
from strawberry.django.context import StrawberryDjangoContext
from django.http import HttpRequest

from typing import Any

from django.http import HttpRequest
from graphql import GraphQLResolveInfo
from strawberry.django.context import StrawberryDjangoContext
from strawberry.types import Info

def get_context(info: HttpRequest | Request | Info[Any, Any] | GraphQLResolveInfo) -> Any:
    if hasattr(info, "context"):
        ctx = getattr(info, "context")  # noqa: B009
        if isinstance(ctx, StrawberryDjangoContext):
            return ctx.request
        return ctx
    return info
