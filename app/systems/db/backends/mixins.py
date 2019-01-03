from django.conf import settings
from django.core.management import call_command

from systems.db import manager


class DatabaseRecoveryMixin(object):
    
    def load(self, data, encrypted = True):
        if settings.DEBUG:
            call_command('makemigrations', interactive = False, verbosity = 0)
        
        call_command('migrate', interactive = False, verbosity = 0)
        manager.DatabaseManager(self.alias).load(data, encrypted)
    
    def load_file(self, file_path = None, encrypted = True):
        if settings.DEBUG:
            call_command('makemigrations', interactive = False, verbosity = 0)
        
        call_command('migrate', interactive = False, verbosity = 0)
        manager.DatabaseManager(self.alias).load_file(file_path, encrypted)


    def save(self, package = manager.PACKAGE_ALL_NAME, encrypted = True):
        manager.DatabaseManager(self.alias).save(package, encrypted)
        
    def save_file(self, package = manager.PACKAGE_ALL_NAME, file_path = None, encrypted = True):
        manager.DatabaseManager(self.alias).save_file(package, file_path, encrypted)
