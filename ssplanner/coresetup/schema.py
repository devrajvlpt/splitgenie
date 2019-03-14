# app level Schema
# This is based on Graphene Django Using Relay
# Doc https://docs.graphene-python.org/projects/django/en/latest/tutorial-relay/

import graphene

from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.rest_framework.mutation import SerializerMutation
from coresetup.models import (
    Topic, 
    SplitAmountLedger,
    Contact
)

from coresetup.serialiser import (
    TopicSerializer,
    SplitLedgerSerializer
)


class TopicModelMutation(SerializerMutation):

    """Summary
    """
    class Meta:

        """Summary
        
        Attributes:
            lookup_field (str): Description
            model_operations (list): Description
            serializer_class (TYPE): Description
        """
        
        serializer_class = TopicSerializer
        model_operations = ['create', 'update', 'delete']
        lookup_field = 'id'

class SplitLedgerMutation(SerializerMutation):

    """Summary
    """
    class Meta:

        """Summary
        
        Attributes:
            lookup_field (str): Description
            model_operations (list): Description
            serializer_class (TYPE): Description
        """
        serializer_class = SplitLedgerSerializer
        model_operations = ['create', 'update', 'delete']
        lookup_field = 'id'

class ContactNode(DjangoObjectType):

    """Summary
    """
    class Meta:
        model = Contact
        filter_fields = ['mobile_number', 'last_login']        
        interfaces = (relay.Node, )

class TopicNode(DjangoObjectType):

    """Schema for Topic Model
    """

    class Meta:

        """Meta Information
        
        Attributes:
            filter_fields (list): Description
            interfaces (TYPE): Description
            model (TYPE): Description
        """

        model = Topic
        filter_fields = ['id', 'total_amount', 'created_at', 'created_by']
        interfaces = (relay.Node, )

    @classmethod
    def get_node(cls, id, info):
        """Summary
        
        Args:
            id (TYPE): Description
            info (TYPE): Description
        """        
        try:
            topic = cls._meta.model.objects.get(id=id)
        except cls._meta.model.DoesNotExist:
            raise None
        if info.context.user == topic.created_by:
            return topic
        return None

class SplitAmountLedgerNode(DjangoObjectType):
    """
    docstring here
        :param DjangoObjectType: 
    """
    

    class Meta:

        """Summary
        
        Attributes:
            filter_fields (list): Description
            interfaces (TYPE): Description
            model (TYPE): Description
        """

        model = SplitAmountLedger
        filter_fields = ['updated_at', 'created_at']
        interfaces = (relay.Node, )

class Query(object):
    contact_node = relay.Node.Field(ContactNode)
    all_contact = DjangoFilterConnectionField(ContactNode)    

    node_topic = relay.Node.Field(TopicNode)
    all_topic = DjangoFilterConnectionField(TopicNode)

    sa_ledger = relay.Node.Field(SplitAmountLedgerNode)
    all_sa_ledger = DjangoFilterConnectionField(SplitAmountLedgerNode)

    def resolve_all_contact(self, info):
        """Summary
        
        Args:
            info (TYPE): Description
        """
        if not info.context.user.is_authenticated():
            return Contact.objects.all()
        else:
            return Contact.objects.filter(mobile_number=context.user)
    
class Mutation(graphene.ObjectType):

    create_topic = TopicModelMutation.Field()
    create_ledger = SplitLedgerMutation.Field()
    