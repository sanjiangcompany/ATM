import json
import os
from conf import settings


# 查看数据
def select(username):

    user_path = os.path.join(settings.DB_PATH,
                            f'{username}.json')
    if os.path.exists(user_path):
        with open(user_path, 'r', encoding='utf-8') as f:
            user_dic = json.load(f)
            return user_dic


# 保存数据
def save(user_dic):
    # 数据层
    # 拼接用户.json文件路径
    user_path = os.path.join(settings.DB_PATH,
                             f'{user_dic.get("username")}.json')

    with open(user_path, 'w', encoding='utf-8') as f:
        json.dump(user_dic, f)
        f.flush()






