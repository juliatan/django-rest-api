from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    # Specify the functions for the manager

    #  If no password is given, set to none
    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        # Takes into account emails being empty string or null
        if not email:
            raise ValueError('User must have an email address')

        # normalizing makes the second half of the email lowercase
        email = self.normalize_email(email)

        # Creates a new model instance of UserProfile
        user = self.model(email=email, name=name)

        # Doing this ensures the password is encrypted
        user.set_password(password)

        # Specify the database to save the user to (in case we use multiple databases in the future)
        user.save(using=self._db)

        return user

    # superuser must have password
    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""
        
        # Don't need to pass in self, since it's a class function we're using
        user = self.create_user(email, name, password)

        # is_superuser is automatically created by the PermissionsMixin
        user.is_superuser = True
        user.is_staff = True

        # Save the user
        user.save(using=self._db)

        return user


# Once done with custom user model configuration, go to settings.py and add the AUTH_USER_MODEL setting
class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # For Django CLI - we can customise what is asked when creating a user e.g. createsuperuser
    objects = UserProfileManager()

    # Use email instead of default username. This automatically makes it required.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
      """Retrieve full name of user"""
      return self.name

    def get_short_name(self):
      """Retrieve short name of user"""
      return self.name

    # Recommended for all Django models to ensure we get some meaningful representation of the model
    def __str__(self):
      """Return string representation of our user"""
      return self.email


class ProfileFeedItem(models.Model):
    """Profile status update"""
    # Connects to the UserProfile model. Because we are using an auth user model, it is best practice to reference the settings
    # in the event we want to change this in the future.
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    # Text of the status update
    status_text = models.CharField(max_length=255)
    # Date and time of the status update. auto_now_add just sets it to now.
    created_on = models.DateTimeField(auto_now_add=True)

    # How to convert model instance into a string
    def __str__(self):
        """Return the model as a string"""
        return self.status_text