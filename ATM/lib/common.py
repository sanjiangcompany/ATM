from functools import wraps

def login_auth(func):  # check_balance
    from core import src  # 避免循环导入问题
    @wraps(func)
    def inner(*args, **kwargs):

        if src.user_info.get('user'):  # nick_sb
            # res = check_balance(*args, **kwargs)
            # return res

            res = func(*args, **kwargs)
            return res

        else:
            print('未登录,请去登录!')
            src.login()


    return inner