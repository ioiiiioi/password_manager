import random
import string

from rest_framework.exceptions import ValidationError
from core.models.user import User

from django.utils.translation import gettext_lazy as _

class UsernameRandomizer:

    def __init__(self, payload:dict) -> None:
        email = payload.get('email', None)
        username = payload.get('username', None)
        self.email = email.lower() if email else None
        self.username = username.lower() if username else None
        if not self.email:
            raise ValidationError(detail=_('Email required'), code=400)

    def is_username_useable(self, username):
        users = User.objects.filter(username__istartswith=username)
        if users.exists():
            username_list = users.values_list('username', flat=True)
            if username in username_list:
                return False
        return True

    def generate_username(self):
        if self.username:
            if self.username_query(self.username):
                return self.username
            else:
                raise ValidationError(detail=_('Username has been taken.'), code=400)
        username = self.use_random_name()
        return username

    def username_query(self, username):
        try:
            User.objects.get(username=username)
            return False
        except User.DoesNotExist:
            return True

    def use_random_name(self):
        vowels = ["a","i","u","e","o"]
        lenght = [4, 5, 6,]
        name = ""
        fl_params = None
        while True:
            for x in range(0,2):
                char_long = random.choice(lenght)
                for i in range(0,char_long):
                    if i == 0:
                        first_letter = random.choice(string.ascii_letters)
                        if first_letter.lower() in vowels:
                            fl_params = "vowels"
                        else:
                            fl_params = "consonants"
                        name+=first_letter
                    else:
                        while True:
                            add_letter = random.choice(string.ascii_letters)
                            if fl_params == "vowels":
                                if add_letter.lower() not in vowels:
                                    name+=add_letter
                                    fl_params = "consonants"
                                    break
                                continue
                            else:
                                if add_letter.lower() in vowels:
                                    name+=add_letter
                                    fl_params = "vowels"
                                    break
                                continue
                name+="_"
            
            name_candidate = name.lower()[:-1]
            if self.username_query(name_candidate):
                name = name_candidate
                break
        return name


