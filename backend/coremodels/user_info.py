from django.db import models
from django.contrib.auth.models import User
from backend.coremodels.cost_center import CostCenter
from django.dispatch import receiver
from django.db.models.signals import post_save

class UserInfo(User):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='test')
    cost_center = models.ForeignKey(CostCenter,  on_delete=models.CASCADE, null=True)

    #These methods will create an instance of the user_info class to extend the existing django user class
    # whenever a User object is created
    @receiver(post_save, sender=User)
    def create_user_info(sender, instance, created, **kwargs):
        if created:
            UserInfo.objects.create(user=instance)
    
    @receiver(post_save, sender=User)
    def save_user_info(sender, instance, **kwargs):
        instance.user_info.save()
    
#    def __str__(self):
 #       return self.user






#Den här klassen kan användas för att "addera på" funktionalitet och attribut på den inbyggda
# user-klassen.