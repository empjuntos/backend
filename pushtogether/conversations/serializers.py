import time

from django.conf.urls import url, include
from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import routers, serializers, viewsets

from .models import Conversation, Comment, Vote


User = get_user_model()


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'name')

    def get_name(self, obj):
        return obj.get_full_name()


class VoteSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Vote
        fields = ('id', 'author','comment', 'value')


class CommentReportSerializer(serializers.HyperlinkedModelSerializer):
    author = AuthorSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'author', 'total_votes', 'agree_votes',
            'disagree_votes', 'pass_votes', 'approval')


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'conversation', 'author', 'content', 'approval', 'votes')


class ConversationReportSerializer(serializers.HyperlinkedModelSerializer):
    author = AuthorSerializer(read_only=True)
    comments = CommentReportSerializer(read_only=True, many=True)

    class Meta:
        model = Conversation
        fields = ('id', 'author', 'total_votes', 'agree_votes', 'disagree_votes',
            'pass_votes', 'total_comments', 'approved_comments',
            'rejected_comments', 'unmoderated_comments', 'total_participants',
            'comments')


class ConversationSerializer(serializers.HyperlinkedModelSerializer):
    author = AuthorSerializer(read_only=True)
    user_participation_ratio = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%d-%m-%Y")
    updated_at = serializers.DateTimeField(format="%d-%m-%Y")
    
    class Meta:
        model = Conversation
        fields = ('id', 'url', 'title', 'description', 'author',
                  'background_color', 'background_image', 'dialog', 'response', 
                  'total_votes', 'approved_comments', 'user_participation_ratio',
                  'created_at', 'updated_at')

    def _get_current_user(self):
        return self.context['request'].user

    def get_user_participation_ratio(self, obj):
        user = self._get_current_user()
        return obj.get_user_participation_ratio(user)
