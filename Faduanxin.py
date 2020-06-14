# -*- coding: utf-8 -*-
import json
import requests
import time
import hashlib
import random
from main import *

def Yanzhengma(number):
	# 输入：字符串形式的手机号  输出：字符串形式的验证码
	random = 104556
	yzm = get_code()
	stryzm = "【Kewail】尊敬的客户您好。您本次的验证码为：" + yzm
	url = "https://live.kewail.com/sms/v1/sendsinglesms?accesskey={0}&random={1}".format("5ee4dca3efb9a35396a06ca8",
																						 random)
	print(url)
	dt = "2019-01-03 20:29:29"
	time_unix = int(time.mktime(time.strptime(dt, "%Y-%m-%d %H:%M:%S")))
	print(time_unix)
	print(type(time_unix))
	sig_not_sha = "secretkey={0}&random={1}&time={2}&mobile={3}".format("0b370e5eaf0044fa98034f7ccf270c58", random,
																		str(time_unix), number)
	hash = hashlib.sha256()
	hash.update(sig_not_sha.encode("utf-8"))
	sig = hash.hexdigest()
	print(sig)
	data = {
		"tel": {
			"nationcode": "86",
			"mobile": number
		},
		"type": 0,
		"msg": stryzm,
		"sig": sig,
		"time": time_unix,
		"extend": "",
		"ext": ""
	}
	print(data)
	f = requests.post(url, json=data)

	print(f.text)

	return yzm

def get_code():
	code_list = []
	for i in range(10):   # 0~9
		code_list.append(str(i))
	for i in range(65, 91):  # A-Z
		code_list.append(chr(i))
	for i in range(97, 123):  # a-z
		code_list.append(chr(i))
	code = random.sample(code_list,6)   #随机取6位数
	code_num = ''.join(code)
	return code_num

def Tishi(tenant, room):
	# 输入：字符串形式的手机号  输出：字符串形式的验证码
	random = 104556

	number = tenant.phoneNumber

	if number == None:
		return False

	stryzm = "【青年租房管理系统】" + tenant.tenantName + "您好，您的合同中关于" + room.roomName + "房屋的合同将于" + room.enddate + "到期。如果您希望进行续租，请尽快办理缴费！"
	url = "https://live.kewail.com/sms/v1/sendsinglesms?accesskey={0}&random={1}".format("5ee4dca3efb9a35396a06ca8",
																						 random)
	print(url)
	dt = "2019-01-03 20:29:29"
	time_unix = int(time.mktime(time.strptime(dt, "%Y-%m-%d %H:%M:%S")))
	print(time_unix)
	print(type(time_unix))
	sig_not_sha = "secretkey={0}&random={1}&time={2}&mobile={3}".format("0b370e5eaf0044fa98034f7ccf270c58", random,
																		str(time_unix), number)
	hash = hashlib.sha256()
	hash.update(sig_not_sha.encode("utf-8"))
	sig = hash.hexdigest()
	print(sig)
	data = {
		"tel": {
			"nationcode": "86",
			"mobile": number
		},
		"type": 0,
		"msg": stryzm,
		"sig": sig,
		"time": time_unix,
		"extend": "",
		"ext": ""
	}
	print(data)
	f = requests.post(url, json=data)

	print(f.text)

	return True
