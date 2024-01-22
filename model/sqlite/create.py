import traceback
import sys

from model.sqlite.sqlite import cursor
from model.sqlite.select import Select_tables
from core.svclog import svc_log_info, svc_log_err
from model.secure.pwd import Pwd_encryption_decrypt

s = Select_tables()
p = Pwd_encryption_decrypt()


def create_tables():
    table_list = ["users", "test"]
    db_exists_table = s.show_all_table()

    if len(db_exists_table) == 0:
        try:
            cursor.execute(
                '''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, role TEXT, password TEXT, phone TEXT, mailbox TEXT)''')
            svc_log_info("table [users] create ok.")
            return
        except:
            svc_log_err("table [users] create fail.")
            print(traceback.format_exc())
    else:

        for table in table_list:
            if table in db_exists_table[0]:
                pass
            elif table == "users":
                try:
                    cursor.execute(
                        '''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, role TEXT, password TEXT, phone TEXT, mailbox TEXT)''')
                    svc_log_info("table [users] create ok.")
                except:
                    svc_log_err("table [users] create fail.")
                    print(traceback.format_exc())
            # elif table == "test":
            #     print("create test")
            else:
                pass
    return


def create_init_user():
    rel = s.show_select_rel("SELECT username,role,phone,mailbox  FROM users WHERE username=\"root\"")

    if len(rel) == 0:
        try:
            cursor.execute("INSERT INTO users (username, role, password, phone, mailbox) VALUES (?, ?, ?, ?, ?)",
                           ("root", "admin",
                            p.encryption("123456"),
                            "000-0000-0000", "000-0000-0000@0.0"))
            svc_log_info("Administrator user initialization success")
        except:
            svc_log_err("Administrator user initialization fail")
            print(traceback.format_exc())
            sys.exit(1)
    return
