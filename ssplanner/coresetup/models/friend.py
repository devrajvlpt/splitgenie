from django.db import models
from .auditlog import AuditLog
from .contact import Contact


class Friend:
    """[summary]

    Args:
        models ([type]): [description]

    Returns:
        [type]: [description]
    """

    users = models.ManyToManyField(Contact)
    current_user = models.ForeignKey(
        Contact,
        related_name='owner',
        on_delete=models.CASCADE,
        null=True
    )

    @classmethod
    def make_friend(cls, current_user, new_friend):
        """[summary]

        Args:
            current_user ([type]): [description]
            new_friend ([type]): [description]

        Returns:
            [type]: [description]
        """
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_friend)
        return True

    @classmethod
    def remove_friend(cls, current_user, new_friend):
        """[summary]

        Args:
            current_user ([type]): [description]
            new_friend ([type]): [description]

        Returns:
            [type]: [description]
        """
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)
        return True
