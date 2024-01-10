from model.sqlite.sqlite import cursor


class Select_tables(object):

    def show_all_table(self):
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        rel = cursor.fetchall()
        return rel

    def show_select_rel(self, sql):
        cursor.execute(sql)
        rel = cursor.fetchall()
        return rel

