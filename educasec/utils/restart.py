import glob
import os


def __delete_migrations():
    migrations = glob.glob('apps/**/migrations/[0-9][0-9][0-9][0-9]*.py')
    if len(migrations) > 0:
        print('Eliminando las siguientes migraciones:\n')
        for migration in migrations:
            try:
                print(migration)
                os.remove(migration)
            except OSError as e:
                print(f'Error: {e.strerror}')
        print(
            f'\n********** Se eliminó {len(migrations)} migraciones **********\n\n')
    else:
        print('\n********** No hay migraciones **********\n\n')


def __delete_sqlite_db():
    db = os.path.join('./db.sqlite3')
    if os.path.exists(db):
        try:
            print(db)
            os.remove(db)
            print('\n********** Se eliminó la bd **********\n')
        except OSError as e:
            print(f'Error: {e.strerror}')
    else:
        print('********** No hay base de datos **********\n\n')


def restart():
    __delete_migrations()
    __delete_sqlite_db()


''' ######################### '''
''' ########## Run ########## '''
''' ######################### '''
restart()
