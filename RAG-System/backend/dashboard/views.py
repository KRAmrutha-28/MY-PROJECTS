from rest_framework.views import APIView
from rest_framework.response import Response

from documents.models import Document
from reports.models import GeneratedReport


class DashboardStatsView(APIView):

    def get(self, request):

        documents = Document.objects.count()

        chunks = sum(
            doc.total_chunks
            for doc in Document.objects.all()
        )

        reports = GeneratedReport.objects.count()

        return Response({
            "documents": documents,
            "chunks": chunks,
            "reports": reports
        })