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
            votes_from_polis = []
            conversations_not_found = []
            comments_not_found = []
            votes_created = []
            votes_already_on_db = []
            print("A importação pode demorar alguns minutos. Importando...")
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
                    conversations_not_found.append(conversation_slug)
                    continue

                try:
                    comment = Comment.objects.get(polis_id=comment_id,
                                                  conversation=conversation.id)
                except Comment.DoesNotExist:
                    comments_not_found.append(comment_id)
                    continue

                try:
                    vote = Vote.objects.get(author=user, comment=comment)
                except Vote.DoesNotExist:
                    with transaction.atomic():
                        vote = Vote.objects.create(comment=comment, value=vote,
                                                   author=user,
                                                   created_at=created)
                    votes_from_polis.append(vote.id)
                    votes_created.append(vote.id)
                    count += 1
                else:
                    votes_from_polis.append(vote.id)
                    votes_already_on_db.append(vote.id)

            self.stdout.write('Total de votos criados: ' + str(count))
            self.print_final_report(conversations_not_found, votes_created,
                                    comments_not_found, votes_already_on_db)
            self.print_divergences_db_polis(votes_from_polis)

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

    def print_divergences_db_polis(self, votes_from_polis):
        divergent_votes = Vote.objects.exclude(id__in=set(votes_from_polis))
        self.stdout.write('Votes on django db but not on polis\':')
        print(list(divergent_votes.values_list('id', flat=True)))

    def print_final_report(self, conversations_not_found, votes_created,
                           comments_not_found, votes_already_on_db):
        self.stdout.write('Conversas não encontradas:')
        print(set(conversations_not_found))
        self.stdout.write('Comentários não encontradas:')
        print(set(comments_not_found))
        self.stdout.write('Votos criados:')
        print(set(votes_created))
        self.stdout.write('Votos que já estavam no banco:')
        print(set(votes_already_on_db))
