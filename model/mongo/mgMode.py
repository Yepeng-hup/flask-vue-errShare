from datetime import datetime
import traceback
from pymongo import DESCENDING
import threading

from .mongo import mg_col_es_text, mg_col_es_class, mg_col_es_label, mg_col_es_recovery, mg_col_es_login_info
from core.svclog import svc_log_info
from core.utils.utils import delete_not_text_img, delete_not_text_video


class Mg_mode(object):

    def insert_text(self, titel, user, class_list, label_list, text) -> bool:
        current_time = datetime.now()
        text_obj = {
            "titel": titel,
            "user": user,
            "class": class_list,
            "label": label_list,
            "date": current_time.strftime("%Y-%m-%d %H:%M:%S"),
            "text": text,
        }
        try:
            text_data = mg_col_es_text.insert_one(text_obj)
            svc_log_info(f"Inserted document ID: {text_data.inserted_id}, text name [{titel}]")
            return True
        except:
            print(traceback.format_exc())
            return False

    def insert_class(self, class_name) -> bool:
        current_time = datetime.now()
        class_obj = {
            "class": class_name,
            "date": current_time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        try:
            class_data = mg_col_es_class.insert_one(class_obj)
            svc_log_info(f"Inserted class ID: {class_data.inserted_id}, class name [{class_name}]")
            return True
        except:
            print(traceback.format_exc())
            return False

    def insert_label(self, label_name) -> bool:
        current_time = datetime.now()
        label_obj = {
            "label": label_name,
            "date": current_time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        try:
            label_data = mg_col_es_label.insert_one(label_obj)
            svc_log_info(f"Inserted label ID: {label_data.inserted_id}, label name [{label_name}]")
            return True
        except:
            print(traceback.format_exc())
            return False

    def insert_login_info(self, user_name) -> bool:
        current_time = datetime.now()
        info_obj = {
            "user": user_name,
            "date": current_time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        try:
            info_data = mg_col_es_login_info.insert_one(info_obj)
            svc_log_info(f"Inserted login user info ID: {info_data.inserted_id}")
            return True
        except:
            print(traceback.format_exc())
            return False

    def insert_recovery(self, titel, user, class_list, label_list, date, text) -> bool:
        rec_obj = {
            "titel": titel,
            "user": user,
            "class": class_list,
            "label": label_list,
            "date": date,
            "text": text,
        }
        try:
            rec_data = mg_col_es_recovery.insert_one(rec_obj)
            svc_log_info(f"recovery document ID: {rec_data.inserted_id}, text name [{titel}]")
            return True
        except:
            print(traceback.format_exc())
            return False

    def delete_text(self, titel) -> bool:
        # 删除文章
        try:
            rel = mg_col_es_text.delete_one({"titel": titel})
            if rel.acknowledged:
                svc_log_info(f"delete text success -> [{titel}]")
                return True
            return False
        except:
            print(traceback.format_exc())
            return False

    def delete_class(self, class_name) -> bool:
        # 删除分类
        try:
            rel = mg_col_es_class.delete_one({"class": class_name})
            if rel.acknowledged:
                svc_log_info(f"delete class success -> [{class_name}]")
                return True
            return False
        except:
            print(traceback.format_exc())
            return False

    def delete_label(self, label_name) -> bool:
        # 删除标签
        try:
            rel = mg_col_es_label.delete_one({"label": label_name})
            if rel.acknowledged:
                svc_log_info(f"delete label success -> [{label_name}]")
                return True
            return False
        except:
            print(traceback.format_exc())
            return False

    def delete_recovery_text(self, title) -> bool:
        #删除回收站里的数据，这里就是彻底删除了
        try:
            r = mg_col_es_recovery.find({"titel": title}, {"text": 1})
            text = r[0]['text']
            thread01 = threading.Thread(target=delete_not_text_img, args=(text,))
            thread02 = threading.Thread(target=delete_not_text_video, args=(text, ))
            thread01.start()
            thread02.start()
            rel = mg_col_es_recovery.delete_one({"titel": title})
            if rel.acknowledged:
                svc_log_info(f"delete recovery text success -> [{title}]")
                return True
            return False
        except:
            print(traceback.format_exc())
            return False

    def delete_login_info(self, user) -> bool:
        try:
            rel = mg_col_es_login_info.delete_one({"user": user})
            if rel.acknowledged:
                return True
            return False
        except:
            print(traceback.format_exc())
            return False

    def select_all_class(self, term) -> list:
        class_all_list = list()
        rel = mg_col_es_class.find({}, term)

        for result in rel:
            class_all_list.append(result)
        return class_all_list

    def select_all_label(self, term) -> list:
        label_all_list = list()
        rel = mg_col_es_label.find({}, term)

        for result in rel:
            label_all_list.append(result)
        return label_all_list

    def select_wz_num(self, term=None) -> int:
        wz_num_list = list()
        rel = mg_col_es_text.find(term)
        for result in rel:
            wz_num_list.append(result)
        return len(wz_num_list)

    def select_text(self, term0, term1) -> list:
        # 根据规则获取文章条目
        text_all_list = list()
        # rel = mg_col_es_text.find()     # 获取所有数据
        rel = mg_col_es_text.find(term0, term1)
        for result in rel:
            text_all_list.append(result)
        return text_all_list

    def select_recovery_text(self, term0, term1) -> list:
        # 获取回收站所有数据
        recovery_text_all_list = []
        rel = mg_col_es_recovery.find(term0, term1)   # 0是排除它，1是不排除
        for result in rel:
            recovery_text_all_list.append(result)
        return recovery_text_all_list

    def select_login_info(self) -> list:
        # 获取登录所有数据
        login_info_list = []
        # 0是排除它，1是不排除, limit是限制
        rel = mg_col_es_login_info.find({}, {'_id': 0}).sort("_id", DESCENDING).limit(20)
        for result in rel:
            login_info_list.append(result)
        return login_info_list

    def select_login_user(self, term0, term1) -> list:
        login_username = []
        rel = mg_col_es_login_info.find(term0, term1).limit(500)
        for i in rel:
            login_username.append(i['user'])
        return login_username


    def update_text(self, term, content) -> bool:
        new_update_value = {"$set": {"text": content}}
        rel = mg_col_es_text.update_one(term, new_update_value)
        return rel.raw_result['updatedExisting']
