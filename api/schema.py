from datetime import datetime
import graphene
import graphql_jwt
from django.conf import settings
from api.models import UserModel, Room, Article, Photo, ThreadModel, ThreadComment
from api.user_auth import access_required


class UserType(graphene.ObjectType):
    id = graphene.ID()
    username = graphene.String()
    avatar = graphene.String()
    full_name = graphene.String()
    date_joined = graphene.Date()
    room = graphene.Field('api.schema.RoomType')


class RoomType(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    description = graphene.String()
    user = graphene.Field(UserType)
    room_picture = graphene.String()
    background_picture = graphene.String()
    default_background_active = graphene.Boolean()
    photos_section_active = graphene.Boolean()
    articles_section_active = graphene.Boolean()
    threads_section_active = graphene.Boolean()
    photos = graphene.List('api.schema.PhotoType')
    articles = graphene.List('api.schema.ArticleType')
    threads = graphene.List('api.schema.ThreadType')

    def resolve_photos(self, info, **kwargs):
        if not self.photos_section_active:
            return []
        return self.photo_set.all()

    def resolve_articles(self, info, **kwargs):
        if not self.articles_section_active:
            return []
        return self.article_set.all()
    
    def resolve_threads(self, info, **kwargs):
        if not self.threads_section_active:
            return []
        return self.threadmodel_set.all()


class ArticleType(graphene.ObjectType):
    id = graphene.ID()
    room = graphene.Field(RoomType)
    author = graphene.Field(UserType)
    title = graphene.String()
    content = graphene.String()
    post_datetime = graphene.DateTime()


class PhotoType(graphene.ObjectType):
    id = graphene.ID()
    room = graphene.Field(RoomType)
    user = graphene.Field(UserType)
    data = graphene.String()
    description = graphene.String()
    public = graphene.Boolean()
    post_datetime = graphene.DateTime()


class ThreadType(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    content = graphene.String()
    creation_datetime = graphene.DateTime()
    author = graphene.Field(UserType)
    room = graphene.Field(RoomType)
    last_comment_datetime = graphene.DateTime()
    public = graphene.Boolean()
    num_comments = graphene.Int()
    comments = graphene.List('api.schema.ThreadCommentType')

    def resolve_comments(self, info, **kwargs):
        return self.threadcomment_set.all()


class ThreadCommentType(graphene.ObjectType):
    id = graphene.ID()
    author = graphene.Field(UserType)
    thread = graphene.Field(ThreadType)
    post_datetime = graphene.DateTime()
    content = graphene.String()


############################
#
# Query
#
############################

class Query:
    version = graphene.String()
    def resolve_version(self, info, **kwargs):
        return settings.VERSION

    users = graphene.List(
        UserType,
        username__icontains=graphene.String(),
        room__name__icontains=graphene.String()
    )
    def resolve_users(self, info, **kwargs):
        return UserModel.objects.filter(**kwargs)

    rooms = graphene.List(
        RoomType,
        name__icontains=graphene.String(),
        user__username__icontains=graphene.String()
    )
    def resolve_rooms(self, info, **kwargs):
        return Room.objects.filter(**kwargs)

    articles = graphene.List(
        ArticleType,
        room_id=graphene.ID(required=True)
    )
    def resolve_articles(self, info, **kwargs):
        return Article.objects.filter(**kwargs)

    photos = graphene.List(
        PhotoType,
        room_id=graphene.ID(required=True)
    )
    def resolve_photos(self, info, **kwargs):
        return Photo.objects.filter(**kwargs)

    threads = graphene.List(
        ThreadType,
        room_id=graphene.ID(required=True),
        name__icontains=graphene.String()
    )
    def resolve_threads(self, info, **kwargs):
        return ThreadModel.objects.filter(**kwargs)

    thread_comments = graphene.List(
        ThreadCommentType,
        thread_id=graphene.ID(required=True)
    )
    def resolve_thread_comments(self, info, **kwargs):
        return ThreadComment.objects.filter(**kwargs)


############################
#
# Mutation
#
############################


class SignUp(graphene.relay.ClientIDMutation):
    user = graphene.Field(UserType)

    class Input:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        full_name = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate_and_get_payload(self, info, **kwargs):

        # Check if username or email already exists
        try:
            UserModel.objects.get(username=kwargs['username'])
        except UserModel.DoesNotExist:
            pass
        else:
            raise Exception('Username already in use')

        try:
            UserModel.objects.get(email=kwargs['email'])
        except UserModel.DoesNotExist:
            pass
        else:
            raise Exception('Email already in use')

        # Create user object
        user = UserModel.objects.create(username=kwargs['username'], email=kwargs['email'], full_name=kwargs['full_name'])
        user.set_password(kwargs['password'])
        user.save()

        # Create standard room for this user
        room = Room.objects.create(name=f'{user.username}{user.id}_room', user=user)
        room.save()

        return SignUp(user)


class SignIn(graphene.relay.ClientIDMutation):
    token = graphene.String()

    class Input:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate_and_get_payload(self, info, **kwargs):
        try:
            user = UserModel.objects.get(
                email=kwargs['email']
            )
        except UserModel.DoesNotExist:
            raise Exception('User not found')

        if not user.check_password(kwargs['password']):
            raise Exception('Invalid password')

        user.last_login = datetime.now()
        user.save()

        session = graphql_jwt.ObtainJSONWebToken.mutate(
            self,
            info,
            username=user.username,
            email=user.email,
            password=kwargs['password']
        )

        return SignIn(session.token)


class CreateArticle(graphene.relay.ClientIDMutation):
    article = graphene.Field(ArticleType)

    class Input:
        title = graphene.String(required=True)
        content = graphene.String(required=True)

    @access_required
    def mutate_and_get_payload(self, info, **kwargs):
        user = kwargs.get('user')
        if not user:
            raise Exception('AUTH ERROR|Invalid anonymous request')

        try:
            Article.objects.get(title=kwargs['title'], author=user, room=user.room)
        except Article.DoesNotExist:
            pass
        else:
            raise Exception('Article title already exists in this room')

        article = Article.objects.create(
            title=kwargs['title'],
            content=kwargs['content'],
            author=user,
            room=user.room
        )
        article.save()

        return CreateArticle(article)


class Mutation:
    sign_up = SignUp.Field()
    sign_in = SignIn.Field()

    create_article = CreateArticle.Field()
