from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if email is None:
            raise TypeError("Need a login")
        user = self.model(email=self.normalize_email(email))
        user.is_active = False
        user.set_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        if email is None:
            raise TypeError("Needed a username")
        if password is None:
            raise TypeError("Needed a password")
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save()
        return user
