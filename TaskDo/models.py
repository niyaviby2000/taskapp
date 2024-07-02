from django.db import models

from django.contrib.auth.models import User

class Task(models.Model):

    title=models.CharField(max_length=200)

    status_opt=(

        ("pending","pending"),

        ("completed","completed"),
        
        ("status","status")
    )

    status=models.CharField(max_length=200,choices=status_opt,default="status")

    user_object=models.ForeignKey(User,on_delete=models.CASCADE)

    created_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.title



