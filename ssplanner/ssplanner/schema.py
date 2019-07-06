# Project level Schema
import graphene
import graphql_jwt
import coresetup.schema

class Query(
		coresetup.schema.contact_schema.Query, 
		coresetup.schema.spent_schema.Query,
		coresetup.schema.owe_schema.Query,
		graphene.ObjectType):
	"""
	docstring here
		:param coresetup.schema.Query: 
		:param graphene.ObjectType: 
	"""
	pass

class Mutation(
		coresetup.schema.contact_schema.Mutation,		
		coresetup.schema.spent_schema.Mutation,
		coresetup.schema.owe_schema.Mutation,
		graphene.ObjectType):

    """Summary
    """
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()




schema = graphene.Schema(query=Query, mutation=Mutation)
