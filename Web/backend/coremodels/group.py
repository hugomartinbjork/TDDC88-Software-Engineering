from django.db import models


class GroupInfo(models.Model):
    '''Group info.'''
    id = models.CharField(max_length=30, primary_key=True)
    group_name = models.CharField(max_length=30)

    def __str__(self):
        return self.group_name
