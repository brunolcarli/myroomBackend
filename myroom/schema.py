import graphene
import graphql_jwt
import api.schema


class Query(api.schema.Query, graphene.ObjectType):
    pass


class Mutation(api.schema.Mutation, graphene.ObjectType):
    validate_user_token = graphql_jwt.Verify.Field()
    refresh_user_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
