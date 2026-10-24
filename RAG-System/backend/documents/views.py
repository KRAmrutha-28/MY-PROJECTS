from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Document
from .serializers import DocumentSerializer
from .chunking import DocumentChunker
from .embeddings import EmbeddingManager

from retrieval.retriever import Retriever

import traceback
import os


class DeleteDocumentView(APIView):

    def delete(
        self,
        request,
        document_id
    ):

        try:

            doc = Document.objects.get(
                document_id=document_id
            )

            print(
                f"Deleting document: {doc.title}"
            )

            # Delete vectors from ChromaDB
            embedding_manager = (
                EmbeddingManager()
            )

            embedding_manager.delete_document_chunks(
                doc.title
            )

            # Delete physical file
            if doc.file:

                if os.path.isfile(
                    doc.file.path
                ):

                    os.remove(
                        doc.file.path
                    )

                    print(
                        f"Deleted file: {doc.file.path}"
                    )

            # Delete database record
            doc.delete()

            print(
                f"Deleted database record: {doc.title}"
            )

            return Response(
                {
                    "message":
                    "Document, file and ChromaDB chunks deleted successfully"
                },
                status=status.HTTP_200_OK
            )

        except Document.DoesNotExist:

            return Response(
                {
                    "error":
                    "Document not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:

            traceback.print_exc()

            return Response(
                {
                    "error":
                    str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DocumentUploadView(APIView):

    def get(self, request):

        return Response({
            "message":
            "Upload endpoint working"
        })

    def post(self, request):

        serializer = DocumentSerializer(
            data=request.data
        )

        if serializer.is_valid():

            document = serializer.save()

            try:

                document.file_size = (
                    document.file.size
                )

                filename = (
                    document.file.name
                )

                document.file_type = (
                    filename.split(".")[-1]
                    .lower()
                )

                document.processing_status = (
                    "PROCESSING"
                )

                document.save()

                file_path = (
                    document.file.path
                )

                print(
                    "======================"
                )
                print(
                    "File Path:",
                    file_path
                )
                print(
                    "File Type:",
                    document.file_type
                )
                print(
                    "======================"
                )

                chunker = (
                    DocumentChunker()
                )

                text = (
                    chunker.extract_text(
                        file_path
                    )
                )

                chunks = (
                    chunker.chunk_text(
                        text
                    )
                )

                embedding_manager = (
                    EmbeddingManager()
                )

                embedding_manager.store_chunks(
                    chunks,
                    document.title
                )

                document.total_chunks = (
                    len(chunks)
                )

                document.processing_status = (
                    "COMPLETED"
                )

                document.save()

                return Response(
                    {
                        "message":
                        "Document uploaded and indexed successfully",

                        "document_id":
                        str(
                            document.document_id
                        ),

                        "file_type":
                        document.file_type,

                        "file_size":
                        document.file_size,

                        "chunks_created":
                        len(chunks)
                    },
                    status=status.HTTP_201_CREATED
                )

            except Exception as e:

                traceback.print_exc()

                document.processing_status = (
                    "FAILED"
                )

                document.save()

                return Response(
                    {
                        "error":
                        str(e)
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class DocumentListView(APIView):

    def get(self, request):

        documents = (
            Document.objects.all()
            .order_by("-uploaded_at")
        )

        serializer = (
            DocumentSerializer(
                documents,
                many=True
            )
        )

        return Response(
            serializer.data
        )


class QueryView(APIView):

    def post(self, request):

        query = request.data.get(
            "query"
        )

        if not query:

            return Response(
                {
                    "error":
                    "Query is required"
                },
                status=400
            )

        retriever = Retriever()

        results = retriever.search(
            query
        )

        return Response(
            {
                "query": query,
                "results": results
            }
        )