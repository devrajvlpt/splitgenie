# app level Schema
# This is based on Graphene Django Using Relay
# Doc https://docs.graphene-python.org/projects/django/en/latest/tutorial-relay/

import graphene
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from coresetup.models.owe_model import OweModel 
from coresetup.models.contact_model import Contact
from django_graphene_permissions import PermissionDjangoObjectType
from django_graphene_permissions.permissions import IsAuthenticated
from django_graphene_permissions import permissions_checker

class OweType(PermissionDjangoObjectType):

    """Summary
    """

    class Meta:

        """Summary
        
        Attributes:
            model (TYPE): Description
        """

        model = OweModel


class CreateOwe(graphene.Mutation):

    """Summary
    
    Attributes:
        owe (TYPE): Description
    """

    owe = graphene.Field(OweType)

    class Arguments:

        """Summary
        
        Attributes:
            created_by (TYPE): Description
            owed_amount (TYPE): Description            
            owed_on (TYPE): Description
        """

        owed_amount = graphene.Int(required=True)
        owed_on = graphene.String(required=True)
        created_by = graphene.Int(required=True)
        updated_by = graphene.Int(required=True)

    @permissions_checker([IsAuthenticated])
    def mutate(self, info, owed_amount, owed_on, created_by, updated_by):
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

        owe = OweModel(
            owed_amount=owed_amount,
            owed_on=owed_on,
            created_by=contact_update,
            updated_by=contact_update
        )        
        owe.save()
        return CreateOwe(owe=owe)


class Query(graphene.ObjectType):

    """Summary
    
    Attributes:
        auth (TYPE): Description
        contacts (TYPE): Description
    """

    owes = graphene.List(OweType)

    @permissions_checker([IsAuthenticated])
    def resolve_owes(self, info):
        """Summary
        
        Args:
            info (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        return OweModel.objects.all()


class Mutation(graphene.ObjectType):

    """Summary
    
    Attributes:
        create_contact (TYPE): Description
    """

    create_owe = CreateOwe.Field()
