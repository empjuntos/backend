from django.conf.urls import url

from .reporters import ConversationPDFReportView

urlpatterns = [
    url(r'conversations/(?P<pk>\d+)/$', ConversationPDFReportView.as_view(),
        name='conversation-pdf-report'),
]
