from datetime import datetime, timedelta
from functools import wraps
import graphql_jwt
from api.models import UserModel


# works if token was sent in request headers as:
# "Authorization": "JWT token""
def access_required(function):
    """
    Verify if the user is logged on the system.
    """
    @wraps(function)
    def decorated(*args, **kwargs):
        user_token = args[1].context.META.get('HTTP_AUTHORIZATION')

        try:
            kind, token = user_token.split()
        except:
            raise Exception('Invalid authorization data!')

        if kind.lower() != 'jwt':
            raise Exception('Invalid authorization method!')

        validator = graphql_jwt.Verify.Field()
        payload = validator.resolver(None, args[1], token).payload
        username = payload.get('username')
        expiration_time = payload.get('exp', 0)
        now = datetime.now() - timedelta(hours=3)

        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            raise Exception('Invalid validation data!')

        if (now.timestamp() > expiration_time):
            raise Exception('Session expired')

        if user.is_anonymous:
            raise Exception('Not logged in!')

        kwargs['user'] = user
        return function(*args, **kwargs)
    return decorated
