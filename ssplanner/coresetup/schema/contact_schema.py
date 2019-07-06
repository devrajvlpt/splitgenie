# app level Schema
# This is based on Graphene Django Using Relay
# Doc https://docs.graphene-python.org/projects/django/en/latest/tutorial-relay/

import graphene
from graphene import relay, ObjectType
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from coresetup.models.contact_model import Contact

class ContactType(DjangoObjectType):

    """Summary
    """

    class Meta:

        """Summary
        
        Attributes:
            model (TYPE): Description
        """

        model = Contact


class CreateContact(graphene.Mutation):

    """Summary
    
    Attributes:
        contact (TYPE): Description
    """

    contact = graphene.Field(ContactType)

    class Arguments:

        """Summary
        
        Attributes:
            email (TYPE): Description
            mobile_number (TYPE): Description
            password (TYPE): Description
            username (TYPE): Description
        """

        mobile_number = graphene.Int(required=True)
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, mobile_number, username, password, email):
        """Summary
        
        Args:
            info (TYPE): Description
            mobile_number (TYPE): Description
            username (TYPE): Description
            password (TYPE): Description
            email (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        contact = Contact(
            mobile_number=mobile_number,
            username=username,
            email=email,
        )
        contact.set_password(password)
        contact.save()

        return CreateContact(contact=contact)


class Query(graphene.ObjectType):

    """Summary
    
    Attributes:
        auth (TYPE): Description
        contacts (TYPE): Description
    """

    contacts = graphene.List(ContactType)
    auth = graphene.Field(ContactType)

    def resolve_contacts(self, info):
        """Summary
        
        Args:
            info (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        return Contact.objects.all()

    def resolve_auth(self, info):
        """Summary
        
        Args:
            info (TYPE): Description            
        """
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        return user


class Mutation(graphene.ObjectType):

    """Summary
    
    Attributes:
        create_contact (TYPE): Description
    """

    create_contact = CreateContact.Field()
