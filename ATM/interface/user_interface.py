from db import db_handler
from core import src

# 注册接口
def register_interface(username, password):
    # 查看用户是否存在
    user_dic = db_handler.select(username)

    if user_dic:
        return False, '用户名已存在!'  # return (False, '用户名已存在!')

    # 业务逻辑
    user_dic = {
        'username': username,
        'password': password,
        'balance': 15000,
        'bank_flow': [],
        'lock': False,
        'shop_car': {}
    }

    db_handler.save(user_dic)
    return True, f'{username}注册成功!'

# 登录接口
def login_interface(username, password):

    # 1.判断用户是否存在
    user_dic = db_handler.select(username)

    # 若用户不存在
    if not user_dic:
        return False, '用户不存在'

    # 2.校验密码是否正确
    if user_dic.get('password') == password:
        return True, f'{username}登录成功!'

    else:
        return False, '密码错误!'


# 注销接口
def logout_interface():

    src.user_info['user'] = None

    return '注销成功!'
