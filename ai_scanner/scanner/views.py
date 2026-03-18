from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from .forms import DocumentUploadForm, ImageUploadForm, TextInputForm
from .utils.text_extractor import extract_text, split_into_sentences
from .utils.image_processing import preprocess_image
from .utils.image_detector import detect_ai_image
from .utils.ai_tool_detector import detect_ai_tool
from .utils.text_processing import split_sentences, process_text
from .utils.ai_detector import analyze_sentences
from .models import ScanHistory
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from .models import ScanHistory
from django.core.paginator import Paginator
import json



def home(request):
    return render(request,'home.html')

def register_view(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")

    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})

def login_view(request):

    if request.method == "POST":

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            return redirect("home")

    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})



def document_scanner(request):

    results = []
    sentences = []
    processed = []

    ai_count = 0
    human_count = 0
    mixed_count = 0
    scan_id = None

    ai_percent = 0
    human_percent = 0
    mixed_percent = 0

    confidence = 0

    form = DocumentUploadForm()

    if request.method == "POST":

        form = DocumentUploadForm(request.POST, request.FILES)

        if form.is_valid():

            uploaded_file = request.FILES['file']
            doc = form.save()

            file_path = doc.file.path

            text = extract_text(file_path)
            sentences = split_sentences(text)
            processed = process_text(sentences)
            results = analyze_sentences(processed)

            for r in results:

                if r["classification"] == "AI":
                    ai_count += 1

                elif r["classification"] == "Human":
                    human_count += 1

                else:
                    mixed_count += 1

            total = ai_count + human_count + mixed_count

            if total > 0:

                ai_percent = round((ai_count / total) * 100, 2)
                human_percent = round((human_count / total) * 100, 2)
                mixed_percent = round((mixed_count / total) * 100, 2)

                confidence = max(ai_percent, human_percent)

            # SAVE SCAN ALWAYS
            scan = ScanHistory.objects.create(

                scan_type="document",
                file_name=uploaded_file.name,
                user=request.user if request.user.is_authenticated else None,
                result="AI" if ai_percent > human_percent else "Human",
                details=json.dumps(results),
                accuracy=confidence
            )

            scan_id = scan.id

    return render(request, "document_scanner.html", {

        "form": form,

        "results": results,
        "sentences": sentences,
        "processed": processed,

        "ai_percent": ai_percent,
        "human_percent": human_percent,
        "mixed_percent": mixed_percent,

        "confidence": confidence,
        "scan_id": scan_id
    })


def image_scanner(request):

    form = ImageUploadForm()

    scan_id = None
    image_url = None
    tensor_shape = None
    tool = None
    confidence = None
    result = None

    if request.method == "POST":

        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():

            image = form.save()

            image_url = image.image.url
            image_path = image.image.path

            tensor = preprocess_image(image_path)
            tensor_shape = tensor.shape

            result = detect_ai_image(tensor)

            ai_prob = result["ai_probability"]
            human_prob = result["human_probability"]

            confidence = max(ai_prob, human_prob) / 100

            # Detect AI tool
            if ai_prob > 60:
                tool = detect_ai_tool(image_path)

            # SAVE SCAN ALWAYS
            scan = ScanHistory.objects.create(

                scan_type="image",
                file_name=image.image.name,

                user=request.user if request.user.is_authenticated else None,

                result="AI" if ai_prob > human_prob else "Human",

                details=json.dumps(result),   # better than str()

                accuracy=confidence
            )

            scan_id = scan.id

    return render(request, 'image_scanner.html', {

        'form': form,
        'image_url': image_url,
        'tensor_shape': tensor_shape,
        'result': result,
        'tool': tool,
        'confidence': confidence,
        'scan_id': scan_id

    })

def text_analyzer(request):

    form = TextInputForm()

    results = None
    scan_id = None

    ai_count = 0
    human_count = 0
    mixed_count = 0

    ai_percent = 0
    human_percent = 0
    mixed_percent = 0

    confidence = 0

    if request.method == "POST":

        form = TextInputForm(request.POST)

        if form.is_valid():

            text_obj = form.save()

            text_data = text_obj.text

            sentences = split_sentences(text_data)

            processed = process_text(sentences)

            results = analyze_sentences(processed)

            for r in results:

                if r["classification"] == "AI":
                    ai_count += 1

                elif r["classification"] == "Human":
                    human_count += 1

                else:
                    mixed_count += 1

            total = ai_count + human_count + mixed_count

            if total > 0:

                ai_percent = round((ai_count / total) * 100, 2)
                human_percent = round((human_count / total) * 100, 2)
                mixed_percent = round((mixed_count / total) * 100, 2)

                confidence = max(ai_percent, human_percent, mixed_percent)

            # SAVE SCAN ALWAYS
            scan = ScanHistory.objects.create(

                scan_type="text",
                file_name="User Input Text",

                user=request.user if request.user.is_authenticated else None,

                result="AI" if ai_percent > human_percent else "Human",

                details=json.dumps(results),

                accuracy=confidence
            )

            scan_id = scan.id

    return render(request, "text_analyzer.html", {

        "form": form,
        "results": results,

        "ai_count": ai_count,
        "human_count": human_count,
        "mixed_count": mixed_count,

        "ai_percent": ai_percent,
        "human_percent": human_percent,
        "mixed_percent": mixed_percent,

        "confidence": confidence,
        "scan_id": scan_id
    })

def logout_view(request):
    logout(request)
    return redirect("home")

@login_required
def dashboard(request):
    return render(request, "dashboard.html")


@login_required(login_url="/login/")
def scan_history(request):

    history_list = ScanHistory.objects.filter(
        user=request.user
    ).order_by("-created_at")

    paginator = Paginator(history_list, 5)   # 5 reports per page

    page_number = request.GET.get("page")
    history = paginator.get_page(page_number)

    return render(request, "scan_history.html", {
        "history": history
    })


import json

def scan_report(request, id):
    scan = ScanHistory.objects.get(id=id)

    try:
        details = json.loads(scan.details)
    except Exception as e:
        print("JSON ERROR:", e)
        print("RAW DATA:", scan.details)
        details = []

    print("DETAILS:", details)

    # ✅ DOCUMENT CASE
    if isinstance(details, list):

        total = len(details)

        ai_count = sum(1 for r in details if isinstance(r, dict) and r.get("classification") == "AI")
        human_count = sum(1 for r in details if isinstance(r, dict) and r.get("classification") == "Human")

        ai_percent = round((ai_count / total) * 100, 2) if total else 0
        human_percent = round((human_count / total) * 100, 2) if total else 0

        confidence = max(ai_percent, human_percent)

    # ✅ IMAGE CASE (USE DIRECT PROBABILITY)
    elif isinstance(details, dict):

        ai_percent = round(details.get("ai_probability", 0), 2)
        human_percent = round(details.get("human_probability", 0), 2)

        confidence = max(ai_percent, human_percent)

        # IMPORTANT: no sentence list for image
        details = []

    else:
        ai_percent = 0
        human_percent = 0
        confidence = 0
        details = []

    return render(request, "scan_report.html", {
        "scan": scan,
        "details": details,
        "ai_percent": ai_percent,
        "human_percent": human_percent,
        "confidence": confidence,
    })

@login_required(login_url='/login/')
def download_report(request, id):



    scan = ScanHistory.objects.get(id=id)

    response = HttpResponse(content_type="application/pdf")

    response["Content-Disposition"] = f'attachment; filename="scan_report_{id}.pdf"'

    doc = SimpleDocTemplate(response)

    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("AI Content Detection Report", styles["Title"]))
    content.append(Spacer(1,20))

    content.append(Paragraph(f"Scan Type : {scan.scan_type}", styles["Normal"]))
    content.append(Paragraph(f"Result : {scan.result}", styles["Normal"]))
    content.append(Paragraph(f"Accuracy : {scan.accuracy}", styles["Normal"]))
    content.append(Paragraph(f"Date : {scan.created_at}", styles["Normal"]))
    content.append(Spacer(1, 20))
    content.append(Paragraph("Detection Summary", styles["Heading2"]))

    content.append(Paragraph(f"AI Content Percentage : {scan.accuracy}", styles["Normal"]))

    content.append(Spacer(1,20))

    content.append(Paragraph("Analysis Details:", styles["Heading2"]))
    content.append(Paragraph(scan.details, styles["Normal"]))

    doc.build(content)

    return response

def delete_scan(request, id):

    scan = get_object_or_404(ScanHistory, id=id, user=request.user)

    if request.method == "POST":
        scan.delete()

    return redirect('scan_history')