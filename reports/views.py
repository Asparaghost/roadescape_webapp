from django.shortcuts import render, redirect
from django.core.mail import send_mail
from decouple import config
from .models import IncidentReport
from .forms import IncidentReportForm, ContactForm, EditIncidentReportForm
from django.utils import timezone
from google.cloud import firestore
from firebase_admin import storage, credentials, auth, initialize_app, get_app
from firebase_admin import db as admin_db 
import firebase_admin
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.template.loader import render_to_string, get_template
import datetime
import io
import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.db.models.functions import ExtractMonth
from xhtml2pdf import pisa


db = firestore.Client()
cred = credentials.Certificate('credentials.json')
storage_bucket_url = 'roadescape2023.appspot.com'


def index(request):
    return render(request, "reports/home.html")

def about(request):
    return render(request, "reports/about_us.html")

def sign_in(request):
    return render(request, "reports/sign_in.html")

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            content = form.cleaned_data['content']
            
            html = render_to_string('reports/emails/contactform.html', {
                'name': name,
                'email': email,
                'content': content
            })

            send_mail('The contact form subject', 'This is the message', 'noreply@roadescape.com', ['caps2023.application@gmail.com'], html_message=html)
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, "reports/contact.html", {'form': form})

@login_required
def ongoing(request):
    collection_ref = db.collection("IncidentReport")
    incident_reports = collection_ref.stream()
    incident_report_data = []

    for incident_report in incident_reports:
        data = incident_report.to_dict()
        status = data.get('status', "Unknown")

        if status == "ongoing":
            description = data.get('description', "No description available")
            created_by = data.get('createdBy', "Unknown")
            created_at = data.get('createdAt', "Unknown")
            obstruction = data.get('obstruction', "N/A")
            latitude = data.get('latitude', "N/A")
            longitude = data.get('longitude', "N/A")
            image_url = data.get('imageUrls', '')
        
            incident_report_data.append({
                'id': incident_report.id,
                'description': description,
                'createdBy': created_by,
                'createdAt': created_at,
                'obstruction': obstruction,
                'imageUrls': image_url,
                'latitude': latitude,
                'longitude': longitude,
                'status': status,
        })
    incident_reports_json = json.dumps(incident_report_data, indent=4, sort_keys=True, default=str)

    
    context = {
        "incident_reports_json": incident_reports_json,
        "incident_reports": incident_report_data,
        "api_key": config('GOOGLE_MAPS_API_KEY'),
    }
    return render(request, "reports/ongoing.html", context)

@login_required
def details_reported(request, id):
    incident_ref = db.collection("IncidentReport").document(id)
    incident_report = incident_ref.get()
    data = incident_report.to_dict()
    context = {
        "incident_report": data,
        "id": id,
        "api_key": config('GOOGLE_MAPS_API_KEY'),
    }
    return render(request, "reports/details_reported.html", context)


@login_required
def details_ongoing(request, id):
    incident_ref = db.collection("IncidentReport").document(id)
    incident_report = incident_ref.get()
    data = incident_report.to_dict()
    context = {
        "incident_report": data,
        "id": id,
        "api_key": config('GOOGLE_MAPS_API_KEY'),
    }
    return render(request, "reports/details_ongoing.html", context)


@login_required
def status_ongoing(request, id):
    incident_ref = db.collection("IncidentReport").document(id)
    incident_report = incident_ref.get()
    
    if not incident_report.exists:
        return JsonResponse({'status': 'error', 'message': 'Incident report not found'})

    incident_ref.update({'status': 'ongoing'})
    return render(request, "reports/requests.html")


@login_required
def status_ended(request, id):
    incident_ref = db.collection("IncidentReport").document(id)
    incident_report = incident_ref.get()
    
    if not incident_report.exists:
        return JsonResponse({'status': 'error', 'message': 'Incident report not found'})

    incident_ref.update({'status': 'ended'})
    return render(request, "reports/ongoing.html")


@login_required
def requests(request):
    collection_ref = db.collection("IncidentReport")
    incident_reports = collection_ref.stream()
    incident_report_data = []

    for incident_report in incident_reports:
        data = incident_report.to_dict()
        status = data.get('status', "Unknown")

        if status == "reported":
            description = data.get('description', "No description available")
            created_by = data.get('createdBy', "Unknown")
            created_at = data.get('createdAt', "Unknown")
            obstruction = data.get('obstruction', "N/A")
            latitude = data.get('latitude', "N/A")
            longitude = data.get('longitude', "N/A")
            image_url = data.get('imageUrls', '')
        
            incident_report_data.append({
                'id': incident_report.id,
                'description': description,
                'createdBy': created_by,
                'createdAt': created_at,
                'obstruction': obstruction,
                'imageUrls': image_url,
                'latitude': latitude,
                'longitude': longitude,
                'status': status,
        })
    incident_reports_json = json.dumps(incident_report_data, indent=4, sort_keys=True, default=str)

    context = {
        "incident_reports_json": incident_reports_json,
        "incident_reports": incident_report_data,
        "api_key": config('GOOGLE_MAPS_API_KEY'),
    }
    return render(request, "reports/requests.html", context)


@login_required
def history(request):
    collection_ref = db.collection("IncidentReport")
    incident_reports = collection_ref.stream()
    incident_report_data = []

    for incident_report in incident_reports:
        data = incident_report.to_dict()
        status = data.get('status', "Unknown")

        if status == "ended":
            description = data.get('description', "No description available")
            created_by = data.get('createdBy', "Unknown")
            created_at = data.get('createdAt', "Unknown")
            obstruction = data.get('obstruction', "N/A")
            latitude = data.get('latitude', "N/A")
            longitude = data.get('longitude', "N/A")
            image_url = data.get('imageUrls', '')
        
            incident_report_data.append({
                'id': incident_report.id,
                'description': description,
                'createdBy': created_by,
                'createdAt': created_at,
                'obstruction': obstruction,
                'imageUrls': image_url,
                'latitude': latitude,
                'longitude': longitude,
                'status': status,
        })
    incident_reports_json = json.dumps(incident_report_data, indent=4, sort_keys=True, default=str)

    context = {
        "incident_reports_json": incident_reports_json,
        "incident_reports": incident_report_data,
        "api_key": config('GOOGLE_MAPS_API_KEY'),
    }
    return render(request, "reports/history.html", context)


@login_required
def delete_report(request, id):
    try:
        incident_ref = db.collection("IncidentReport").document(id)
        incident_ref.delete()
        return redirect('requests') 
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': 'Failed to delete incident report'})


@login_required
def delete_history(request, id):
    try:
        incident_ref = db.collection("IncidentReport").document(id)
        incident_ref.delete()
        return redirect('history') 
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': 'Failed to delete incident report'})

@login_required
def save_to_firebase(request):
    if request.method == 'POST':
        form = IncidentReportForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            data['status'] = 'ongoing'
            data['createdBy'] = 'RoadEscape_admin'
            data['createdAt'] = timezone.now()

            bucket = storage.bucket()
            image_urls = [] 

            if 'imageUrls' in request.FILES:
                image = request.FILES['imageUrls']
                if image:
                    image_blob = bucket.blob(f'images/{image.name}')
                    image_blob.upload_from_file(image, content_type=image.content_type)

                    token = auth.create_custom_token('public')
                    download_url = image_blob.generate_signed_url(
                        datetime.timedelta(days=7),
                        method='GET', version='v4',
                        query_parameters={'alt': 'media', 'token': token})

                    image_urls.append(download_url)  

            incident_report = IncidentReport(**data)
            incident_report.save()

            firestore_client = firestore.Client()
            reports_ref = firestore_client.collection('IncidentReport')
            
            data['imageUrls'] = image_urls
            new_report_ref, document_id = reports_ref.add(data)

            return redirect('ongoing')
    else:
        form = IncidentReportForm()
    return render(request, 'reports/incident_form.html', {'form': form, "api_key": config('GOOGLE_MAPS_API_KEY')})


@login_required
def update_ongoing_incident(request, id):
    try:
        incident_ref = db.collection("IncidentReport").document(id)
        incident_report = incident_ref.get()

        if not incident_report.exists:
            return JsonResponse({'status': 'error', 'message': 'Failed to update incident report because it does not exist'})

        form = EditIncidentReportForm(request.POST or None, instance=IncidentReport(**incident_report.to_dict()))

        if request.method == 'POST' and form.is_valid():
            data = form.cleaned_data
            incident_ref.update({
                'obstruction': data['obstruction'], 
                'description': data['description'],
                'latitude': data['latitude'], 
                'longitude': data['longitude'] 
                })
            return redirect('ongoing')

        context = {
            'form': form,
            'id': id,
            "api_key": config('GOOGLE_MAPS_API_KEY')
        }
        return render(request, 'reports/update_ongoing.html', context)

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': 'Failed to update incident report'})



@login_required
def update_reported_incident(request, id):
    try:
        incident_ref = db.collection("IncidentReport").document(id)
        incident_report = incident_ref.get()

        if not incident_report.exists:
            return JsonResponse({'status': 'error', 'message': 'Failed to update incident report because it does not exist'})

        form = EditIncidentReportForm(request.POST or None, instance=IncidentReport(**incident_report.to_dict()))

        if request.method == 'POST' and form.is_valid():
            data = form.cleaned_data
            incident_ref.update({
                'obstruction': data['obstruction'], 
                'description': data['description'],
                'latitude': data['latitude'], 
                'longitude': data['longitude'] 
                })
            return redirect('requests')

        context = {
            'form': form,
            'id': id,
            "api_key": config('GOOGLE_MAPS_API_KEY')
        }
        return render(request, 'reports/update_reported.html', context)

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': 'Failed to update incident report'})
    
    
@login_required
def analytics(request):
    try:
        firebase_users = auth.list_users()
        users_count = len(firebase_users.users)

        incident_reports = get_all_incident_reports()
        incident_data = get_incident_data()

        reported_incidents_count = count_incidents_by_status("reported")
        ongoing_incidents_count = count_incidents_by_status("ongoing")
        ended_incidents_count = count_incidents_by_status("ended")
        incident_monthly = get_incident_monthly()

        months = [str(month) for month in range(1, 13)]
        monthly_counts = [incident_monthly.get(month, 0) for month in months]
        context = {
            'users_count': users_count,
            'reported_incidents_count': reported_incidents_count,
            'ongoing_incidents_count': ongoing_incidents_count,
            'ended_incidents_count': ended_incidents_count,
            'incident_reports': incident_reports,
            'incident_data': json.dumps(incident_data),
            'incident_monthly': json.dumps(incident_monthly),
            'months': json.dumps(months),  
            'monthly_counts': json.dumps(monthly_counts),
        }

        return render(request, "reports/analytics.html", context)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


def count_incidents_by_status(status):
    firestore_client = firestore.Client()
    incidents_ref = firestore_client.collection('IncidentReport')
    query = incidents_ref.where('status', '==', status)
    incidents = query.stream()
    count = len(list(incidents))
    return count


def get_incident_data():
    firestore_client = firestore.Client()

    incidents_ref = firestore_client.collection('IncidentReport')
    incident_reports = incidents_ref.stream()
    incident_data = {}

    for incident_report in incident_reports:
        data = incident_report.to_dict()
        obstruction = data.get('obstruction', '')
        status = data.get('status', '')

        if status in ('ongoing', 'ended'):
            if obstruction not in incident_data:
                incident_data[obstruction] = 1
            else:
                incident_data[obstruction] += 1
    return incident_data


def get_incident_monthly():
    firestore_client = firestore.Client()

    incidents_ref = firestore_client.collection('IncidentReport')
    incident_reports = incidents_ref.stream()
    incident_monthly = {}

    for incident_report in incident_reports:
        data = incident_report.to_dict()
        status = data.get('status', '')
        created_at = data.get('createdAt', None)

        if created_at:
            month = created_at.month
            key = str(month)

            if status in ('reported', 'ongoing', 'ended'):
                if key not in incident_monthly:
                    incident_monthly[key] = 1
                else:
                    incident_monthly[key] += 1

    return incident_monthly


@login_required
def generate_pdf(request):
    incident_reports = get_all_incident_reports()
    selected_incident_ids = request.GET.getlist('selected_incidents')
    selected_incidents = [incident for incident in incident_reports if incident['id'] in selected_incident_ids]

    context = {
        'selected_incidents': selected_incidents,
        'api_key': config('GOOGLE_MAPS_API_KEY'),
    }

    template = get_template('reports/pdf_template.html')
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="incident_reports.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response


def get_all_incident_reports():
    firestore_client = firestore.Client()
    incidents_ref = firestore_client.collection('IncidentReport')

    incident_reports = incidents_ref.stream()
    incident_reports_data = []

    for incident_report in incident_reports:
        data = incident_report.to_dict()
        incident_reports_data.append({
            'id': incident_report.id,
            'obstruction': data.get('obstruction', ''),
            'status': data.get('status', ''),
            'description': data.get('description', ''),
            'createdBy': data.get('createdBy', ''),
            'createdAt': data.get('createdAt', ''),
            'imageUrls': data.get('imageUrls', ''),
            'latitude': data.get('latitude', ''),
            'longitude': data.get('longitude', ''),
        })

    return incident_reports_data
