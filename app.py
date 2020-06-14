# -*- coding:utf-8 -*-
from functools import wraps
from flask import Flask, request, render_template, redirect, url_for, flash, session, jsonify

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_

import uuid          
from flask import Flask, request, json, Response          
from flask_sqlalchemy import SQLAlchemy

#app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.secret_key = '\xc9ixnRb\xe40\xd4\xa5\x7f\x03\xd0y6\x01\x1f\x96\xeao+\x8a\x9f\xe4'
import config
from main import *
from Faduanxin import *       
          
app = Flask(__name__)          
app.config.from_object(config)  
db = SQLAlchemy(app)



# ############################################
# # 路由
# ############################################




app.debug=True
# #################################################
# 以下为公共页面
# #################################################
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html',phone='',ret='')

# ################################################
# 以下为用户登录后可访问的页面
# ################################################
@app.route('/userhome/<userID>')
def userhome(userID):
    return render_template('UserHome.html',userID=userID)

@app.route('/changeinfo/<userID>')
def changeinfo(userID):
    return render_template('changeInfo.html',userID=userID,ret=getTenant(userID))

@app.route('/orderquery/<userID>')
def orderquery(userID):
    ret = getApplyByTID(userID)
    return render_template('OrderQuery.html',userID=userID,ret=ret)

@app.route('/applyform/<userID>/<roomID>')
def applyform(userID,roomID):
    return render_template('applyform.html',userID=userID,roomID=roomID)

@app.route('/housequery/<userID>')
def housequery(userID):
    return render_template('HouseQuery.html',userID=userID)

@app.route('/fix/<userID>/<roomID>')
def fix(userID,roomID):
    return render_template('fix.html',userID=userID,roomID=roomID)

@app.route('/complanation/<userID>/<roomID>')
def complanation(userID,roomID):
    return render_template('complanation.html',userID=userID,roomID=roomID)

@app.route('/valuefix/<userID>/<roomID>')
def valuefix(userID,roomID):
    return render_template('valuefix.html',userID=userID,roomID=roomID)

@app.route('/prolong/<userID>/<roomID>')
def prolong(userID,roomID):
    return render_template('prolong.html',userID=userID,roomID=roomID)

@app.route('/msgbox/<userID>')
def msgbox(userID):
    ret = getMessageByTID(userID)
    return render_template('msgbox.html',userID=userID,ret=ret)

@app.route('/contract/<userID>')
def contract(userID):
    return render_template('Contract.html',userID=userID)

@app.route('/pay/<userID>')
def pay(userID):
    return render_template('pay.html',userID=userID)

# ################################################
# 以下为管理员登录后可查看的页面
# ################################################
@app.route('/adminhome')
def f_adminhome():
    return render_template('admin_home.html',repair=getUntreatedRepair(),apply=getUntreatedApply(),complain=getUntreatedComplain())

@app.route('/arrange')
def f_repairs():
    return render_template('arrangeRepair.html',repair=getUntreatedRepair(),repairman=searchInfo("","repairman"))

@app.route('/audit')
def f_audit():
    return render_template('auditApply.html',apply=getUntreatedApply())

@app.route('/reply')
def f_reply():
    return render_template('replyComplain.html',complain=getUntreatedComplain())

@app.route('/manageroom')
def f_manageroom():
    return render_template('manage_room.html',room=searchInfo("","room"),serverID=10)

@app.route('/managecontract')
def f_managecontract():
    return render_template('manage_contract.html',contract=getLongRentApply())

# ################################################
# 以下为师傅登录后可查看的页面
# ################################################

@app.route('/workerhome/<repairmanID>')
def f_worker(repairmanID):
    return render_template('WorkerHome.html',order=getUnhandledRepairorder(repairmanID))


# ################################################
# 以下为公共实现的功能
# ################################################

# 1.注册
@app.route('/register', methods=['GET', 'POST'])
def f_register():
    if request.method=='POST':
        a = register(request.form['username'],request.form['okphone'],request.form['password1'],request.form['sex'],request.form['age'],request.form['job'],request.form['city'])
        return render_template('signup.html',userID=a)
    return render_template('signup.html')


# 2.登录
@app.route('/login', methods=['GET', 'POST'])
def f_login():
    if request.method =='POST':
        userid=request.form['userID']
        result = login(request.form['userID'],request.form['password'])
        if result != 0:
            if result == 1:
                return redirect(url_for('userhome',userID=userid))
            elif result == 3:
                return redirect(url_for('f_adminhome'))
            elif result == 2:
                return redirect(url_for('f_worker',repairmanID=userid))
    return render_template('index.html', error="账号或密码错误！")


# ################################################
# 以下为租客登陆后实现的功能
# ################################################

# 3.修改个人信息
@app.route('/change/<userID>', methods=['GET', 'POST'])
def f_changeinfo(userID):
    if request.method == 'POST':
        result = changeTenant(userID,request.form['username'],request.form['phone'],request.form['password1'],request.form['sex'],request.form['age'],request.form['job'],request.form['city'])
        if result == True:
            return render_template('changeInfo.html',result=result,userID=userID,ret=getTenant(userID))
    return render_template('NotFound.html')


# 4.搜索房源
@app.route('/search/<userID>', methods=['GET', 'POST'])
def f_search(userID):
    if request.method == 'POST':
        ret = searchRoom(request.form['keyword'],request.form['rentTime'])
        return render_template('HouseQuery.html',userID=userID,ret=ret)
    return render_template('NotFound.html')


# 5.提交申请
@app.route('/apply/<userID>/<roomID>', methods=['GET','POST'])
def f_apply(userID,roomID):
    if request.method == 'POST':
        ret=submitApply(int(userID),int(roomID),request.form['reason'],request.form['startdate'],request.form['enddate'])
        if ret == 0:
            return render_template('applyform.html',userID=userID,roomID=roomID,error="已提交过")
        else:
            return render_template('applyform.html',userID=userID,roomID=roomID,info="ok")
    return render_template('NotFound.html')

# 6.报修
@app.route('/f_fix/<userID>/<roomID>', methods=['GET','POST'])
def f_fix(userID,roomID):
    if request.method == 'POST':
        ret = submitRepair(userID, roomID, request.form['reason'])
        if ret == True:
            return render_template('fix.html',userID=userID,roomID=roomID,msg='ok')
        elif ret == False:
            return render_template('fix.html',userID=userID,roomID=roomID,error='nook')
    return render_template('NotFound.html')

# 7.投诉
@app.route('/f_complanation/<userID>/<roomID>', methods=['GET','POST'])
def f_complanation(userID,roomID):
    if request.method == 'POST':
        ret = submitComplain(userID, roomID, request.form['reason'])
        if ret == True:
            return render_template('complanation.html',userID=userID,roomID=roomID,msg='ok')
        elif ret == False:
            return render_template('complanation.html',userID=userID,roomID=roomID,error='nook')
    return render_template('NotFound.html')

# 8.评价师傅
@app.route('/f_valuefix/<userID>/<roomID>', methods=['GET','POST'])
def f_valuefix(userID,roomID):
    if request.method == "POST":
        rpid=getRepairmanIDInRepairorder(userID,roomID)
        ret = commentRepairman(rpid,float(request.form['score']))
        return render_template('valuefix.html',userID=userID,roomID=roomID,msg="ok")
    return render_template('NotFound.html')

# 9.申请续约
@app.route('/f_prolong/<userID>/<roomID>', methods=['GET','POST'])
def f_prolong(userID,roomID):
    if request.method =='POST':
        apply_pre = getApply(userID,roomID)
        if request.form['enddate']<str(apply_pre.enddate):
            return render_template('prolong.html',userID=userID,roomID=roomID,error="error")
        else:
            result = changeApply(userID, roomID, request.form['reason'], apply_pre.startdate, request.form['enddate'], 10, False, apply_pre.ispayed , apply_pre.isLongRent)
            return render_template('prolong.html',userID=userID,roomID=roomID,msg="ok")
    return render_template('NotFound.html')

# 10.发送验证码
@app.route('/submitphone', methods=['GET','POST'])
def submitphone():
    if request.method == 'POST':
        ret = Yanzhengma(request.form['phone'])
        return render_template('signup.html',phone=request.form['phone'],ret=ret)


# ################################################
# 以下为管理员登录后可实现的功能
# ################################################

# 1.安排师傅处理报修
@app.route('/arrange/<tenantID>/<roomID>',methods=['GET','POST'])
def f_gnerrepair(tenantID,roomID):
    if request.method == 'POST':
        ret = gnerRepairorder(tenantID,roomID,request.form['repairmanID'])
        if ret:
            return redirect(url_for('f_repairs'))
        else:
            return redirect(url_for('f_repairs'))   #so ret is redundant?

# 2.审核申请
@app.route('/audit/<tenantID>/<roomID>/<serverID>',methods=['GET','POST'])
def f_auditapply(tenantID,roomID,serverID):
    if request.method == 'POST':
        dealApply(tenantID,roomID,serverID,request.form.get('reply'),request.form.get('dealmode'))
    return redirect(url_for('f_audit'))

# 3.处理投诉
@app.route('/reply/<tenantID>/<roomID>/<serverID>',methods=['GET','POST'])
def f_replycomplain(tenantID,roomID,serverID):
    if request.method == 'POST':
        submitReplyToComplain(tenantID,roomID,10,request.form.get('reply'))
    return redirect(url_for('f_reply'))

# 4.管理租客
@app.route('/managetenant', methods=['GET','POST'])
def f_managetenant():
    if request.method == 'POST':
        addTenant(request.form['tenantName'],request.form['phoneNumber'],request.form['password'],request.form['sex'],request.form['age'],request.form['job'],request.form['city'])
    return render_template('manage_tenant.html',tenant=searchInfo("","tenant"))  

# 5.管理房源
@app.route('/manageroom/<serverID>/<roomID>',methods=['GET','POST'])
def f_faceroom(serverID,roomID):
    if request.method == 'POST':
        addApply(request.form['tenantID'],roomID,request.form['content'],request.form['startdate'],request.form['enddate'],serverID)
        dealApply(request.form['tenantID'],request.form['roomID'],serverID,"",1)
    return redirect(url_for(f_manageroom))

# 6.管理师傅
@app.route('/manageworker',methods=['GET','POST'])
def f_manageworker():
    if request.method == 'POST':
        addRepairman(request.form.get['password'])
    return render_template('manage_worker.html',worker=searchInfo("","repairman"))

# 7.管理合同（长租订单）
@app.route('/managecontract/<tenantID>/<roomID>/<serverID>',methods=['GET','POST'])
def f_deletecontract(tenantID,roomID,serverID):
    if request.method == 'POST':
        deleteApply(tenantID,roomID,serverID)
    redirect(url_for('/f_managecontract'))



# ################################################
# 以下为师傅登录后可以实现的功能
# ################################################

# 1.处理工单
@app.route('/workerhome/<repairmanID>/<tenantID>/<roomID>',methods=['GET','POST'])
def f_dealorder(repairmanID,tenantID,roomID):
    if request.method == 'POST':
        dealRepairorder(tenantID,roomID)
    return redirect(url_for('f_worker',repairmanID=repairmanID))




# ################################################
# 以下为需要传递至前端全局的函数
# ################################################

def searchRepairByID(tid,rid):
    result = Repair.query.filter(and_(Repair.tenantID == tid, Repair.roomID == rid)).all()
    return result

def searchComplainByID(tid,rid):
    result = Repair.query.filter(and_(Complain.tenantID == tid, Complain.roomID == rid)).all()
    return result

app.add_template_global(searchRoomByID,'searchRoomByID')
app.add_template_global(searchRepairByID,'searchRepairByID')
app.add_template_global(searchComplainByID,'searchComplainByID')

if __name__=='__main__':
    app.run(
      host='0.0.0.0',
      port= 80,
      debug=True
    )