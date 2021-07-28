from django import forms
from django.forms.widgets import NumberInput #for the date field
from .models import Job
import re

CATEGORIES = [
	('',''),
	('finance','finance'),
	('engineering','engineering'),
	('engineering','sales/marketing'),
]

JOB_TYPE = [
	('',''),
	('full time','full time'),
	('part time','part time'),
]

#for url validation
regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE) #url validation

regex_ = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b' #email validation


class JobPostForm(forms.Form):
	employer_email = forms.EmailField(required = True, label = "Your Email",widget=forms.TextInput(attrs={'class': 'form-control'}))
	title = forms.CharField(required = True, label = "Job Title", widget=forms.TextInput(attrs={'class': 'form-control'}))
	location = forms.CharField(required = True, label = "Job Location", widget=forms.TextInput(attrs={'class': 'form-control'}))
	category = forms.ChoiceField(choices=CATEGORIES, required = True, label = "Job Category", widget=forms.Select(attrs={'class':'form-control'}))
	job_type = forms.ChoiceField(choices=JOB_TYPE, required = True, label = "Job Type", widget=forms.Select(attrs={'class':'form-control'}))
	description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}), required = True, label = "Job description")
	application_email_website = forms.CharField(required = True, label = "Email or Website for Application",widget=forms.TextInput(attrs={'class':'form-control'}))
	closing_Date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date','class':'form-control'},format='%Y-%m-%d'), required = True, label = "Job Expiry Date", input_formats=('%Y-%m-%d', ))
	company_name = forms.CharField(required = True, label = "Company Name", widget=forms.TextInput(attrs={'class': 'form-control'}))
	company_website = forms.CharField(required = False, label = "Company Website", widget=forms.TextInput(attrs={'class': 'form-control'}))

	def clean(self):
		super(JobPostForm, self).clean()
		email_or_url = self.cleaned_data.get('application_email_website')
		# validating field to contain either email or url
        #if field doesn't contain email
		if bool(re.match(regex_, email_or_url))== False : 
			if (re.match(regex, email_or_url) is not None) == False :
				self._errors['application_email_website'] = self.error_class([
                'Field must contain a url or an email'])
		return self.cleaned_data