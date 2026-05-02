from django.db import models

class Client(models.Model):
    company_name = models.CharField(max_length=255)
    group_name = models.CharField(max_length=255, blank=True, null=True)
    categories = models.TextField() # Isme selected categories store hongi
    states = models.TextField()     # Isme selected states store honge
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name
    




