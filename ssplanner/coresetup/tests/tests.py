# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from coresetup.models.models import (
        SubTopic,
        Topic,
        Contact
    )

# Create your tests here.
class SubTopicTestCase(TestCase):
    def setUp(self):
        topic = Topic.objects.filter(id=4).first()
        contact = Contact.objects.filter(id=4).first()
        SubTopic.objects.create(
            sub_topicname="kdmarriage",
            sub_topicamount="5000",
            sub_topicdescription="triptotirunelveli",
            topic_id=topic,
            created_by=contact,
            updated_by=contact,
        )
    
    def test_subtopics_create(self):
        created = self.setUp()
        self.assertTrue(isinstance(create, SubTopic))
        self.assertEqual(created.__unicode(), created.sub_topicname)