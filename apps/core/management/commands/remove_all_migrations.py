#!/usr/bin/env python
# -*-coding:utf-8-*-

from django.core.management.base import BaseCommand, CommandError
import glob
import os

class Command(BaseCommand):
    help = 'remove all migrations files'

    def handle(self, *args, **options):

        for filename in glob.glob('apps/*/migrations/*.py'):
            if os.path.basename(filename) == '__init__.py':
                pass
            else:
                print(f'remove {filename}')
                os.remove(filename)
        print('workdone')
