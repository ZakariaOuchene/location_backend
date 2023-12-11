from urllib.parse import parse_qs
from channels.db import database_sync_to_async

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


class TokenAuthentication:
    

    model = None

    def get_model(self):
        if self.model is not None:
            return self.model
        # print('self model ', self.model)
        from rest_framework.authtoken.models import Token
        # print('Token ', Token)

        return Token


    def authenticate_credentials(self, key):
        model = self.get_model()
        print("moddddddel",model)
        tck = model.objects.select_related("user")
        
        user = User.objects.get(username=user) 
        tokens = model.objects.filter(user=user)
        print("tokeeeeeeeensnnss",tokens)



        try:
             token = model.objects.select_related("user").filter(key=key).first()
             if token is None:
                print('Token not found for key:', key)
                raise AuthenticationFailed(_("Invalid token"))
        except model.DoesNotExist:
                print('Token model does not exist')
                raise AuthenticationFailed(_("Invalid token"))

        if not token.user.is_active:
                raise AuthenticationFailed(_("User inactive or deleted."))


        return token.user


@database_sync_to_async
def get_user(scope):
   
    from django.contrib.auth.models import AnonymousUser

    if "token" not in scope:
        raise ValueError(
            "Cannot find token in scope. You should wrap your consumer in "
            "TokenAuthMiddleware."
        )
    token = scope["token"]
    user = None
    try:
        auth = TokenAuthentication()
        user = auth.authenticate_credentials(token)
    except AuthenticationFailed:
        pass
    return user or AnonymousUser()


class TokenAuthMiddleware:
 
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
       
        query_params = parse_qs(scope["query_string"].decode())
        token = query_params["token"][0]
        print('token',token )

        scope["token"] = token
        
        print('scope["token"]',scope["token"] )
        scope["user"] = await get_user(scope)
        print('usssssssssssssssssssssser',scope["user"] )
        return await self.app(scope, receive, send)