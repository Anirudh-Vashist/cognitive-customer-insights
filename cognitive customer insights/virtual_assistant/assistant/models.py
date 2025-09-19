from django.db import models

class Query(models.Model):
    user_input = models.CharField(max_length=255)
    bot_response = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_input} - {self.bot_response}"