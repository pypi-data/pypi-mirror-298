from django.db import models
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
import uuid


class AuditableBaseModel(models.Model):
    """
    Abstract base model that includes audit fields for tracking creation and updates.
    """

    @staticmethod
    def random_related_name():
        """Generate a random string for related_name."""
        return get_random_string(10)

    created = models.DateTimeField(auto_now_add=True, null=True, blank=True,)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True,)

    added_by = models.ForeignKey(
        User, 
        on_delete=models.DO_NOTHING, 
        null=True, 
        blank=True,
        related_name='created_%(class)ss'
    )

    last_updated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='updated_%(class)ss'
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True