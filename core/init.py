from model.sqlite.create import create_tables, create_init_user


def check_conn_mongo():
    pass


class Inits(object):

    def init_mongo(self):
        pass

    def init_sqlite(self):
        create_tables()

    def init_user_and_role(self):
        create_init_user()
