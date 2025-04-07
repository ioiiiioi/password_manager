import json
import requests
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient

class LiveClient:
    def __init__(self, token=None):
        self.base_url = "https://backend.accel.id"
        self.token = None if not token else f"Bearer {token}"

    def post(self, url, data, headers, files=None, **extra):
        url = self.base_url + url
        data, file = self.dict_to_json_parser(data)
        return self.request(
            method='POST',
            url=url,
            data=data,
            headers=headers,
            files=files if not file else file
        )

    def put(self, url, headers, data=None, files=None, **extra):
        url = self.base_url + url
        data, file = self.dict_to_json_parser(data)
        return self.request(
            method='PUT',
            url=url,
            data=data,
            headers=headers,
            files=files if not file else file
        )

    def patch(self, url, headers, data=None, files=None, **extra):
        url = self.base_url + url
        data, file = self.dict_to_json_parser(data)
        return self.request(
            method='PATCH',
            url=url,
            data=data,
            headers=headers,
            files=files if not file else file
        )

    def delete(self, url, headers, data=None, files=None, **extra):
        url = self.base_url + url
        data = self.dict_to_json_parser(data)
        return self.request(
            method='DELETE',
            url=url,
            data=data,
            headers=headers,
            files=files
        )
    
    def get(self, url, headers, data=None, files=None, **extra):
        url = self.base_url + url
        data = self.dict_to_json_parser(data)
        return self.request(
            method='DELETE',
            url=url,
            data=data,
            headers=headers,
            files=files
        )

    def dict_to_json_parser(self, data=None):
        file = None
        if isinstance(data, dict):
            data = json.dumps(data)
        for key, val in data.items():
            if isinstance(val,SimpleUploadedFile):
                data.pop(key)
                file[key] = val.content
            if isinstance(val, list):
                for obj in val:
                    if isinstance(obj, SimpleUploadedFile):
                        data.pop(key)
        return data, file

    def request(self, method, url, headers, data=None, files=None):
        if self.token:
            headers['Authorization'] = self.token
        return requests.request(
            method=method, 
            url=url, 
            headers=headers, 
            data=data,
            files=files
        )

class CustomAPIClient(APIClient):
    print_result = True
    
    def post(self, path, data=None, format=None, content_type=None, follow=False, **extra):
        if extra['headers']['Content-Type'] == 'application/json':
            format = 'json'
        resp = super().post(path, data, format, content_type, follow, **extra)
        if self.print_result:
            print("================================================================")
            print(json.dumps(resp.json(), indent=4))
            print("================================================================\n")
        return resp

    def put(self, path, data=None, format=None, content_type=None, follow=False, **extra):
        if extra['headers']['Content-Type'] == 'application/json':
            format = 'json'
        resp = super().put(path, data, format, content_type, follow, **extra)
        if self.print_result:
            print("================================================================")
            print(json.dumps(resp.json(), indent=4))
            print("================================================================\n")
        return resp

    def patch(self, path, data=None, format=None, content_type=None, follow=False, **extra):
        if extra['headers']['Content-Type'] == 'application/json':
            format = 'json'
        resp = super().patch(path, data, format, content_type, follow, **extra)
        if self.print_result:
            print("================================================================")
            print(json.dumps(resp.json(), indent=4))
            print("================================================================\n")
        return resp
    
    def get(self, path, data=None, follow=False, **extra):
        resp = super().get(path, data, follow, **extra)
        if self.print_result:
            print("================================================================")
            print(json.dumps(resp.json(), indent=4))
            print("================================================================\n")
        return resp

    def delete(self, path, data=None, format=None, content_type=None, follow=False, **extra):
        resp = super().delete(path, data, format, content_type, follow, **extra)
        if self.print_result:
            print("================================================================")
            print(json.dumps(resp.json(), indent=4))
            print("================================================================\n")
        return resp

class BaseTestCase(TestCase):
    def setUp(self):
        self.client = CustomAPIClient()
        self.headers = {
            "Content-Type":"application/json"
        }
        self.server = "local"
        
    def unauthorized_call(self):
        if self.server == 'local':
            return self.client
        else:
            return LiveClient()

    def authorized_call(self, user=None, token=None):
        if self.server == 'local':
            if token:
                self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
            # token = user.get_tokens_for_user()['access']
            # self.refresh = user.get_tokens_for_user()['refresh']
            return self.client
        else:
            return LiveClient(token)