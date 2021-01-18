from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Book(models.Model):
    book_id = models.AutoField(primary_key = True)
    book_name = models.CharField(max_length=64)
    book_author = models.CharField(max_length=64)
    description = models.TextField(max_length=300)
    avalaible = models.IntegerField(null=True)
    book_image = models.ImageField(null=True,blank=True,upload_to="images/")
    category = models.CharField(max_length=64,default="book")
    def __str__(self):
        return f"{self.book_name}"

Branch_choices = (
    ('1','Electronics'),
    ('2','Computer Science'),
    ('3','Information Technology'),
    ('4','Production'),
    ('5','Civil'),
    ('6','Mechanical'),
    ('7','Electrical'),
    ('8','Chemical'),
    ('9','Instrumentation'),
    ('10','Textile')
)

Year_choices = (
    ('1','FirstYear BTECH'),
    ('2','SecondYear BTECH'),
    ('3','ThirdYear BTECH'),
    ('4','FourthYear BTECH'),
    ('5','FiveYear BTECH'),
    ('6','SixYear BTECH'),
)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reg_no = models.CharField(max_length=64, blank=False)
    Branch = models.CharField(max_length=64, choices = Branch_choices, default='1')
    Year = models.CharField(max_length=64,choices = Year_choices,default='1')
    books = models.ManyToManyField(Book,blank=True,related_name="books")
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()