from collections.abc import Iterable
from django.db import models
from django.forms import CharField
from core.base_models import BaseModels, ChoiceArrayField, FieldChoices
from core.models import User, Organization, Team

class VaultType(models.Model):
    name = models.CharField(max_length=30)
    keys = ChoiceArrayField(models.CharField(max_length=100, choices=FieldChoices.choices), default=list)

    def save(self, *args, **kwargs) -> None:
        self.name = self.name.upper()
        self.name = self.name.replace(" ", "_")
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

class Vault(BaseModels):
    name = models.CharField(max_length=255, null=False, blank=False)
    vault_type = models.ForeignKey(VaultType, on_delete=models.DO_NOTHING, related_name='vault_content', null=True, blank=True) 
    value = models.JSONField(default=dict)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='vaults_creator')
    updated_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.DO_NOTHING, related_name='vaults_updated_by')
    shared_team = models.ForeignKey(Team, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='vaults_shared_team')
    shared_organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='vaults_shared_organization')

    def save(self, *args, **kwargs) -> None:
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name

