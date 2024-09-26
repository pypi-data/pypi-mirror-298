#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only

import json
import os
import re
from urllib.parse import urljoin

import requests


class ApiClient:
    def __init__(self, base_url, username, password, token_url=None):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.token_url = token_url if token_url is not None else "api/token/"
        self.token = self.get_token()
        self.header = self.get_header()

    def get_token(self):
        auth_endpoint = f"{self.base_url}/{self.token_url}"

        credentials = {
            "username": self.username,
            "password": self.password
        }
        headers = {"content-type": "application/x-www-form-urlencoded; charset=UTF-8"}
        res = requests.post(url=auth_endpoint, data=credentials, headers=headers).json()
        jwt_token = res["data"]["access"]
        return jwt_token

    def get_header(self):
        header = {
            "Authorization": f"JWT {self.token}",
            "Content-Type": "application/json"
        }
        return header

    def post(self, url, data=None, json=None):
        response = requests.post(url, headers=self.header, data=data, json=json)
        return response


class SendMe:

    def __init__(
            self,
            base_url,
            username,
            password,
            custom_api=None
    ):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.custom_api = custom_api if custom_api is not None else "api/youqu/yqresult/"
        self.api = ApiClient(
            base_url=self.base_url,
            username=self.username,
            password=self.password,
        )

    def get_remote_json_data(self, json_path):
        print("当前路径：", os.path.abspath("."))
        json_res = {}
        for root, dirs, files in os.walk(json_path):
            for file in files:
                if file.startswith("last_") and file.endswith("result.json"):
                    client_ip = re.findall(r"/\d+_(\d+\.\d+\.\d+\.\d+)_.*?", root)
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8") as f:
                        json_data = json.load(f)
                        if client_ip:
                            json_res[client_ip[0]] = json_data
        if not json_res:
            print("json data not found", json_res)
        return json_res

    def backfill(self, json_backfill_task_id, json_path=None):
        json_path = json_path if json_path is not None else "./report/"
        json_res = self.get_remote_json_data(json_path)
        tpl = {
            "case": "",
            "task": json_backfill_task_id,
            "result": "",
            "is_closed": "",
            "module": "",
            "longrepr": "",
            "pm_ip": "",
            "owner": "",
        }
        for _ip, res in json_res.items():
            test_cases = res.get("test_cases")
            for case_py in test_cases:
                case_py_path = test_cases.get(case_py).get("py_path")
                module, *_ = case_py_path.split("/")
                tpl["case"] = case_py_path
                case_id = re.findall(r"test_.*?_(\d+)", case_py)
                if case_id:
                    tpl["case"] = case_id[0]
                tpl["module"] = module
                result = test_cases.get(case_py).get("py_outcome")
                tpl["result"] = "fail" if result == "failed" else "pass"
                tpl["is_closed"] = False if result == "failed" else True
                tpl["pm_ip"] = _ip
                res = self.api.post(
                    url=urljoin(self.base_url, self.custom_api),
                    json=tpl
                )
                print(self.custom_api, res, tpl)


if __name__ == '__main__':
    SendMe(
        base_url="http://10.20.52.223:8000",
        username="AT",
        password="123456",
    ).backfill("fec78d932921482298350e976798ad3b")
