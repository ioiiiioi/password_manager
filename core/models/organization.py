from django.db import models
from core.base_models import (
    MetadataModels,
    BaseModels,
    PlanChoices,
    ShareLevelChoices,
)


class Organization(MetadataModels):
    name = models.CharField(max_length=50, unique=True)
    alias = models.CharField(max_length=25)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    plan = models.CharField(max_length=7, choices=PlanChoices.choices, default=PlanChoices.FREE)
    created_by = models.ForeignKey("core.User", on_delete=models.CASCADE, related_name="organization_created_by")

    def __str__(self) -> str:
        return self.name