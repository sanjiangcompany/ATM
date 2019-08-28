from db import db_handler

# 提现接口
def withdraw_interface(username, money):
    # 1.把用户当前的金额取出做一次校验
    user_dic = db_handler.select(username)
    withdraw_money = money * 1.05
    if user_dic.get('balance') >= withdraw_money:
        # 对user_dic中的金额进行修改
        user_dic['balance'] -= withdraw_money
        # 记录流水
        msg = f'{username}提现{money}元成功!'
        user_dic['bank_flow'].append(msg)  # [].append(msg)
        # 保存修改过后的user_dic
        db_handler.save(user_dic)
        return True, msg
    return False, '你个*穷*, 请充值或者重新输入!'

# 还款接口
def repay_interface(username, money):
    # 1.获取用户信息
    user_dic = db_handler.select(username)

    user_dic['balance'] += money

    msg = f'{username}还款{money}元成功!'

    user_dic['bank_flow'].append(msg)

    db_handler.save(user_dic)

    return msg

# 转账接口
def transfer_interface(current_user, to_user, money):
    # 1.判断目标用户是否存在
    to_user_dic = db_handler.select(to_user)

    if not to_user_dic:
        return  False, '目标用户不存在, 你瞎呀!'


    # 2.判断当前用户余额是否足够
    current_user_dic = db_handler.select(current_user)

    if current_user_dic.get('balance') >= money:

        # 3.当前用户减钱,目标用户加钱
        current_user_dic['balance'] -= money
        to_user_dic['balance'] += money

        msg =  f'{current_user}向{to_user}转账{money}元成功!'

        # 记录流水
        current_user_dic['bank_flow'].append(msg)
        to_user_flow = f'{to_user}接收到{current_user}转账{money}元成功!'
        to_user_dic['bank_flow'].append(to_user_flow)

        db_handler.save(current_user_dic)
        db_handler.save(to_user_dic)

        return True, msg

    return False, '亲爱的用户,余额不足, 转账失败!'

# 查看流水接口
def check_flow_interface(username):
    user_dic = db_handler.select(username)

    return user_dic.get('bank_flow')

# 查看余额接口
def check_bal_interface(username):

    user_dic = db_handler.select(username)

    return user_dic.get('balance')

# 银行支付接口
def pay_interface(username, cost):
    user_dic = db_handler.select(username)

    if user_dic.get('balance') >= cost:

        user_dic['balance'] -= cost

        # 记录流水
        flow = f'{username}购物支付{cost}成功!'

        user_dic['bank_flow'].append(flow)


        db_handler.save(user_dic)

        return True

    return False













































