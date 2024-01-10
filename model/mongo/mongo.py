import pymongo

from core.conf import mg_host, mg_port, mg_user, mg_password, mg_name


client = pymongo.MongoClient(f"mongodb://{mg_user}:{mg_password}@{mg_host}:{mg_port}/?authSource={mg_name}")
db = client[mg_name]

# 选择集合, 集合列表
mg_col_es_text = db['es_text']
mg_col_es_label = db['es_label']
mg_col_es_class = db['es_class']
mg_col_es_recovery = db['es_recovery']
mg_col_es_login_info = db['es_login_info']



