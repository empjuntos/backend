from django.core.management.base import BaseCommand, CommandError
from pushtogether.users.models import User
from pushtogether.conversations.models import Comment, Conversation, Vote
from django.db.utils import IntegrityError
from django.db import transaction

import csv


class Command(BaseCommand):
    help = 'import polis data to EJ backend'

    def add_arguments(self, parser):
        parser.add_argument('comments', type=str,
                            help='Path to the comments csv file to import')

    def handle(self, *args, **options):
        csv_file_comments_path = options['comments']

        self.create_comments(csv_file_comments_path)

    @transaction.atomic
    def create_comments(self, csv_file_comments_path):
        with open(csv_file_comments_path, 'r') as csv_file_comments:
            readf = csv.DictReader(csv_file_comments)
            count = 0
            for row in readf:
                xid = row.get('xid')
                comment_id = row.get('comment_id')
                created = row.get('created')
                txt = row.get('txt')
                conversation_slug = row.get('conversation_slug')
                mod = self.get_moderation_state(int(row.get('mod')))
                user = self.find_user_by_xid(xid)
                if not user:
                    continue

                try:
                    conversation = Conversation.objects.get(polis_slug=conversation_slug)
                except Conversation.DoesNotExist:
                    self.stdout.write('conversation does not exist, polis_slug: ' + conversation_slug)
                    continue

                try:
                    comment = Comment.objects.get(conversation=conversation.id,
                                                  polis_id=comment_id)
                except Comment.DoesNotExist:
                    with transaction.atomic():
                        comment = Comment.objects.create(author=user, conversation=conversation,
                                                         content=txt, polis_id=comment_id, approval=mod,
                                                         created_at=created)
                    print('created comment, polis_id:' + comment.polis_id)
                    count += 1
                else:
                    print('Comment already on database. ID:' + comment.id)

            self.stdout.write('Comments created: ' + str(count))

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

    def get_moderation_state(self, mod):
        switcher = {
            0: 'UNMODERATED',
            1: 'APPROVED',
            -1: 'REJECTED',
        }
        return switcher.get(mod, 'nothing')
