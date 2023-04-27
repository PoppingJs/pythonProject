def test_flow(login):
    url = "http://mall.lemonban.com:8107/prod/prodInfo?prodId=17134"
    res = login.request("get", url)
    print(res.json())



