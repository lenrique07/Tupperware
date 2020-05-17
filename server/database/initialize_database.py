import sqlite3
import sys

from sqlalchemy.engine import create_engine
from configparser import ConfigParser

from ..usuarios.scripts import insertions as user_insertions
from ..mcatalogo.scripts import insertions as mcatalogo_insertions
from ..configuracion.scripts import insertions as mconfiguracion_insertions



from server.database import connection
from .models import Base


def main():
    reload_db()
    user_insertions()
    mcatalogo_insertions()
    mconfiguracion_insertions()

    print('Database created/updated correctly!')


def reload_db():
    config = ConfigParser()
    config.read('settings.ini')
    db_url = config['Database']['url']
    connection.db_url = config['Database']['url']
    if 'sqlite' in db_url:
        dbname = db_url.split('///')[1]
        sqlite3.connect(dbname)
    engine = create_engine(config['Database']['url'])
    Base.metadata.drop_all(engine, checkfirst=True)
    Base.metadata.create_all(engine, checkfirst=True)


if __name__ == '__main__':
    sys.exit(int(main() or 0))
