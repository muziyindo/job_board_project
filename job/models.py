from django.db import models
from account.models import MyUser #added this

# Create your models here.
class Job(models.Model):
	employer_id = models.ForeignKey(MyUser, on_delete=models.CASCADE,blank = True, null=True)
	employer_email = models.EmailField(max_length = 200)
	title = models.CharField(max_length=300)
	location = models.CharField(max_length=200)
	category = models.CharField(max_length=200)
	job_type = models.CharField(max_length=50, blank=True)
	description = models.TextField()
	application_email_website = models.CharField(max_length=255)
	closing_Date = models.DateField(auto_now=False, auto_now_add=False)
	company_name = models.CharField(max_length=200)
	company_website = models.CharField(max_length=200)

	def __str__(self):	
		return self.company_name

	def summary(self):
		return self.description[:100]