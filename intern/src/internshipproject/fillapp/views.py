from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from .models import InternshipApplication
from django.core.paginator import Paginator

def register(request):
    if request.method == 'POST':
        # Get form data
        firstname = request.POST.get('firstname')
        middlename = request.POST.get('middlename')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        school = request.POST.get('school')
        course = request.POST.get('course')
        year = request.POST.get('year')
        birthdate = request.POST.get('birthdate')
        gender_type = request.POST.get('gender_type')
        internship_position = request.POST.get('internship_position')
        internship_type = request.POST.get('internship_type')
        required_hrs = request.POST.get('required_hrs')
        profile_image = request.FILES.get('profile_image')
        resume_file = request.FILES.get('resume_file_name')


       # Max file size: 5MB
        MAX_FILE_SIZE = 5 * 1024 * 1024
        if resume_file.size > MAX_FILE_SIZE:
            return render(request, 'index.html', {
                'error_message': 'Resume file must be 5MB or less.',
            })

        # Allow only PDFs (check by content type or file extension)
        if not resume_file.name.lower().endswith('.pdf'):
            return render(request, 'index.html', {
                'error_message': 'Resume must be a PDF file.',
            })

        # Check if email already exists
        if InternshipApplication.objects.filter(email=email).exists():
            # Return error message if duplicate found
            return render(request, 'index.html', {
                'error_message': 'An application with this applicant already exists.',
            })

        # Save to the database
        InternshipApplication.objects.create(
            firstname=firstname,
            middlename=middlename,
            lastname=lastname,
            email=email,
            phone_number=phone_number,
            address=address,
            school=school,
            course=course,
            year=year,
            birthdate=birthdate,
            gender_type=gender_type,
            internship_position=internship_position,
            internship_type=internship_type,
            required_hrs=required_hrs,
            profile_image=profile_image,
            resume_file_name=resume_file
        )

        # Send HTML email confirmation
        html_content = render_to_string(
            'emailsconfirm.html',
            {'firstname': firstname, 'lastname': lastname}
        )
        email_message = EmailMessage(
            subject='Internship Application Received',
            body=html_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )
        email_message.content_subtype = 'html'  # Send as HTML
        email_message.send()


        # Redirect after successful POST to avoid resubmission
        return redirect(reverse('register') + '?success=1')

    # Handle GET request and show success modal if query param is set
    show_success_modal = request.GET.get('success') == '1'
    return render(request, 'index.html', {'show_success_modal': show_success_modal})









