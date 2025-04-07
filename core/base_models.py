from pyexpat import model
import uuid
from django import forms
from django.db import models
from django.contrib.postgres.fields import ArrayField


class BaseModels(models.Model):
    id = models.UUIDField(primary_key=True, unique=True,default=uuid.uuid4)
    is_active = models.BooleanField(default=False)
    is_sandbox = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract=True


class MetadataModels(BaseModels):
    private_metadata = models.JSONField(default=dict)
    public_metadata = models.JSONField(default=dict) 

    class Meta:
        abstract=True


class PlanChoices(models.TextChoices):
    FREE = ("FREE", "FREE")
    PREMIUM = ("PREMIUM", "PREMIUM")
    CUSTOM = ("CUSTOM", "CUSTOM")


class ShareLevelChoices(models.TextChoices):
    ORGANIZATION = ("ORGANIZATION", "ORGANIZATION")
    PERSONAL = ("PERSONAL", "PERSONAL")
    TEAM = ("TEAM", "TEAM")

READ_ONLY_FIELDS = [
    "id",
    "is_active",
    "is_sandbox",
    "created_at",
    "updated_at",
]

READ_ONLY_FIELDS_WITH_DELETE = READ_ONLY_FIELDS.append('deleted_at')

class ChoiceArrayField(ArrayField):
    """
    A field that allows us to store an array of choices.
    Uses Django's Postgres ArrayField
    and a MultipleChoiceField for its formfield.
    """

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.MultipleChoiceField,
            'choices': self.base_field.choices,
        }
        defaults.update(kwargs)
        # Skip our parent's formfield implementation completely as we don't
        # care for it.
        # pylint:disable=bad-super-call
        return super(ArrayField, self).formfield(**defaults)

class FieldChoices(models.TextChoices):
    EMAIL = ("EMAIL","EMAIL") 
    USERNAME = ("USERNAME","USERNAME") 
    PASSWORD = ("PASSWORD","PASSWORD") 
    URL = ("URL","URL") 
    NOTES = ("NOTES","NOTES") 
    TOKEN = ("TOKEN","TOKEN")
