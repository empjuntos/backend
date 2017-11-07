from rest_framework.routers import SimpleRouter
from .views import (
    ConversationViewSet,
    ConversationReportViewSet,
    ConversationReportCSVViewSet,
    CommentViewSet,
    NextCommentViewSet,
    CommentReportViewSet,
    CommentReportCSVViewSet,
    VoteViewSet,
    AuthorViewSet,
)

router = SimpleRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'conversations', ConversationViewSet, base_name='conversation')
router.register(r'comments', CommentViewSet)
router.register(r'votes', VoteViewSet)
router.register(r'conversations_report', ConversationReportViewSet,
                base_name='conversation-report')
router.register(r'conversations_report_csv', ConversationReportCSVViewSet,
                base_name='conversation-report-csv')
router.register(r'comments_report', CommentReportViewSet,
                base_name='comment-report')
router.register(r'comments_report_csv', CommentReportCSVViewSet,
                base_name='comment-report-csv')
router.register(r'next_comment', NextCommentViewSet,
                base_name='conversation-next-comment')

urlpatterns = router.urls
