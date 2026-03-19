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
from django.db.models import Avg, Count
from django.db.models.functions import TruncDate
import json
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

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

            result = detect_ai_image(tensor, image_path)
            confidence = result["confidence"]
            tool = result["type"]

            ai_prob = result["ai_probability"]
            human_prob = result["human_probability"]

            confidence = round(max(ai_prob, human_prob) / 100 * 100, 2)

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
    user = request.user
    scans = ScanHistory.objects.filter(user=user)

    total_scans = scans.count()
    doc_count = scans.filter(scan_type="document").count()
    img_count = scans.filter(scan_type="image").count()
    text_count = scans.filter(scan_type="text").count()

    ai_count = scans.filter(result__icontains="ai").count()
    human_count = scans.filter(result__icontains="human").count()
    mixed_count = scans.filter(result__icontains="mixed").count()

    # ✅ Average Accuracy
    avg_accuracy = scans.aggregate(avg=Avg('accuracy'))['avg'] or 0

    # ✅ Insight
    if ai_count > human_count:
        insight = "Most content is AI generated"
    else:
        insight = "Most content is human written"

    # ✅ Weekly Data
    weekly = (
        scans.annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )

    dates = [str(item['date']) for item in weekly]
    counts = [item['count'] for item in weekly]

    # ✅ Recent Activity
    recent_scans = scans.order_by('-created_at')[:5]
    # filter_type = request.GET.get('type')

    # if filter_type and filter_type != "all":
    #   scans = scans.filter(scan_type=filter_type)
    
    context = {
        "total_scans": total_scans,
        "doc_count": doc_count,
        "img_count": img_count,
        "text_count": text_count,
        "ai_count": ai_count,
        "human_count": human_count,
        "mixed_count": mixed_count,
        "avg_accuracy": round(avg_accuracy, 2),
        "insight": insight,
        "dates": dates,
        "counts": counts,
        "recent_scans": recent_scans,
    }

    return render(request, "dashboard.html", context)


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

    scan = get_object_or_404(ScanHistory, id=id, user=request.user)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="scan_report_{id}.pdf"'

    doc = SimpleDocTemplate(response)
    styles = getSampleStyleSheet()
    styles["Title"].alignment = 1

    content = []

    # 🔥 TITLE
    content.append(Paragraph("AI Content Detection Report", styles["Title"]))
    content.append(Spacer(1, 20))

    # 🔥 BASIC INFO
    content.append(Paragraph(f"<b>Scan Type:</b> {scan.scan_type}", styles["Normal"]))
    content.append(Paragraph(f"<b>Result:</b> {scan.result}", styles["Normal"]))
    content.append(Paragraph(f"<b>Accuracy:</b> {scan.accuracy}%", styles["Normal"]))
    content.append(Paragraph(f"<b>Date:</b> {scan.created_at}", styles["Normal"]))
    content.append(Spacer(1, 20))

    # ✅ FINAL VERDICT
    if scan.result == "AI":
        verdict_color = "red"
    elif scan.result == "Human":
        verdict_color = "green"
    else:
        verdict_color = "orange"

    content.append(Paragraph(
        f"<font color='{verdict_color}' size=14><b>Final Verdict: {scan.result} Generated</b></font>",
        styles["Normal"]
    ))
    content.append(Spacer(1, 20))

    # 🔥 SUMMARY
    content.append(Paragraph("Detection Summary", styles["Heading2"]))
    content.append(Spacer(1, 10))
    content.append(Paragraph(f"<b>AI Content:</b> {scan.accuracy}%", styles["Normal"]))

    # ✅ CONFIDENCE
    if scan.accuracy > 80:
        level = "High Confidence"
    elif scan.accuracy > 60:
        level = "Moderate Confidence"
    else:
        level = "Low Confidence"

    content.append(Paragraph(f"<b>Confidence Level:</b> {level}", styles["Normal"]))
    content.append(Spacer(1, 20))

    # 👉 PARSE JSON SAFELY
    try:
        details = json.loads(scan.details)

        if isinstance(details, dict):
            details = [details]

        details = [d for d in details if isinstance(d, dict)]

    except:
        details = []

    # ✅ DISTRIBUTION (ONLY ONCE, CORRECT WAY)
    ai_count = 0
    human_count = 0
    mixed_count = 0

    for r in details:
        cls = r.get("classification")

        if cls == "AI":
            ai_count += 1
        elif cls == "Human":
            human_count += 1
        elif cls == "Mixed":
            mixed_count += 1

    content.append(Paragraph("Content Distribution", styles["Heading2"]))
    content.append(Spacer(1, 10))
    content.append(Paragraph(f"AI Sentences: {ai_count}", styles["Normal"]))
    content.append(Paragraph(f"Human Sentences: {human_count}", styles["Normal"]))
    content.append(Paragraph(f"Mixed Sentences: {mixed_count}", styles["Normal"]))
    content.append(Spacer(1, 20))

    # ✅ WARNING
    if scan.result == "AI":
        warning = "This content is likely AI-generated. Verify before use."
    elif scan.result == "Mixed":
        warning = "Mixed signals detected. Manual review recommended."
    else:
        warning = "Content appears human-written."

    content.append(Paragraph(
        f"<font color='orange'><b>Note:</b> {warning}</font>",
        styles["Normal"]
    ))
    content.append(Spacer(1, 20))

    # 🔥 ANALYSIS DETAILS
    content.append(Paragraph("Analysis Details", styles["Heading2"]))
    content.append(Spacer(1, 10))

    if scan.scan_type in ["text", "document"] and details:

        for r in details:
            if not isinstance(r, dict):
                continue

            sentence = r.get("sentence", "")
            sentence = sentence[:300] + "..." if len(sentence) > 300 else sentence

            classification = r.get("classification", "")
            ai_prob = round(r.get("ai_probability", 0) * 100, 2)
            human_prob = round(r.get("human_probability", 0) * 100, 2)

            # 🎨 COLOR
            if classification == "AI":
                color = "red"
            elif classification == "Human":
                color = "green"
            else:
                color = "orange"

            text = f"""
            <font color="{color}">
            <b>Sentence:</b> {sentence}<br/>
            <b>Type:</b> {classification}<br/>
            <b>AI:</b> {ai_prob}% | <b>Human:</b> {human_prob}%
            </font>
            """

            content.append(Paragraph(text, styles["BodyText"]))
            content.append(Spacer(1, 15))

    else:
        content.append(Paragraph(
            "<font color='blue'>This is an image scan — no sentence-level analysis available.</font>",
            styles["Normal"]
        ))
        content.append(Spacer(1, 10))
        content.append(Paragraph(f"<b>AI Probability:</b> {scan.accuracy}%", styles["Normal"]))

    # ✅ PAGE BREAK (FIXES LAYOUT)
    content.append(PageBreak())

    # ✅ METADATA
    content.append(Paragraph("Report Metadata", styles["Heading2"]))
    content.append(Spacer(1, 10))
    content.append(Paragraph(f"Report ID: {scan.id}", styles["Normal"]))
    content.append(Paragraph("Generated By: AI Scanner System", styles["Normal"]))

    # ✅ HEADER + FOOTER
    def add_header_footer(canvas, doc):
        canvas.setFont("Helvetica-Bold", 12)
        canvas.drawString(180, 800, "AI Content Detection Report")

        canvas.setFont("Helvetica", 9)
        canvas.drawString(200, 20, "Generated by AI Scanner")

    doc.build(content, onFirstPage=add_header_footer, onLaterPages=add_header_footer)

    return response

def delete_scan(request, id):

    scan = get_object_or_404(ScanHistory, id=id, user=request.user)

    if request.method == "POST":
        scan.delete()

    return redirect('scan_history')