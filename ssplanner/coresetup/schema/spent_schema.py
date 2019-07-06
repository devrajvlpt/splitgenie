# app level Schema
# This is based on Graphene Django Using Relay
# Doc https://docs.graphene-python.org/projects/django/en/latest/tutorial-relay/

import graphene
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from coresetup.models.spent_model import SpentModel 
from coresetup.models.contact_model import Contact
from django_graphene_permissions import PermissionDjangoObjectType
from django_graphene_permissions.permissions import IsAuthenticated
from django_graphene_permissions import permissions_checker



class SpentType(PermissionDjangoObjectType):

    """Summary
    """    


    class Meta:

        """Summary
        
        Attributes:
            model (TYPE): Description
        """

        model = SpentModel    



class CreateSpent(graphene.Mutation):

    """Summary
    
    Attributes:
        spent (TYPE): Description
    """

    spent = graphene.Field(SpentType)

    class Arguments:

        """Summary
        
        Attributes:
            created_by (TYPE): Description
            owed_amount (TYPE): Description            
            owed_on (TYPE): Description
        """

        spent_amount = graphene.Int(required=True)
        spent_on = graphene.String(required=True)
        created_by = graphene.Int(required=True)
        updated_by = graphene.Int(required=True)

    @permissions_checker([IsAuthenticated])
    def mutate(self, info, spent_amount, spent_on, created_by, updated_by):
        """Summary
        
        Args:
            info (TYPE): Description
            owed_amount (TYPE): Description
            owed_on (TYPE): Description
            created_by (TYPE): Description
        
        Returns:
            TYPE: Description
        """

        contact_update = Contact.objects.get(mobile_number=created_by)

        if not contact_update:
            raise Exception('Not logged in!')


        spent = SpentModel(
            spent_amount=spent_amount,
            spent_on=spent_on,
            created_by=contact_update,
            updated_by=contact_update
        )        
        spent.save()

        return CreateSpent(spent=spent)


class Query(graphene.ObjectType):

    """Summary
    
    Attributes:
        auth (TYPE): Description
        contacts (TYPE): Description
    """

    spents = graphene.List(SpentType)

    @permissions_checker([IsAuthenticated])
    def resolve_spents(self, info):
        """Summary
        
        Args:
            info (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        return SpentModel.objects.all()


class Mutation(graphene.ObjectType):

    """Summary
    
    Attributes:
        create_contact (TYPE): Description
    """

    create_spent = CreateSpent.Field()
