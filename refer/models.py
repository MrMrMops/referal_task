from django.contrib.auth.models import User
from django.db import models

admin = User.objects.get(id=1)
class Code(models.Model):
    refer_code = models.CharField(max_length=100)
    user = models.OneToOneField(User,on_delete=models.CASCADE, blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    referals = models.ForeignKey(User, on_delete=models.CASCADE , related_name='referals', blank=True,null=True)


    def __str__(self):
        return self.refer_code

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, blank=True,null=True)
    refer_by = models.ForeignKey(User, on_delete=models.CASCADE , related_name='refer_by',blank=True,null=True)

    def __str__(self):
        return self.user.username
