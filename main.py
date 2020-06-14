# -*- coding:utf-8 -*-
#!coding=utf-8
import sys
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

import uuid            
from flask import Flask, request, json, Response            
from flask_sqlalchemy import SQLAlchemy            
from sqlalchemy import or_, and_, not_  
# from sshMethod import *  

import config            

app = Flask(__name__)            
app.config.from_object(config)            
db = SQLAlchemy(app)            

class Tenant(db.Model):            
	__tablename__ = "Tenant"
	tenantID = db.Column(db.Integer, primary_key = True, nullable = False)
	tenantName = db.Column(db.String(40), nullable = False)
	phoneNumber = db.Column(db.String(11), nullable = False)
	password = db.Column(db.String(40), nullable = False)
	isMale = db.Column(db.String(40), nullable = False)
	age = db.Column(db.String(40), nullable = False)
	job = db.Column(db.String(40), nullable = False)
	city = db.Column(db.String(40), nullable = False)
	def __init__(self, tid, tna, pn, psw, im, age, job, cit):
		self.tenantID = tid
		self.tenantName = tna
		self.phoneNumber = pn
		self.password = psw
		self.isMale = im
		self.age = age
		self.job = job
		self.city = cit

class Complain(db.Model):            
	__tablename__ = "Complain"
	tenantID = db.Column(db.Integer, db.ForeignKey("Tenant.tenantID"), primary_key = True, nullable = False)
	roomID = db.Column(db.Integer, db.ForeignKey("Room.roomID"), primary_key = True, nullable = False)
	serverID = db.Column(db.Integer, db.ForeignKey("Server.serverID"), nullable = False)
	content = db.Column(db.String(300), nullable = False)
	reply = db.Column(db.String(300))
	ishandled = db.Column(db.Boolean, default = False)
	def __init__(self, tid, rid, sid, ct):
		self.tenantID = tid
		self.roomID = rid
		self.serverID = sid
		self.content = ct
		self.ishandled = False

class Repair(db.Model):            
	__tablename__ = "Repair"
	tenantID = db.Column(db.Integer, db.ForeignKey("Tenant.tenantID"), primary_key = True, nullable = False)
	roomID = db.Column(db.Integer, db.ForeignKey("Room.roomID"), primary_key = True, nullable = False)
	content = db.Column(db.String(300), nullable = False)
	serverID = db.Column(db.Integer, db.ForeignKey("Server.serverID"), nullable = False)
	ishandled = db.Column(db.Boolean, default = False)
	def __init__(self, tid, rid, ct, sid):
		self.tenantID = tid
		self.roomID = rid
		self.serverID = sid
		self.content = ct
		self.ishandled = False

class Room(db.Model):            
	__tablename__ = "Room"
	roomID = db.Column(db.Integer, primary_key = True, nullable = False)
	roomName = db.Column(db.String(40), nullable = False)
	available = db.Column(db.Integer, nullable = False)
	capacity = db.Column(db.Integer, nullable = False)
	isLongRent = db.Column(db.Boolean, nullable=False)
	description = db.Column(db.String(300), nullable = False)
	rentmoney = db.Column(db.Integer, nullable = False)
	def __init__(self, rid, rn, cap, ilr, ds, rm):
		self.roomID = rid
		self.roomName = rn
		self.capacity = cap
		self.available = cap
		self.isLongRent = ilr
		self.description = ds
		self.rentmoney = rm

class Server(db.Model):            
	__tablename__ = 'Server'
	serverID = db.Column(db.Integer, primary_key=True)
	password = db.Column(db.String(40), nullable=False)
	def __init__(self, id, psw):
		self.serverID = id
		self.password = psw

class Repairorder(db.Model):            
	__tablename__ = 'Repairorder'
	tenantID = db.Column(db.Integer, db.ForeignKey('Tenant.tenantID'), primary_key = True, nullable=False)
	roomID = db.Column(db.Integer, db.ForeignKey("Room.roomID"), primary_key = True, nullable = False)
	repairmanID = db.Column(db.Integer, db.ForeignKey('Repairman.repairmanID'), primary_key = True, nullable=False)
	content = db.Column(db.String(300), nullable=False)
	ishandled = db.Column(db.Boolean, default=0, nullable=False)
	def __init__(self, tid, roomid, rid, con):
		self.tenantID = tid
		self.roomID = roomid
		self.content = con
		self.repairmanID = rid
		self.ishandled = 0

class Repairman(db.Model):            
	__tablename__ = 'Repairman'
	repairmanID = db.Column(db.Integer, primary_key=True)
	password = db.Column(db.String(40), nullable=False)
	evaluatenum = db.Column(db.Integer, default=0)
	score = db.Column(db.Float, default=10.0)
	def __init__(self, rid, psw):
		self.repairmanID = rid
		self.password = psw
		self.evaluatenum = 0
		self.score = 10.0

class Apply(db.Model):            
	__tablename__ = 'Apply'
	tenantID = db.Column(db.Integer, db.ForeignKey('Tenant.tenantID'), primary_key = True, nullable=False)
	roomID = db.Column(db.Integer, db.ForeignKey('Room.roomID'), primary_key = True, nullable=False)
	content = db.Column(db.String(300), nullable = False)
	startdate = db.Column(db.Date, nullable=False)
	enddate = db.Column(db.Date, nullable=False)
	serverID = db.Column(db.Integer, db.ForeignKey('Server.serverID'), primary_key = True, nullable=False)
	isagreed = db.Column(db.Integer, default=0)
	ispayed = db.Column(db.Boolean, default=0)
	isLongRent = db.Column(db.Boolean)
	def __init__(self, tid, rid, con, sda, eda, sid):
		self.tenantID = tid
		self.roomID = rid
		self.content = con
		self.startdate = sda
		self.enddate = eda
		self.serverID = sid
		self.ispayed = 0
		self.isagreed = 0
  
class UnapprovedApply(db.Model):
	__tablename__ = 'UnapprovedApply'
	uApplyID = db.Column(db.Integer, primary_key = True, nullable = False)
	reply = db.Column(db.String(300))
	tenantID = db.Column(db.Integer, db.ForeignKey('Tenant.tenantID'), nullable=False)
	roomID = db.Column(db.Integer, db.ForeignKey('Room.roomID'), nullable=False)
	content = db.Column(db.String(300), nullable = False)
	startdate = db.Column(db.Date, nullable=False)
	enddate = db.Column(db.Date, nullable=False)
	serverID = db.Column(db.Integer, db.ForeignKey('Server.serverID'), primary_key = True, nullable=False)
	isagreed = db.Column(db.Integer, default=0)
	ispayed = db.Column(db.Boolean, default=0)
	isLongRent = db.Column(db.Boolean)
	def __init__(self, rep, tid, rid, con, sda, eda, sid):
		uaid = 100000 + UnapprovedApply.query.count()
		while UnapprovedApply.query.filter(UnapprovedApply.uApplyID == uaid).first() != None:
			uaid = uaid + 1
		self.uApplyID = uaid
		self.reply = rep
		self.tenantID = tid
		self.roomID = rid
		self.content = con
		self.startdate = sda
		self.enddate = eda
		self.serverID = sid
		self.ispayed = 0
		self.isagreed = 0

class Message(db.Model):
	__tablename__ = 'Message'
	messageID = db.Column(db.Integer, primary_key = True, nullable = False)
	type = db.Column(db.Integer, nullable = False)
	#	1 申请通过	2 申请不通过	3 报修分配师傅	4 投诉处理
	tenantID = db.Column(db.Integer, nullable = False)
	content = db.Column(db.String(300), nullable = False)
	def __init__(self, type, tid, con):
		mid = 1000000 + Message.query.count()
		while Message.query.filter(Message.messageID == mid).first() != None:
			mid = mid + 1
		self.messageID = mid
		self.type = type
		self.tenantID = tid
		self.content = con

#=================以下是古雨写的函数=======================  
  
def login(ID, password):        
	#RET    0 错误    1 租客    2 师傅    3 客服
	result = Tenant.query.filter(Tenant.tenantID == ID).first()
	if result != None:
		if result.password == password:
			return 1
		else:
			return 0
	result = Repairman.query.filter(Repairman.repairmanID == ID).first()
	if result != None:
		if result.password == password:
			return 2
		else:
			return 0
	result = Server.query.filter(Server.serverID == ID).first()
	if result != None:
		if result.password == password:
			return 3
		else:
			return 0

def register(tenantName, phoneNumber, password, isMale, age, job, city):        
	#RET    tenantID
	tenantID = 10000 + Tenant.query.count()
	while Tenant.query.filter(Tenant.tenantID == tenantID).first() != None:
		tenantID = tenantID + 1
	tenant = Tenant(tenantID, tenantName, phoneNumber, password, isMale, age, job, city)
	db.session.add(tenant)
	db.session.commit()
	return tenantID

def getTenant(tenantID):      
	#RET    Tenant结构，通过“.”获得各个属性
	ret = Tenant.query.filter(Tenant.tenantID == tenantID).first()
	return ret
  
def changeTenant(tenantID, tenantName, phoneNumber, password, isMale, age, job, city):  
	#RET    True    False 查无此人
	ten = Tenant.query.filter(Tenant.tenantID == tenantID).first()
	if ten == None:
		return False
	# ten = Tenant(tenantID, tenantName, phoneNumber, password, isMale, age, job, city)
	ten.tenantName = tenantName
	ten.phoneNumber = phoneNumber
	ten.password = password
	ten.isMale = isMale
	ten.age = age
	ten.job = job
	ten.city = city
	db.session.commit()
	return True
  
def searchRoom(keyword, type):  
	#PAR    搜索关键词  short|long
	#RET    所有符合要求的房间
	if type == "short":
		cond = False
	elif type == "long":
		cond = True
	ret = Room.query.filter(and_(Room.roomName.contains(keyword), Room.isLongRent == cond, Room.available > 0)).all()
	return ret

def searchRoomByID(rid):
	result = Room.query.filter(Room.roomID == rid).first()
	return result
  
def submitApply(tenantID, roomID, content, startdate, enddate):  
	#PAR    租户id  房间id  开始日期    结束日期
	#RET    1 成功  0 申请已存在    -1 房间容量已满
	if Apply.query.filter(and_(Apply.tenantID == tenantID, Apply.roomID == roomID)).first() != None:
		return 0
	roo = Room.query.filter(Room.roomID == roomID).first()
	if roo.available <= 0:
		return -1
	roo.available = roo.available - 1
	app = Apply(tenantID, roomID, content, startdate, enddate, 10)
	app.isLongRent = roo.isLongRent
	db.session.add(app)
	db.session.commit()
	return 1
  
def getApplyByTID(tenantID):  
	#PAR    租户id
	#RET    该租户的所有订单
	ret = Apply.query.filter(Apply.tenantID == tenantID).all()
	return ret
  
# def changeApply(TID, RID, startdate, enddate, isagreed, ispayed):  
#     #PAR    租客id  房屋id  起始日期    结束日期    是否审核    是否支付  
#     #RET    True    False 订单不存在  
#     app = Apply.query.filter(Apply.tenantID == TID and Apply.roomID == RID).first()  
#     if app == None:  
#         return False  
#     app = Apply(TID, RID, startdate, enddate, 10)  
#     app.isagreed = isagreed  
#     app.ispayed = ispayed  
#     db.session.commit()  
#     return True  
  
def submitComplain(TID, RID, content):  
	#PAR    租客id  房间id  投诉内容
	#RET    True    False 投诉已存在
	if Complain.query.filter(and_(Complain.tenantID == TID, Complain.roomID == RID)).first() != None:
		return False
	com = Complain(TID, RID, 10, content)
	db.session.add(com)
	db.session.commit()
	return True
  
def submitRepair(TID, RID, content):  
	#PAR    租客id  房间id  报修内容
	#RET    True    False 报修已存在
	if Repair.query.filter(and_(Repair.tenantID == TID, Repair.roomID == RID)).first() != None:
		return False
	rep = Repair(TID, RID, content, 10)
	db.session.add(rep)
	db.session.commit()
	return True
  
def commentRepairman(repairmanID, score):  
	#PAR    师傅id  分数（0-10的整数）
	#RET    True    False 师傅不存在
	rpm = Repairman.query.filter(Repairman.repairmanID == repairmanID).first()
	if rpm == None:
		return False
	sumScore = rpm.evaluatenum * rpm.score + score
	rpm.evaluatenum = rpm.evaluatenum + 1
	rpm.score = sumScore / rpm.evaluatenum
	db.session.commit()
	return True
  
def dealRepairorder(TID, RID):  
	#PAR    租户id  房间id（注意这个不是师傅id！！！！！）
	#RET    True    False 表Repair或Repairman中不存在条目
	#理论上调用这个函数的时候，表Repair和Repairman要么同时出现该条目，要么同时不出现，如果不统一的话就是有bug
	rep = Repair.query.filter(and_(Repair.tenantID == TID, Repair.roomID == RID)).first()
	rpo = Repairorder.query.filter(and_(Repairorder.tenantID == TID, Repairorder.roomID == RID)).first()
	if rep == None or rpo == None:
		return False
	rep.ishandled = True
	rpo.ishandled = True
	db.session.commit()
	return True
  
def getUntreatedRepair():  
	#RET    未安排师傅的报修表，返回的是列表而不是对象
	repLis = Repair.query.all()
	ret = []
	for rep in repLis:
		if Repairorder.query.filter(and_(Repairorder.tenantID == rep.tenantID, Repairorder.roomID == rep.roomID)).first() == None:
			ret.append(rep)
	return ret
  
def getUntreatedComplain():  
	#RET    未处理的投诉，返回的是对象而不是列表
	ret = Complain.query.filter(Complain.ishandled == False).all()
	return ret
  
def getUntreatedApply():  
	#RET    未审核的申请，返回的是对象而不是列表
	ret = Apply.query.filter(Apply.isagreed == False).order_by(Apply.startdate.asc()).all()
	return ret

def getUnhandledRepairorder(repairmanID):
	#PAR	师傅id
	#RET	所有待处理的工单
	ret = Repairorder.query.filter(and_(Repairorder.repairmanID == repairmanID, Repairorder.ishandled == False)).all()
	return ret

def getMessageByTID(tid):
	#PAR	租户id
	#RET	该租户的所有消息
	ret = Message.query.filter(Message.tenantID == tid).all()
	return ret

def getRepairmanIDInRepairorder(TID, RID):
	#PAR	租户id	房间id
	#RET	师傅id	如果该项不存在会返回None
	rpo = Repairorder.query.filter(and_(Repairorder.tenantID == TID, Repairorder.roomID == RID)).first()
	if rpo == None:
		return None
	return rpo.repairmanID

def getApply(TID, RID):  
	#PAR    租户id	房间id
	#RET    一个订单
	ret = Apply.query.filter(and_(Apply.tenantID == TID, Apply.roomID == RID)).first()
	return ret

def getLongRentApply():
	#RET	所有长租订单
	ret = Apply.query.filter(and_(Apply.isagreed == 1, Apply.isLongRent == True)).all()
	return ret

#========================以下是史书华写的函数=========================  
# Tenant  
  
def addTenant(tenantName, phoneNumber, password, isMale, age, job, city):  
	# RET   tenantID
	tenantID = 10000 + Tenant.query.count()
	while Tenant.query.filter(Tenant.tenantID == tenantID).first() != None:
		tenantID = tenantID + 1
	tenant = Tenant(tenantID, tenantName, phoneNumber, password, isMale, age, job, city)
	db.session.add(tenant)
	db.session.commit()
	return tenantID
  
def deleteTenant(tenantID):  
	# RET   True success
	result = Tenant.query.filter(Tenant.tenantID == tenantID).all()
	for ite in result:
		db.session.delete(ite)
	db.session.commit()
	return True
  
# Server  
  
def addServer(password):  
	# RET   serverID
	sid = 10 + Server.query.count()
	while Server.query.filter(Server.serverID == sid).first() != None:
		sid = sid + 1
	sman = Server(sid, password)
	db.session.add(sman)
	db.session.commit()
	return sid
  
def deleteServer(sid):  
	# RET   True: success
	result = Server.query.filter(Server.serverID == sid).all()
	for ite in result:
		db.session.delete(ite)
	db.session.commit()
	return True
  
def changeServer(sid, password):  
	# RET   True: success
	result = Server.query.filter(Server.serverID == sid).all()
	for ite in result:
		ite.password = password
	db.session.commit()
	return True
  
# Repairman  
  
def addRepairman(password):  
	# RET   repairmanID
	rid = 100 + Repairman.query.count()
	while Repairman.query.filter(Repairman.repairmanID == rid).first() != None:
		rid = rid + 1
	rman = Repairman(rid, password)
	db.session.add(rman)
	db.session.commit()
	return rid
  
def deleteRepairman(rid):  
	# RET   True: success
	result = Repairman.query.filter(Repairman.repairmanID == rid).all()
	for ite in result:
		db.session.delete(ite)
	db.session.commit()
	return True
  
def changeRepairman(rid, password, evaluatenum, score):  
	# RET   True: success
	result = Repairman.query.filter(Repairman.repairmanID == rid).all()
	for ite in result:
		ite.password = password
		ite.evaluatenum = evaluatenum
		ite.score = score
	db.session.commit()
	return True
  
# Room  
  
def addRoom(roomName, capacity, isLongRent, description, rentmoney):  
	# RET   roomID
	rid = 1000 + Room.query.count()
	room = Room(rid, roomName, capacity, isLongRent, description, rentmoney)
	db.session.add(room)
	db.session.commit()
	return rid
  
def deleteRoom(rid):  
	# RET   True: success
	result = Room.query.filter(Room.roomID == rid).all()
	for ite in result:
		db.session.delete(ite)
	db.session.commit()
	return True
  
def changeRoom(rid, roomName, available, capacity, isLongRent, description, rentmoney):  
	# RET   True: success
	result = Room.query.filter(Room.roomID == rid).all()
	for ite in result:
		ite.roomName = roomName
		ite.available = available
		ite.capacity = capacity
		ite.isLongRent = isLongRent
		ite.description = description
		ite.rentmoney = rentmoney
	db.session.commit()
	return True
  
# Apply  
  
def addApply(tenantID, roomID, content, startdate, enddate, serverID):  
	# RET   True: success
	apply = Apply(tenantID, roomID, content, startdate, enddate, serverID)
	db.session.add(apply)
	db.session.commit()
	return True
  
def deleteApply(tenantID, roomID, serverID):  
	# RET   True: success
	result = Apply.query.filter(and_(Apply.serverID == serverID, Apply.roomID == roomID, Apply.tenantID == tenantID)).all()
	for ite in result:
		db.session.delete(ite)
	db.session.commit()
	return True
  
def changeApply(tenantID, roomID, content, startdate, enddate, serverID, isagreed, ispayed, isLongRent):  
	# RET   True: success
	result = Apply.query.filter(and_(Apply.serverID == serverID, Apply.roomID == roomID, Apply.tenantID == tenantID)).all()
	for ite in result:
		ite.startdate = startdate
		ite.enddate = enddate
		ite.content = content
		ite.isagreed = isagreed
		ite.ispayed = ispayed
		ite.isLongRent = isLongRent
	db.session.commit()
	return True

def dealApply(tenantID, roomID, serverID, reply, dealmode):
	# dealmode: 1 is agreed, others is disagreed.
	result = Apply.query.filter(and_(Apply.serverID == serverID, Apply.roomID == roomID, Apply.tenantID == tenantID)).first()
	roo = Room.query.filter(Room.roomID == roomID).first()
	if dealmode == 1:
		result.isagreed = 1
		msgCon = "您对房源“" + roo.roomName + "”的申请已通过。"
		msg = Message(1, tenantID, msgCon)
		db.session.add(msg)
		db.session.commit()
		return True
	else:
		ure = UnapprovedApply(reply, result.tenantID, result.roomID, result.content, result.startdate, result.enddate, result.serverID)
		msgCon = "您对房源“" + roo.roomName + "”的申请未通过。"
		msg = Message(2, tenantID, msgCon)
		db.session.add(msg)
		db.session.delete(result)
		db.session.add(ure)
		db.session.commit()
		return True

# Repair  
  
def addRepair(tenantID, roomID, content, serverID):  
	# RET   True: success
	repair = Repair(tenantID, roomID, content, serverID)
	db.session.add(repair)
	db.session.commit()
	return True
  
def deleteRepair(tenantID, roomID, serverID):  
	# RET   True: success
	result = Repair.query.filter(and_(Repair.tenantID == tenantID, Repair.serverID == serverID, Repair.roomID == roomID)).all()
	for ite in result:
		db.session.delete(ite)
	db.session.commit()
	return True
  
def changeRepair(tenantID, roomID, content, serverID, ishandled):  
	# RET   True: success
	result = Repair.query.filter(and_(Repair.tenantID == tenantID, Repair.serverID == serverID, Repair.roomID == roomID)).all()
	for ite in result:
		ite.ishandled = ishandled
		ite.content = content
	db.session.commit()
	return True
  
# Complain  
  
def addComplain(tenantID, roomID, serverID, content):  
	# RET   True: success
	comp = Complain(tenantID, roomID, serverID, content)
	db.session.add(comp)
	db.session.commit()
	return True
  
def deleteComplain(tenantID, roomID, serverID):  
	# RET   True: success
	result = Complain.query.filter(and_(Complain.tenantID == tenantID, Complain.serverID == serverID, Complain.roomID == roomID)).all()
	for ite in result:
		db.session.delete(ite)
	db.session.commit()
	return True
  
def changeComplain(tenantID, roomID, serverID, content, reply, ishandled):  
	# RET   True: success
	result = Complain.query.filter(and_(Complain.tenantID == tenantID, Complain.serverID == serverID, Complain.roomID == roomID)).all()
	for ite in result:
		ite.ishandled = ishandled
		ite.reply = reply
		ite.content = content
	db.session.commit()
	return True
  
# Repairorder  
  
def gnerRepairorder(tenantID, roomID, repairmanID):  
	# RET: True success
	repair = Repair.query.filter(and_(Repair.tenantID == tenantID, Repair.roomID == roomID)).first()
	ro = Repairorder(repair.tenantID, repair.roomID, repairmanID, repair.content)
	# repair.ishandled = True
	roo = Room.query.filter(Room.roomID == roomID).first()
	msgCon = "我们已派出" + str(repairmanID) + "号师傅处理您对房屋“" + roo.roomName + "”的报修。"
	msg = Message(3, tenantID, msgCon)
	db.session.add(msg)
	db.session.add(ro)
	db.session.commit()
	return True
  
# def deleteRepairorder(tenantID, roomID, repairmanID):  
#   # RET   True: success  
#   result = Repairorder.query.filter(  
#       and_(Repairorder.tenantID == tenantID, Repairorder.roomID == roomID, Repairorder.repairmanID == repairmanID)).all()  
#   for ite in result:  
#       db.session.delete(ite)  
#   db.session.commit()  
#   return True  
  
# def changeRepairorder(tenantID, roomID, rmanID, content, ishandled):  
#   # RET   True: success  
#   result = Repairorder.query.filter(  
#       and_(Repairorder.tenantID == tenantID, Repairorder.roomID == roomID,  
#            Repairorder.repairmanID == rmanID)).all()  
#   for ite in result:  
#       ite.content = content  
#       ite.ishandled = ishandled  
#   db.session.commit()  
#   return True  
  
# Auxiliary function  
  
def searchInfo(words, mode):  
	# 说明：return得到的是一个包含查询结果的集合，可以使用 foreach 逐个访问元素，需要什么属性自取即可
	# 模式说明：
	# room， 搜索名字或描述的关键字；
	# tenant，搜索名字的关键字；
	# repairman，搜索ID的关键字（没有名字QAQ）；
	# apply，搜索租客名字的关键字；
  
	if mode == "room":
		result = Room.query.filter(or_(Room.roomName.like("%"+words+"%") if words is not None else "",
									   Room.description.like("%"+words+"%") if words is not None else "")).all()
	elif mode == "tenant":
		result = Tenant.query.filter(Tenant.tenantName.like("%"+words+"%") if words is not None else "").all()
	elif mode == "repairman":
		result = Repairman.query.filter(Repairman.repairmanID.like("%"+words+"%") if words is not None else "").all()
	elif mode == "apply":
		result = Apply.query.filter(Tenant.tenantName.like("%"+words+"%") if words is not None else "").all()
	else:
		result = None
	return result
	# s = len(result)
	# strj = '{"count": ' + str(s)
	# i = 0
	# if mode == "room":
	#   for ite in result:
	#       i = i+1
	#       strj += ', "item"' + str(i) + ': "' + str(ite.roomName) + '"'
	# elif mode == "tenant":
	#   for ite in result:
	#       i = i+1
	#       strj += ', "item"' + str(i) + ': "' + str(ite.tenantName) + '"'
	# elif mode == "repairman":
	#   for ite in result:
	#       i = i+1
	#       strj += ', "item"' + str(i) + ': "' + str(ite.repairmanID) + '"'
	# else:
	#   for ite in result:
	#       i = i + 1
	#       strj += ', "item"' + str(i) + ': "' + str(ite.startdate) + '"'
	# return json.load(strj)
  
def submitReplyToComplain(tenantID, roomID, serverID, reply):  
	# RET   True: success
	result = Complain.query.filter(and_(Complain.tenantID == tenantID, Complain.serverID == serverID, Complain.roomID == roomID)).all()
	roo = Room.query.filter(Room.roomID == roomID).first()
	for ite in result:
		ite.reply = reply
		ite.ishandled = True
	msgCon = "您对房屋“" + roo.roomName + "”的投诉已收到回复：" + reply
	msg = Message(4,tenantID, msgCon)
	db.session.add(msg)
	db.session.commit()
	return True
  
#=========================函数到这里结束================================  

# db.drop_all()
# db.create_all()  
# addServer("password")
# addTenant('gy','12312312345','password',1,18,'coder','sz')
# addRoom('room1',4,1,'description',100)
# submitApply(10000, 1000, "content", '2020/06/13', '2020/07/13')
# dealApply(10000,1000,10,'reply',1)
# submitRepair(10000,1000,'content')
# addRepairman('password')
# gnerRepairorder(10000,1000,100)

db.drop_all()
db.create_all()
test = register('rosheen','15810586673','12345',True,18,'student','beijing')
test_room1 = addRoom('杭州市下城区 中海望庐小区 4人间','4',True,'房间敞亮,靠近西溪银泰城,步行至地铁龙翔桥站10分钟','2000')
test_room2 = addRoom('杭州市西湖区 南都花园三区 2人间','2',True,'位于西湖区文一西路122号，文一西路与竟州路交汇，临近古荡，古墩路，双地铁口边，文新站2号线边。周围的商业街有：城西印象城，银泰百货','2460')
test_room3 = addRoom('杭州市下城区 润和亿城嘉园 4人间','4',True,'亿城嘉园小区单间，简单装修，小区门口生活购物吃饭都有，公交总站非常方便，实图实价、民用水电','1000')
test_room4 = addRoom('深圳市龙岗区 卓然居 1人间','1',True,'房间周边无遮挡采光通风好，57平户型端正，双阳台，天然气入户，带家私家电','2100')
test_room5 = addRoom('深圳市龙岗区 锦城星苑 1人间','1',True,'小区300米处有仙人岭农贸市场，楼下有生鲜超市，小区东边有华润万家购物超市，距离小区2公里有三甲医院，三站公交到双龙天虹商场、地铁站','1600')
test_room11 = addRoom('北京市海淀区 北京航空航天大学男生宿舍 4人间','4',False,'有独立卫浴,靠近食堂,步行至知春路或西土城地铁站15分钟','100')
test_room4 = addRoom('北京市朝阳区 东恒时代二期','2',False,'该房源位于八里庄东里小区，周边商超购物方便','120')
test_server = addServer('1234567')
test_server = addRepairman('1234567')
test_apply1 = submitApply(10000,1000,'好','2020-7-10','2020-8-10')
test_apply2 = submitApply(10000,1001,'好','2020-7-10','2021-8-10')
apply_pass1 = dealApply(10000,1000, 10,' reply', 1)
apply_pass1 = dealApply(10000,1001, 10,' reply', 1)