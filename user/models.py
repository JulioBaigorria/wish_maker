from django.db import models

class User(models.Model):
    name = models.CharField(max_length=60)
    username = models.CharField(max_length=60)
    password = models.CharField(max_length=60)
    date_hired = models.DateField()
    yourwishitems = models.ManyToManyField("wish", related_name="favorites", default=None)


    def __str__(self):
        return f'{self.name}'

class Wish(models.Model):
    name = models.CharField(max_length=60)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    wishers = models.ManyToManyField(User, related_name="items")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'






