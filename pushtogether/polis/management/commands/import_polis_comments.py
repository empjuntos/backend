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
            readf = csv.DictReader(csv_file_comments, delimiter=',')
            count = 0
            comments_from_polis = []
            conversations_not_found = []
            comments_created = []
            comments_already_on_db = []
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
                    conversations_not_found.append(conversation_slug)
                    continue

                # Check comments that are probably saved in wrong conversations

                # comment = Comment.objects.get(polis_id=comment_id)
                # if comment.conversation.id != conversation_id:
                #     self.stdout.write('Possível comentário em conversa errada: ')
                #     self.stdout.write('Id: ' + str(comment.id))

                try:
                    comment = Comment.objects.get(conversation=conversation.id,
                                                  polis_id=comment_id)
                except Comment.DoesNotExist:
                    with transaction.atomic():
                        comment = Comment.objects.create(author=user, conversation=conversation,
                                                         content=txt, polis_id=comment_id, approval=mod,
                                                         created_at=created)
                    comments_from_polis.append(comment.id)
                    comments_created.append(comment.id)
                    count += 1
                else:
                    comments_from_polis.append(comment.id)
                    comments_already_on_db.append(comment.id)

            self.stdout.write('Total de comentários criados: ' + str(count))
            self.print_final_report(conversations_not_found, comments_created,
                                    comments_already_on_db)
            self.print_divergences_db_polis(comments_from_polis)


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

    def print_divergences_db_polis(self, comments_from_polis):
        divergent_comments = Comment.objects.exclude(id__in=set(comments_from_polis))
        self.stdout.write('Comments on our db but not on polis\':')
        print(list(divergent_comments.values_list('id', flat=True)))

    def print_final_report(self, conversations_not_found, comments_created,
                           comments_already_on_db):
        self.stdout.write('Conversas não encontradas:')
        print(set(conversations_not_found))
        self.stdout.write('Comentários criados:')
        print(set(comments_created))
        self.stdout.write('Comentários que já estavam no banco:')
        print(set(comments_already_on_db))
