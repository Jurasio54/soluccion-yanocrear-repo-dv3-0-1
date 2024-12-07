import requests
from bs4 import BeautifulSoup
import json

class DVUpload:

    def __init__(self,user,passw,host,repo=None):
        self.user = user
        self.passw = passw
        self.host = host
        self.login_url = self.host + "login/signIn"
        self.sess = requests.Session()
        self.csrfToken = ""        
        self.repo = repo
        self.headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; 5002B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36"
        }
        
    def login(self):
        try:
            response = self.sess.get(self.login_url, headers=self.headers)
            html = BeautifulSoup(response.text, 'html.parser')
            csrfToken = html.find("input", attrs={"name": "csrfToken"})["value"]
            data = {"username": self.user,"password": self.passw,"csrfToken": csrfToken}		
            self.csrfToken = csrfToken
            login_post = self.sess.post(self.login_url,data=data,headers=self.headers)
            if login_post.url != self.login_url:
                print("Inició sesión")
            else:
                print("Usuario o contraseña incorrecta")
        except Exception as e:
            print(str(e))
    
    def make_repo(self):
        try:
            data = {
                'csrfToken': self.csrfToken,
                'submissionChecklist': '1',
                'locale': 'es_ES',
                'sectionId': '1',
                'checklist-1': '1',
                'checklist-2': '1',
                'checklist-3': '1',
                'checklist-4': '1',
                'checklist-5': '1',
                'checklist-6': '1',
                'commentsToEditor': '',
                'userGroupId': '14',
                'copyrightNoticeAgree': '1',
                'privacyConsent': '1',
                'submitFormButton': '' 
            }
            response = self.sess.post(f"{self.host}submission/saveStep/1",data=data,headers=self.headers)
            json_response = json.loads(response.text)
            load = json_response["events"][0]["data"]
            repo = load.split("submissionId=")[1].split("#")[0]
            self.repo = repo
            return repo
        except Exception as e:
            print(str(e))
        
    def upload(self,file):
        try:
            self.headers["X-Csrf-Token"] = self.csrfToken
            data = {"name[es_ES]": file, "fileStage": 2}
            files = {"file": open(file, "rb")}        
            response = self.sess.post(f"{self.host}api/v1/submissions/{self.repo}/files",files=files,data=data,headers=self.headers)        
            json_response = json.loads(response.text)
            print(json_response["url"])
            return json_response["url"]
        except Exception as e:
            print(str(e))