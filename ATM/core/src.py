from interface import user_interface
from interface import bank_interface
from interface import shop_interface
from lib import common
user_info = {
    'user': None
}

# 注册,面条版
# def register():
#     while True:
#         # 视图层
#         username = input('请输入用户名:').strip()
#         password = input('请输入密码:').strip()
#         re_password = input('请确认密码:').strip()
#         if password == re_password:
#
#             # 业务逻辑
#             user_dic = {
#                 'username': username,
#                 'password': password,
#                 'balance': 15000,
#                 'bank_flow': [],
#                 'lock': False,
#                 'shop_car': {}
#             }
#
#             # 数据层
#             user_path = os.path.join(settings.DB_PATH, f'{username}.json')
#
#             with open(user_path, 'w', encoding='utf-8') as f:
#                 json.dump(user_dic, f)
#                 f.flush()
#
#             break
#
#         else:
#             print('两次密码不一致!')
#

# 注册
def register():
    while True:
        # 视图层
        username = input('请输入用户名:').strip()
        password = input('请输入密码:').strip()
        re_password = input('请确认密码:').strip()
        if password == re_password:
            # (False, '用户名已存在!')
            flag, msg = user_interface.register_interface(username, password)
            if flag:  # True
                print(msg)  # f'{username}注册成功!'
                break

            else:  # False
                print(msg)  # 用户名已存在!

        else:
            print('两次密码不一致!')


# 登录功能
def login():
    while True:
        username = input('请输入用户名:').strip()
        password = input('请输入密码:').strip()
        flag, msg = user_interface.login_interface(username, password)

        if flag:
            print(msg)
            user_info['user'] = username
            break

        else:
            print(msg)


# 查看余额
@common.login_auth
def check_balance():
    print('查看余额!')
    balance = bank_interface.check_bal_interface(user_info['user'])
    print(balance)


# 提现
@common.login_auth
def withdraw():
    while True:
        money = input('请输入提现金额:').strip()
        if not money.isdigit():
            print('必须是数字')
            continue

        money = int(money)

        flag, msg = bank_interface.withdraw_interface(user_info.get('user'), money)
        if flag:
            print(msg)
            break

        else:
            print(msg)


# 还款
@common.login_auth
def repay():
    while True:
        money = input('请输入还款金额:').strip()
        if not money.isdigit():
            print('必须是数字!')
            continue

        money = int(money)

        msg = bank_interface.repay_interface(user_info.get('user'), money)
        print(msg)
        break


# 转账功能
@common.login_auth
def transfer():
    while True:
        # 1.输入转账目标用户
        to_user = input('请输入转账目标用户:').strip()

        # 2.输入转账金额
        money = input('请输入转账金额:').strip()
        if not money.isdigit():
            print('金额必须是数字!')
            continue

        money = int(money)

        # 3.调用转账接口
        flag, msg = bank_interface.transfer_interface(user_info.get('user'), to_user, money)
        if flag:
            print(msg)
            break

        else:
            print(msg)

# 查看流水
@common.login_auth
def check_flow():
    flow_list = bank_interface.check_flow_interface(user_info['user'])
    if flow_list:
        for flow in flow_list:
            print(flow)

# 购物功能
@common.login_auth
def shopping():

    # 商品列表
    good_list = [
        # 商品名, 价格
        ['广东凤爪', 50],
        ['macbook', 18888],
        ['fj_公仔', 500],
        ['坦克', 10000]
    ]

    # 定义空的购物车
    shopping_car = {}  # {"good_name": 商品数量, key: value...}

    # 商品总价
    cost = 0

    # 获取当前用户金额
    user_bal = bank_interface.check_bal_interface(user_info.get('user'))

    while True:

        # 1.打印商品信息
        for index, goods in enumerate(good_list):
            print(index, goods)

        # 2.让用户输入商品编号
        choice = input('请输入商品编号 or q退出购买:').strip()

        if choice == 'q':
            break

        if not choice.isdigit():
            print("必须是数字!")
            continue
        choice = int(choice)

        # 3.拿到商品名称与价格
        good_name, good_price = good_list[choice]

        # 判断当前用户金额是否 >= 商品单价
        if user_bal >= good_price:

            # 4.添加购物车
            if good_name in shopping_car:
                shopping_car[good_name] += 1
            else:
                shopping_car[good_name] = 1

            # 5.合计总价
            cost += good_price

        else:
            print('用户金额不足!')


    if not cost:
        print('没有选择商品!')
        return

    # 6.开始结算, 先调用购物车接口, 再通过购物车接口去调用支付接口
    sure = input('是否确认购买, 输入y/n:').strip()
    if sure == 'y':
        flag, msg = shop_interface.shop_pay_interface(
            user_info.get('user'), shopping_car, cost)
        if flag:
            print(msg)

        else:
            print(msg)

    elif sure == 'n':
        # 添加购物车功能
        flag, msg = shop_interface.shopping_car_interface(
            user_info.get('user'), shopping_car)

        if flag:
            print(msg)

        else:
            print(msg)

# 查看购物车功能
@common.login_auth
def check_shop_car():
    shop_car = shop_interface.check_shop_car_interface(user_info.get('user'))
    print(shop_car)


def logout():
    if user_info.get('user'):
        msg = user_interface.logout_interface()
        print(msg)

func_dic = {
    '1': register,
    '2': login,
    '3': check_balance,
    '4': withdraw,
    '5': repay,
    '6': transfer,
    '7': check_flow,
    '8': shopping,
    '9': check_shop_car,
    '10': logout,
}


def run():
    while True:
        print('''
            1.注册
            2.登录
            3.查看额度
            4.提现
            5.还款
            6.转账
            7.查看流水
            8.购物功能
            9.查看购物车
            10.注销
            q.退出
        ''')

        choice = input('请输入功能编号: ').strip()

        if choice == 'q':
            break

        if choice not in func_dic:
            print('输入错误,请重新输入!')
            continue

        # func_dic[choice]()

        func_dic.get(choice)()






















