def login(username=None, password=None):
    """改成访问接口，得到接口数据的函数"""
    if username is None or password is None:
        return {"code": "400", "msg": "用户名或密码为空"}
    if username == 'yuz' and password == 123:
        return {"code": "200", "msg": "登录成功"}
    return {"code": "300", "msg": "用户名或密码错误"}

