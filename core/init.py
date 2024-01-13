from model.sqlite.create import create_tables, create_init_user
from core.svclog import svc_log_info


class Inits(object):

    def init_sqlite(self):
        svc_log_info("init sqlite db ....")
        create_tables()
        svc_log_info("init sqlite db ok")

    def init_user_and_role(self):
        svc_log_info("init user and role ....")
        create_init_user()
        svc_log_info("init user and role ok")


