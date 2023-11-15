from django.utils.translation import gettext as _
import jwt
from strawberry.extensions import Extension
from base import exceptions

from base.jwt import jwt_decode

from strawberry.extensions.utils import is_introspection_field
from users.models import CustomUser

class AuthenticationMiddleware(Extension):

    def resolve(self, _next, root, info, **args):
        if not root and not is_introspection_field(info):
            token = info.context.request.headers.get('Authorization')
    
            if token:
                token = token.replace("JWT ", "")
                try:
                    payload = jwt_decode(token)
                    user = CustomUser.objects.filter(jwt_token_key = payload["token"], email = payload["email"]).first()
                    
                    if user:
                        info.context.request.user = user
                except jwt.ExpiredSignatureError:
                    raise exceptions.PermissionDenied(_("Signature has expired."))
                except jwt.DecodeError:
                    raise exceptions.PermissionDenied(_("Error decoding signature."))
                except jwt.InvalidTokenError:
                    raise exceptions.PermissionDenied(_("Invalid token."))
        
        return _next(root, info, **args)

