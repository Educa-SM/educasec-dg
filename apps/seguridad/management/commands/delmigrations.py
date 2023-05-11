import glob
import os

from django.core.management.base import BaseCommand


def __delete_migrations(handl):
    migrations = glob.glob(r'apps/**/migrations/[0-9][0-9][0-9][0-9]*.py')
    if len(migrations) > 0:
        print('Eliminando las siguientes migraciones:\n')
        for migration in migrations:
            try:
                print(f'- {migration}')
                os.remove(migration)
            except OSError as e:
                print(f'Error: {e.strerror}')
        handl.stdout.write(handl.style.SUCCESS(f'\n********** Se eliminó {len(migrations)} migraciones **********\n\n'))
    else:
        handl.stdout.write(handl.style.WARNING('\n********** No hay migraciones **********\n\n'))


def __delete_sqlite_db(handl):
    db = os.path.join('./db.sqlite3')
    if os.path.exists(db):
        try:
            print(db)
            os.remove(db)
            print()
            handl.stdout.write(handl.style.SUCCESS('\n********** Se eliminó la bd **********\n'))
        except OSError as e:
            print(f'Error: {e.strerror}')
    else:
        handl.stdout.write(handl.style.WARNING('********** No hay base de datos **********\n\n'))


def restart(handl):
    __delete_migrations(handl)
    __delete_sqlite_db(handl)


class Command(BaseCommand):
    help = 'Eliminar migraciones'

    def handle(self, *args, **options):
        restart(self)
