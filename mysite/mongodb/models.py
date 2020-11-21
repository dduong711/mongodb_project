from django.db import models

class MongoDB(models.Model):
    connection_string = models.CharField(max_length=1024, unique=True)

    def __str__(self):
        return str(self.id)