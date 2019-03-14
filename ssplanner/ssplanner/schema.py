# Project level Schema
import graphene
import coresetup.schema

class Query(coresetup.schema.Query, graphene.ObjectType):
	"""
	docstring here
		:param coresetup.schema.Query: 
		:param graphene.ObjectType: 
	"""
	pass

class Mutation(coresetup.schema.Mutation, graphene.ObjectType):

    """Summary
    """
    pass




schema = graphene.Schema(query=Query, mutation=Mutation)