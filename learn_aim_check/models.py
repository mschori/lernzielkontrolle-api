from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import EducationOrdinance, User


class Tag(models.Model):
    """
    Represents a tag for a learn aim.
    i.e. Database Design, SQL, Python, etc.
    """
    tag_name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tag_name


class ActionCompetence(models.Model):
    """
    Represents an action competence.
    i.e. A1, A2, A3 etc.
    """
    identification = models.CharField(max_length=5, null=False, blank=False)
    title = models.CharField(max_length=50, null=False, blank=False)
    education_ordinance = models.ManyToManyField(EducationOrdinance)
    description = models.TextField(max_length=500, null=False, blank=False)
    associated_modules_vocational_school = models.TextField(max_length=254, null=True, blank=True)
    associated_modules_overboard_course = models.TextField(max_length=254, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns the identification and the title of the action competence.
        i.e. A1 - Create a database
        """
        return self.identification + " - " + self.title


class LearnAim(models.Model):
    """
    Represents a learn aim.
    A learn aim is a part of a action competence.
    """
    action_competence = models.ForeignKey(ActionCompetence, on_delete=models.CASCADE)
    identification = models.CharField(max_length=10, null=False, blank=False)
    description = models.TextField(max_length=254, null=False, blank=False)
    taxonomy_level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)], null=False,
                                         blank=False)
    example_text = models.TextField(max_length=254, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        """
        Returns the identification of the learn aim.
        i.e. A1.1 - Create a database
        """
        return self.action_competence.identification + " - " + self.identification


class CheckLearnAim(models.Model):
    """
    Represents a close learn aim.

    """
    assigned_trainee = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    closed_learn_check = models.ForeignKey(LearnAim, on_delete=models.CASCADE, null=False, blank=False)
    comment = models.TextField(max_length=254, null=False, blank=False)
    semester = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)], null=False, blank=False)
    close_stage = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)], null=False, blank=False)
    is_approved = models.BooleanField(null=False, blank=False, default=False)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='approved_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns the identification of the learn aim.
        i.e. A1.1 - Create a database
        """
        return self.assigned_trainee.email + " - " + self.closed_learn_check.action_competence.identification + "." + self.closed_learn_check.identification + ": " + self.closed_learn_check.description
