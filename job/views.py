from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# import re # for email validation
from .models import Job
from .forms import JobPostForm  # imported this for the post job form


# Create your views here.

def home(request):
    jobs_ = Job.objects.all()
    return render(request, 'home.html', {'jobs': jobs_})


def jobs(request):
    return HttpResponse('Jobs')


@login_required(login_url="signin")
def post_job(request):
    if request.method == 'POST':

        # using django modelform and its validation
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = Job()
            job.employer_email = form.cleaned_data['employer_email']
            job.title = form.cleaned_data['title']
            job.location = form.cleaned_data['location']
            job.category = form.cleaned_data['category']
            job.job_type = form.cleaned_data['job_type']
            job.description = form.cleaned_data['description']
            job.application_email_website = form.cleaned_data['application_email_website']
            job.closing_Date = form.cleaned_data['closing_Date']
            job.company_name = form.cleaned_data['company_name']
            job.company_website = form.cleaned_data['company_website']
            job.save()
            return redirect('/')
        else:
            print(form.errors)

    else:
        form = JobPostForm()
    return render(request, 'Job/post_job.html', {'page_title': 'Post a Job', 'form': form})
