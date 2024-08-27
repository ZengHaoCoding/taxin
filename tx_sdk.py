import requests
import json

api = "http://api.my531.com"
# 必须配置
userName = ""
passWord = ""


class TX(object):

    def __init__(self):
        self.userName = userName
        self.passWord = passWord
        self.token = None
        self.phone_number = None
        self.headers = {
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
        }
        self.project_id = None
        self.login()

    def login(self, newUserName=None, newPassWord=None):
        if newUserName is not None and newPassWord is not None:
            self.userName = str(newUserName)
            self.passWord = str(newPassWord)
        try:
            url = api + f'/Login/?username={self.userName}&password={self.passWord}&type=json'
            response = requests.get(url=url, headers=self.headers)
            response = json.loads(response.text)
            if response.get("stat"):
                self.token = response.get("data").get("token")
                return True
        except Exception as e:
            print("【他信SDK】登录失败")
        return False

    def get_number(self, project_id, number=None):
        self.project_id = project_id
        try:
            if self.token is None:
                print("【他信SDK】token为空，请先登录。")
                return False
            url = api + f'/GetPhone/?token={self.token}&id={self.project_id}&type=json'
            if number:
                url += "&phone=" + str(number)
            else:
                url += "&card=2"
            response = requests.get(url=url, headers=self.headers)
            response = json.loads(response.text)
            if response.get("stat"):
                self.phone_number = response.get("data")
                return True
        except Exception as e:
            print("【他信SDK】手机号码获取失败")
        return False

    def get_msg(self):
        try:
            url = api + f'/GetMsg/?token={self.token}&id={self.project_id}&phone={self.phone_number}&type=json'
            response = requests.get(url=url, headers=self.headers)
            response = json.loads(response.text)
            if response.get("stat"):
                self.cancel_number()
                return response.get("data")
        except Exception as e:
            print("【他信SDK】短信获取失败")
        return None

    def cancel_number(self):
        try:
            url = api + f'/Cancel/?token={self.token}&id={self.project_id}&phone={self.phone_number}'
            response = requests.get(url=url, headers=self.headers)
            response = json.loads(response.text)
            if response.get("stat"):
                return True
        except Exception as e:
            print("【他信SDK】手机号释放失败")
        return False


if __name__ == '__main__':
    tx = TX()
    
    # 下面这个login不是必须调用，开发者一般有固定的用户名与密码，只一开始配置好就行
    # tx.login("新用户名", "新密码")

    # “111”为项目id
    tx.get_number(111)
    while True:
        msg = tx.get_msg()
        if msg:
            # 使用msg验证码进行下一步操作
            break
