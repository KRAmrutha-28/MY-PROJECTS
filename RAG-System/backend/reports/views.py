from rest_framework.views import APIView
from rest_framework.response import Response

from retrieval.pipeline import RetrievalPipeline
from services.gemini_service import generate_report

from django.http import FileResponse

from reports.pdf_generator import create_pdf
from reports.html_generator import create_html
from reports.docx_generator import create_docx
from reports.pptx_generator import create_pptx
from reports.xlsx_generator import create_xlsx

from .models import GeneratedReport
from documents.models import QueryHistory

import tempfile

class ReportHistoryView(APIView):


 def get(self, request):

    reports = GeneratedReport.objects.order_by(
        "-created_at"
    )

    data = []

    for report in reports:

        data.append({
            "report_id": str(report.report_id),
            "title": report.report_title,
            "created_at": report.created_at,
            "status": report.status
        })

    return Response(data)


class ReportGenerationView(APIView):


 def post(self, request):

    query = request.data.get("query")

    if not query:
        return Response(
            {"error": "Query is required"},
            status=400
        )

    pipeline = RetrievalPipeline()

    chunks = pipeline.retrieve(query)

    context = "\n\n".join(chunks)

    report = generate_report(
        query,
        context
    )

    query_obj = QueryHistory.objects.create(
        query_text=query
    )

    GeneratedReport.objects.create(
        query=query_obj,
        report_title=query,
        report_content=report,
        status="completed"
    )

    return Response({
        "query": query,
        "report": report
    })


class DownloadReportPDFView(APIView):


 def post(self, request):

    report = request.data.get("report")

    if not report:
        return Response(
            {"error": "Report is required"},
            status=400
        )

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    )

    create_pdf(report, temp_file.name)

    return FileResponse(
        open(temp_file.name, "rb"),
        as_attachment=True,
        filename="Research_Report.pdf"
    )


class DownloadHTMLView(APIView):


 def post(self, request):

    report = request.data.get("report")

    if not report:
        return Response(
            {"error": "Report is required"},
            status=400
        )

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".html"
    )

    create_html(report, temp_file.name)

    return FileResponse(
        open(temp_file.name, "rb"),
        as_attachment=True,
        filename="Research_Report.html"
    )


class DownloadDOCXView(APIView):


 def post(self, request):

    report = request.data.get("report")

    if not report:
        return Response(
            {"error": "Report is required"},
            status=400
        )

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".docx"
    )

    create_docx(report, temp_file.name)

    return FileResponse(
        open(temp_file.name, "rb"),
        as_attachment=True,
        filename="Research_Report.docx"
    )


class DownloadPPTXView(APIView):


 def post(self, request):

    report = request.data.get("report")

    if not report:
        return Response(
            {"error": "Report is required"},
            status=400
        )

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pptx"
    )

    create_pptx(report, temp_file.name)

    return FileResponse(
        open(temp_file.name, "rb"),
        as_attachment=True,
        filename="Research_Report.pptx"
    )


class DownloadXLSXView(APIView):


 def post(self, request):

    report = request.data.get("report")

    if not report:
        return Response(
            {"error": "Report is required"},
            status=400
        )

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".xlsx"
    )

    create_xlsx(report, temp_file.name)

    return FileResponse(
        open(temp_file.name, "rb"),
        as_attachment=True,
        filename="Research_Report.xlsx"
    )

