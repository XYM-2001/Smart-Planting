import datetime
from email.policy import default
from django.db import models
from django.urls import reverse


class User(models.Model):
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    profile = models.ImageField(upload_to='user_image/', default='user_image/no_image.jpeg')
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Prefer not to say',  'Prefer not to say'),
    )
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='Male')
    birthday = models.DateField(default = datetime.datetime.today().strftime("%Y-%m-%d"))
    phone_num = models.PositiveBigIntegerField(default=0000000000)
    c_time = models.DateTimeField(auto_now_add=True)
    ACCOUNT_TYPE = (
        ('Premium Free', 'Premium Free'),
        ('Premium', 'Premium'),
        ('Premium Plus', 'Premium Plus')
    )
    status = models.CharField(max_length=50, choices=ACCOUNT_TYPE, default='Premium Free')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('authentication:login')
    class Meta:
        ordering = ['c_time']

class Expert(models.Model):
    # Qihang 
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    expertise = models.TextField()
    experience = models.TextField()
    availability = models.CharField(max_length=255)
    references = models.TextField()   

    def __str__(self):
        return self.full_name


