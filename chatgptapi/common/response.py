from flask import jsonify


def result(status='Success', msg='', data=None):
    res = {
        "status": status,
        "msg": msg,
    }
    if data:
        res['data'] = data
    return jsonify(res)


def ok():
    return result()


def ok_with_data(data):
    return result(data=data)


def fail():
    return result(status='Fail', msg='')


def fail_with_msg(msg):
    return result(status='Fail', msg=msg)


def rate_limit():
    return result(status='Fail', msg='请求速度太快')


def unauth():
    return result(status='Unauthorized', msg='无访问权限')





