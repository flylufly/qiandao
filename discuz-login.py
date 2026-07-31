import re
import requests

class DiscuzLogin:
proxies = {
'http': '[http://127.0.0.1:1080](https://link.wtturl.cn/?target=http%3A%2F%2F127.0.0.1%3A1080&scene=im&aid=497858&lang=zh)',
'https': '[https://127.0.0.1:1080](https://link.wtturl.cn/?target=https%3A%2F%2F127.0.0.1%3A1080&scene=im&aid=497858&lang=zh)'
}

def **init**(self, hostname, username, password, questionid='0', answer=None, proxies=None):
self.session = requests.session()
self.hostname = hostname
self.username = username
self.password = password
self.questionid = questionid
self.answer = answer
if proxies:
self.proxies = proxies

@classmethod
def user\_login(cls, hostname, username, password, questionid='0', answer=None, proxies=None):
user = DiscuzLogin(hostname, username, password, questionid, answer, proxies)
user.login()

def form\_hash(self):
rst = self.session.get(f'https://{self.hostname}/member.php?mod=logging&action=login').text
loginhash = re.search(r'<div id="main\_messaqge\_(.+?)">', rst).group(1)
formhash = re.search(r'<input type="hidden" name="formhash" value="(.+?)" />', rst).group(1)
return loginhash, formhash</div>

def login(self):
loginhash, formhash = self.form\_hash()
login\_url = f'https://{self.hostname}/member.php?mod=logging&action=login&loginsubmit=yes&loginhash={loginhash}&inajax=1'
form\_data = {
'formhash': formhash,
'referer': f'https://{self.hostname}/',
'loginfield': self.username,
'username': self.username,
'password': self.password,
'questionid': self.questionid,
'answer': self.answer,
'cookietime': 2592000
}
login\_rst = self.session.post(login\_url, proxies=self.proxies, data=form\_data)
if self.session.cookies.get('xxzo\_2132\_auth'):
print(f'Welcome {self.username}!')
else:
raise ValueError('Verify Failed! Check your username and password!')

if **name** == '**main**':
DiscuzLogin.user\_login('hostname', 'username', 'password')
