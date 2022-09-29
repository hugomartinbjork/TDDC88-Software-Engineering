from django.db import models

class Group(models.Model):
    id = models.CharField(max_length = 30, primary_key=True)
    group_name = models.CharField(max_length = 30)
    def __str__(self):
        return self.group_name