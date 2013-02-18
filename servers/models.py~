from django.db import models

# Create your models here.
class Os(models.Model):
    nomOS = models.CharField(max_length=200)
    def __unicode__(self):
        return self.nomOS
class Server(models.Model):
    nomServer = models.CharField(max_length=200)
    typeOs = models.ForeignKey(Os)
    typeReq = models.CharField(max_length=200)
    url = models.CharField(max_length=200)

