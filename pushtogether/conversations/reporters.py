from django.views.generic import DetailView
from django.http import HttpResponse

from reportlab.pdfgen import canvas

from .models import Conversation, Comment, Vote


class ConversationPDFReportView(DetailView):
    queryset = Conversation.objects.all()

    def get(self, request, *args, **kwargs):
        conversation = self.get_object()

        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

        # Create the PDF object, using the response object as its "file."
        p = canvas.Canvas(response)

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        p.drawString(100, 100, "Hello world.")

        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()
        return response
