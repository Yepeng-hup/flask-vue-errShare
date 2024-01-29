login_err_num_list = []


def delete_err_list_login_ok_user(user_name):
    # if login_err_num_list.count(user_name) < 6:
    while user_name in login_err_num_list:
        login_err_num_list.remove(user_name)


class Login_secure(object):

    def login_err_num_user_block(self, user_name) -> dict:
        login_err_num_list.append(user_name)
        err_num = login_err_num_list.count(user_name)
        return {"user_name": user_name, "err_num": err_num}
