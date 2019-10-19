from django.db import models

# Group represents the fundamental unit in UPI-Collect.
class Group(models.Model):
    id = models.AutoField(primary_key=True)
    # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

# Contact represents the people added in each Group sharing a common Subscription