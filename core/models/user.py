from django.db import models
from core.base_models import (
    PlanChoices, 
    MetadataModels,
)
from django.contrib.auth.models import (
    AbstractUser, 
    BaseUserManager,
)

class UserManager(BaseUserManager):

    def create_user(
        self,
        username:str,
        password:str,
        is_active:bool,
        email:str,
        phone_number:str=None,
        last_name:str=None,
        first_name:str=None,
        **extra_fields,
    ):
        user = self.model(
            email=email,
            username=username,
            is_active=is_active
        )
        if password:
            user.set_password(password)
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if phone_number:
            user.phone_number = phone_number
        user.save()
        return user


class User(MetadataModels, AbstractUser): 
    email = models.EmailField(unique=True)
    organization = models.ForeignKey("core.Organization", null=True, blank=True, on_delete=models.CASCADE, related_name="users")
    plan = models.CharField(max_length=7, choices=PlanChoices.choices, default=PlanChoices.FREE)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    # @property
    # def active_plan(self):
    #     if self.organization is not None:
    #         return self.organization.plan
    #     return self.plan
    
    # @property
    # def _as_dict(self):
    #     return {
    #         "id":str(self.id),
    #         "username":self.username,
    #         "first_name":self.first_name,
    #         "last_name":self.last_name,
    #         "email":self.email,
    #         "phone_number":self.phone_number,
    #         "organization":None if not self.organization else self.organization.name,
    #         "plan":self.plan,
    #         "is_active":self.is_active,
    #     }