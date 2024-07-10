import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def _drop_database(**connection_params):
    database_name = 'test_' + connection_params['NAME']
    conn = psycopg2.connect(
        database='postgres',
        user=connection_params['USER'],
        password=connection_params['PASSWORD'],
        host=connection_params['HOST'],
        port=connection_params['PORT'],
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(f'DROP DATABASE IF EXISTS "{database_name}"')
    conn.close()
