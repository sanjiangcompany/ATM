from interface import bank_interface
from db import db_handler

# 商城结算接口
def shop_pay_interface(username, shop_car, cost):
    # 1.调用银行支付接口
    flag = bank_interface.pay_interface(username, cost)
    # 获取当前用户
    user_dic = db_handler.select(username)
    # 2.判断是否支付成功!
    # 若支付成功,清空购物车
    if flag:
        user_dic['shop_car'] = {}
        db_handler.save(user_dic)
        return True, '购物并支付成功!'
    # 若支付失败,保存购物车
    else:
        user_dic['shop_car'] = shop_car
        db_handler.save(user_dic)
        return False, '支付失败, 保存购物车'


# 添加购物车接口
def shopping_car_interface(username, shop_car):
    # 1.获取当前用户
    user_dic = db_handler.select(username)

    # 2.添加购物车
    if shop_car:
        user_dic['shop_car'] = shop_car
        db_handler.save(user_dic)
        return True, '添加购物车成功!'

    else:
        return False, '购物车是空的!'


# 查看购物车接口
def check_shop_car_interface(username):
    user_dic = db_handler.select(username)

    return user_dic.get('shop_car')