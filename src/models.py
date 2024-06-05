import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import SoftDeleteManager


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(
        verbose_name=_("Created at"), db_index=True, auto_now_add=True
    )
    updated_at = models.DateTimeField(verbose_name=_("Updated at"), auto_now=True)

    class Meta:
        abstract = True


class Extensions(models.Model):
    """
    Best practice for lookup field url instead pk or slug
    """

    uuid = models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    """
    Best practice for lookup field url instead pk or slug.
    for security
    """

    uuid = models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeleteManager()

    class Meta:
        abstract = True
