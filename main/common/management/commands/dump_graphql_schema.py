"""
    GraphQL Schema dump command
    ===========================

    This command allows to dump the main Graphene GraphQL schema into a GraphQL file.

"""

from django.core.management.base import BaseCommand
from graphene_django.settings import graphene_settings
from graphql.utils import schema_printer


class Command(BaseCommand):
    """ Dumps Graphene main GraphQL schema in a single GraphQL file. """

    help = 'Dump Graphene main GraphQL schema in a single GraphQL file.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-o', '--output',
            help='Specifies a file to which the output is written.'
        )

    def handle(self, *args, **options):
        """ Performs the command actions. """
        output = open(options['output'], 'w') if options['output'] else self.stdout
        output.write(schema_printer.print_schema(graphene_settings.SCHEMA))
        if options['output']:
            self.stdout.write(
                self.style.MIGRATE_HEADING(
                    'Successfully dumped GraphQL schema to {}'.format(options['output'])
                )
            )
