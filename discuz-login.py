import re
import requests


class DiscuzLogin:
    proxies = {
        'http': 'http://127.0.0.1:1080',
        'https': 'https://127.0.0.1:1080'
    }

    def __init__(self, hostname, username, password, questionid='0', answer=None, proxies=None):
        self.session = requests.Session()
        # 模拟浏览器头
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': f'https://{hostname}'
        })

        self.hostname = hostname
        self.username = username
        self.password = password
        self.questionid = questionid
        self.answer = answer
        if proxies:
            self.proxies = proxies

    @classmethod
    def user_login(cls, hostname, username, password, questionid='0', answer=None, proxies=None):
        user = cls(hostname, username, password, questionid, answer, proxies)
        user.login()

    def form_hash(self):
        url = f'https://{self.hostname}/member.php?mod=logging&action=login'
        try:
            rsp = self.session.get(url, proxies=self.proxies, timeout=10, allow\_redirects=False)
            rsp.raise_for_status()
            rst = rsp.text
        except Exception as e:
            raise RuntimeError(f"获取登录页失败: {e}")

        # 修正你原来的拼写错误 main_messaqge → main_message
        loginhash = re.search(r'<div id="main_message_(.+?)">', rst)
        formhash = re.search(r'<input.*?name="formhash".*?value="([^"]+)"', rst, re.S)

        if not loginhash or not formhash:
            raise RuntimeError("页面结构已变，无法提取 loginhash / formhash")

        return loginhash.group(1), formhash.group(1)

    def login(self):
        loginhash, formhash = self.form_hash()

        login_url = (f'https://{self.hostname}/member.php?mod=logging&action=login'
                     f'&loginsubmit=yes&loginhash={loginhash}&inajax=1')

        form_data = {
            'formhash': formhash,
            'referer': f'https://{self.hostname}/',
            'username': self.username,
            'password': self.password,
            'questionid': self.questionid,
            'answer': self.answer,
            'cookietime': 2592000,
            'loginfield': 'username'  # 固定为 username 更稳
        }

        try:
            login_rst = self.session.post(
                login_url,
                data=form_data,
                proxies=self.proxies,
                timeout=10
            )
        except Exception as e:
            raise RuntimeError(f"登录请求失败: {e}")

        # 通用判断，不写死 cookie 名
        if 'login' not in login_rst.url and ('欢迎' in login_rst.text or '退出' in login_rst.text):
            print(f'Welcome {self.username}!')
        else:
            raise ValueError('Verify Failed! 用户名/密码/安全提问错误')


if __name__ == '__main__':
    # 替换成你真实的域名、账号、密码
    DiscuzLogin.user_login(
        hostname='your.domain.com',
        username='yourname',
        password='yourpass'
    )
