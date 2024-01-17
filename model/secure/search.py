from core.svclog import svc_log_warn
from flask import request


class Search_secure(object):

    def check_search_text(self, not_secure_str_list: list, secure_content: str) -> bool:
        for char in not_secure_str_list:
            if char in secure_content:
                svc_log_warn(f"search content illegality, ip -> [{request.remote_addr}], keywords -> [{char}]")
                return True
        return False




