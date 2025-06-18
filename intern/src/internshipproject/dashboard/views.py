from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect # Best practice for POST requests
import json
from fillapp.models import InternshipApplication # Ensure this import is correct
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_http_methods


@login_required
@require_http_methods(["GET", "POST"])
@csrf_protect
def dashboard_view(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # --- AJAX Status Update Logic ---
        try:
            applicant_id = request.POST.get('applicant_id')
            new_status = request.POST.get('status')

            if not applicant_id or not new_status:
                return JsonResponse({'success': False, 'message': 'Missing data.'}, status=400)

            applicant = get_object_or_404(InternshipApplication, id=applicant_id)
            valid_statuses = [choice[0] for choice in InternshipApplication.STATUS_TYPE_CHOICES]

            if new_status not in valid_statuses:
                return JsonResponse({'success': False, 'message': 'Invalid status.'}, status=400)

            applicant.status = new_status
            applicant.save()

            return JsonResponse({'success': True, 'message': 'Status updated.', 'new_status': new_status})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    # --- Dashboard Data Logic (GET request) ---
    interns = InternshipApplication.objects.all()
    total_applicants = interns.count()

    # Gender distribution
    male = interns.filter(gender_type='Male').count()
    female = interns.filter(gender_type='Female').count()
    total_gender = [male, female]

    known_internship_positions = [
        "Computer Science / IT Intern",
        "Journalism Intern",
        "Marketing and Communication Intern",
        "Multimedia Arts Intern",
        "Research Intern",
        "Statistics Intern",
    ]

    position_counts = interns.values('internship_position').annotate(count=Count('id'))
    roles_dashboard = {position: 0 for position in known_internship_positions}

    for item in position_counts:
        role = item['internship_position']
        if role in roles_dashboard:
            roles_dashboard[role] = item['count']

    total_positions = list(roles_dashboard.values())
    role_labels = list(roles_dashboard.keys())

    # Filtering and pagination
    selected_position = request.GET.get('position')
    applicants_queryset = interns.order_by('-id')
    if selected_position and selected_position != 'all':
        applicants_queryset = applicants_queryset.filter(internship_position=selected_position)

    paginator = Paginator(applicants_queryset, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.get_page(1)

    display_pages = 8
    current_page = page_obj.number
    total_pages = paginator.num_pages

    start_page = max(1, current_page - (display_pages // 2))
    end_page = min(total_pages, start_page + display_pages - 1)

    if (end_page - start_page + 1) < display_pages:
        if current_page - start_page < display_pages // 2:
            end_page = min(total_pages, start_page + display_pages - 1)
        elif end_page - current_page < display_pages // 2:
            start_page = max(1, end_page - display_pages + 1)
            end_page = min(total_pages, start_page + display_pages - 1)

    page_range = range(start_page, end_page + 1)

    context = {
        'total_gender': total_gender,
        'total_positions': total_positions,
        'role_labels': role_labels,
        'total_applicants': total_applicants,
        'page_obj': page_obj,
        'applicants': page_obj.object_list,
        'page_range': page_range,
        'known_internship_positions': known_internship_positions,
        'selected_position': selected_position,
    }

    return render(request, 'dashboard/index.html', context)


@login_required
def applicant_detail_view(request, applicant_id):
    applicant = get_object_or_404(InternshipApplication, id=applicant_id)
    return render(request, 'dashboard/applicant_detail.html', {'applicant': applicant})




