from django.db import models
from django.contrib.auth.models import User

# Candidate table
class Candidate(models.Model):
    name = models.CharField(max_length=100)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.name


# Vote table (one user can vote only once)
class Vote(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)