from django.core.management.base import BaseCommand, CommandError
from pushtogether.users.models import User
from pushtogether.conversations.models import Comment, Conversation, Vote
from django.db.utils import IntegrityError
from django.db import transaction

import csv


class Command(BaseCommand):
    help = 'import polis votes to EJ backend'

    def add_arguments(self, parser):
        parser.add_argument('votes', type=str,
                            help='Path to the votes csv file to import')

    def handle(self, *args, **options):
        csv_file_votes_path = options['votes']

        self.create_votes(csv_file_votes_path)

    @transaction.atomic
    def create_votes(self, csv_file_votes_path):
        with open(csv_file_votes_path, 'r') as csv_file_votes:
            readf = csv.DictReader(csv_file_votes)
            count = 0
            for row in readf:
                xid = row.get('xid')
                comment_id = row.get('comment_id')
                vote = self.get_vote_value(row.get('vote'))
                created = row.get('created')
                conversation_slug = row.get('conversation_slug')
                user = self.find_user_by_xid(xid)
                if not user:
                    continue

                try:
                    conversation = Conversation.objects.get(polis_slug=conversation_slug)
                except Conversation.DoesNotExist:
                    self.stdout.write('conversation does not exist, polis_slug: ' + conversation_slug)
                    continue

                try:
                    comment = Comment.objects.get(polis_id=comment_id,
                                                  conversation=conversation.id)
                except Comment.DoesNotExist:
                    self.stdout.write('comment does not exist, polis_id: ' + comment_id)
                    continue

                try:
                    vote = Vote.objects.get(author=user, comment=comment,
                                            conversation_id=conversation.id)
                except Vote.DoesNotExist:
                    with transaction.atomic():
                        vote = Vote.objects.create(comment=comment, value=vote,
                                                   author=user,
                                                   created_at=created)
                    print('created vote, polis_id:' + str(vote.polis_id))
                    count += 1
                else:
                    print('Vote already on database. ID:' + vote.id)

            self.stdout.write('Votes created: ' + str(count))

    def find_user_by_xid(self, xid):
        if xid:
            try:
                user = User.objects.get(id=xid)
            except User.DoesNotExist:
                self.stdout.write('user does not exist')
                user = None
        else:
            #  TODO get user with admin id
            user = User.objects.get(id=1)
        return user

    def get_vote_value(self, vote):
        switcher = {
            '0': 0,
            '1': -1,
            '-1': 1,
        }
        return switcher.get(vote)
