from django.db import models
from core.base_models import (
    MetadataModels,
    BaseModels,
    PlanChoices,
    ShareLevelChoices,
)

class Team(BaseModels):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=13, choices=ShareLevelChoices.choices)
    organization = models.ForeignKey("core.Organization", on_delete=models.CASCADE, related_name="teams", null=True, blank=True)
    member = models.ManyToManyField("core.User", related_name="teams", blank=True)
    created_by = models.ForeignKey("core.User", on_delete=models.CASCADE, related_name="teams_creator")

