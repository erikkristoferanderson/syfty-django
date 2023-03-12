from django.db import models
from accounts.models import CustomUser

# from django.db import models


class Syft(models.Model):
    subreddit = models.CharField(max_length=200)
    search_term = models.CharField(max_length=200, default="")
    owner = models.ForeignKey(CustomUser,
                              on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.subreddit + "," + self.search_term + ',' + str(self.owner.id)


class Subscription(models.Model):
    active = models.BooleanField(default=False)
    owner = models.ForeignKey(CustomUser,
                              on_delete=models.CASCADE, default=1)
