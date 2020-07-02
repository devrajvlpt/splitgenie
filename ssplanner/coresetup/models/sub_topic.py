from django.db import models
from django.conf import settings
from .topic import Topic
from .auditlog import AuditLog


class SubTopic(AuditLog):
    """[summary]

    Args:
        models ([type]): [description]
    """
    sub_topicname = models.CharField(max_length=120, default="Untitled")
    sub_topicamount = models.IntegerField()
    sub_topicdescription = models.CharField(max_length=240, default="Untitled")
    topic_id = models.ForeignKey(
            Topic,
            related_name='sub_topic_topic',
            on_delete=models.CASCADE,
            blank=True
    )
    created_by = models.ForeignKey(
                            settings.AUTH_USER_MODEL,
                            related_name='subtopic_created',
                            on_delete=models.CASCADE,
                        )
    updated_by = models.ForeignKey(
                            settings.AUTH_USER_MODEL,
                            related_name='subtopic_updated',
                            on_delete=models.CASCADE
                        )    
