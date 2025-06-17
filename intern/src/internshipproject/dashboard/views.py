from django.shortcuts import render
from fillapp.models import InternshipApplication
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, get_object_or_404

@login_required
def dashboard_view(request):
    interns = InternshipApplication.objects.all()
    total = interns.count()

    # Gender distribution
    male = InternshipApplication.objects.filter(gender_type='Male').count()
    female = InternshipApplication.objects.filter(gender_type='Female').count()
    total_gender = [male, female]

    # Internship position counts (top 6 known types)
    position_counts = InternshipApplication.objects.values('internship_position').annotate(count=Count('id'))

    # Manually map specific roles if needed
    roles = {
        "Computer Science / IT Intern": 0,
        "Journalism Intern": 0,
        "Marketing and Communication Intern": 0,
        "Multimedia Arts Intern": 0,
        "Research Intern": 0,
        "Statistics Intern": 0,
    }

    for item in position_counts:
        role = item['internship_position']
        if role in roles:
            roles[role] = item['count']

    total_positions = list(roles.values())

    context = {
        'total_gender': total_gender,
        'total_positions': total_positions,
        'role_labels': list(roles.keys()),  # To use in chart labels
        'total_applicants': total,
        'applicants': interns,
    }

    return render(request, 'dashboard/index.html', context)

@login_required
def applicant_detail_view(request, applicant_id):
    applicant = get_object_or_404(InternshipApplication, id=applicant_id)
    return render(request, 'dashboard/applicant_detail.html', {'applicant': applicant})

