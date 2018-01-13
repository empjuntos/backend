from rest_framework.routers import SimpleRouter
from .views import (
    ConversationViewSet,
    ConversationReportViewSet,
    CommentViewSet,
    NextCommentViewSet,
    CommentReportViewSet,
    VoteViewSet,
    AuthorViewSet,
    RandomConversationViewSet,
)

router = SimpleRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'conversations', ConversationViewSet, base_name='conversation')
router.register(r'comments', CommentViewSet)
router.register(r'votes', VoteViewSet)
router.register(r'conversations-report', ConversationReportViewSet,
                base_name='conversation-report')
router.register(r'comments-report', CommentReportViewSet,
                base_name='comment-report')
router.register(r'next_comment', NextCommentViewSet,
                base_name='conversation-next-comment')
router.register(r'random_conversation', RandomConversationViewSet,
                base_name='conversation-random')

urlpatterns = router.urls
