# -*- coding: utf-8 -*-
import TOKEN
from TOKEN.lib.curve.ttypes import *
from datetime import datetime
import time,random,sys,json,os,codecs,threading,glob,re
from thrift.protocol import TCompactProtocol
from thrift.transport import THttpClient
from ttypes import LoginRequest
import json, requests, LineService

with open('token.json', 'r') as fp:
    aun = json.load(fp)
    
def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)
    
token = TOKEN.LINE()
if aun['token1'] == "":
    token.login(qr=True)
else:
    token.login(token=aun['token1'])
token.loginResult()

sever1 = 'DESKTOPWIN'
Headers = {
        'User-Agent': "Line/8.3.3",
        'X-Line-Application': "DESKTOPWIN\t5.5.5DESKTOPWIN\t18.99",
        "x-lal": "ja-US_US",
    }

sever2 = 'DESKTOPMAC'   
Headers2 = {
        'User-Agent': "Line/8.4.1 iPad4,1 9.0.2",
        'X-Line-Application': "DESKTOPMAC 5.8.0-YOSEMITE-x64    MAC 10.8.5",
        "x-lal": "ja-US_US",
    }

sever3 = 'CHROMEOS'
Headers3 = {
        'User-Agent': "CHROMEOS\t9.0.3Bot-Eater\t17.09",
        'X-Line-Application': "CHROMEOS 1.7.14 BotEater x64",
        "x-lal": "ja-US_US",
    }

sever4 = 'IOSIPAD'
Headers4 = {
        'User-Agent': "Line/8.0.0",
        'X-Line-Application': "IOSIPAD\t7.18.0\tiPhone OS\t11.12.1",
        "x-lal": "ja-US_US",
    }

print ("登入成功")

helpMessage =""" ☆ token登入指令 ☆

 1. DESKTOPWIN
 ↬ loginwin 1 
 ===================
 2. DESKTOPMAC
 ↬ loginmac 1 
 ===================
 3. CHROMEOS
 ↬ loginchromeos 1 
 ===================
 4.IOSIPAD
 ↬ loginiosipad 1 
 ===================
 5. @bye 機器退出群組
 
 [ Token Login v1.0 ]
"""
mid = token.getProfile().mid
Bots=[mid]
creator =["權限者mid"]

wait = {
    'leaveRoom':True,
    'autoAdd':True,
    'autoJoin':True,
    'message':"感謝你加我好友，現在你可以邀請我到群組 ☆",
    "lang":"JP",
    }
    
def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)
    
def bot(op):
    try:
        if op.type == 0:
            return
        if op.type == 5:
            contact = token.getContact(op.param1)
            if wait["autoAdd"] == True:
                token.findAndAddContactsByMid(op.param1)
                print ("[ 5 ] 通知添加好友: " + contact.displayName)
                if (wait["message"] in [""," ","\n",None]):
                    pass
                else:
                    token.sendText(op.param1,str(wait["message"]))
                                     
        if op.type == 13:
            group = token.getGroup(op.param1)
            inviter = token.getContact(op.param2)
            print ("[ 13 ] 通知邀請群組: " + str(group.name) + "\n邀請者: " + inviter.displayName)
            if mid in op.param3:
              if wait["autoJoin"] == True:
                token.acceptGroupInvitation(op.param1)
                token.sendText(op.param1,"請輸入help查看指令")
            
        if op.type == 21 or op.type == 22 or op.type ==24:
            if wait["leaveRoom"] == True:
                token.leaveRoom(op.param1)
                print ("[ 24 ] 通知離開副本")

        if (op.type == 25 or op.type == 26) and op.message.contentType == 0:
            msg = op.message
            if msg.text in ["help","Help","key","@help","menu","指令"]:
              if wait["lang"] == "JP":
                  token.sendText(msg.to,helpMessage)
############# REBOOT ##########################
            elif msg.text.lower().startswith("restart"):
             if msg.from_ in creator:
              print ("[ Info ] Bot Restart")
              try:
                 token.sendText(msg.to,"Restart done ")
                 restart_program()
              except:
                 token.sendText(msg.to,"Please wait")
                 restart_program()
                 pass
############# LOGIN WIN ##########################
            elif msg.text.lower().startswith("loginwin"):
              separate = msg.text.split(" ")
              jmlh = int(separate[1])
              for x in range(jmlh):
                  Headers.update({'x-lpqs' : '/api/v4/TalkService.do'})
                  transport = THttpClient.THttpClient('https://gd2.line.naver.jp/api/v4/TalkService.do')
                  transport.setCustomHeaders(Headers)
                  protocol = TCompactProtocol.TCompactProtocol(transport)
                  client = LineService.Client(protocol)
                  qr = client.getAuthQrcode(keepLoggedIn=1, systemName=sever1)
                  link = "line://au/q/" + qr.verifier
                  print('\n')
                  print(link)
                  token.sendText(msg.to,str(link))
                  Headers.update({"x-lpqs" : '/api/v4/TalkService.do', 'X-Line-Access': qr.verifier})
                  json.loads(requests.session().get('https://gd2.line.naver.jp/Q', headers=Headers).text)
                  Headers.update({'x-lpqs' : '/api/v4p/rs'})
                  transport = THttpClient.THttpClient('https://gd2.line.naver.jp/api/v4p/rs')
                  transport.setCustomHeaders(Headers)
                  protocol = TCompactProtocol.TCompactProtocol(transport)
                  client = LineService.Client(protocol)
                  req = LoginRequest()
                  req.type = 1
                  req.verifier = qr.verifier
                  req.e2eeVersion = 1
                  res = client.loginZ(req)
                  print('\n')
                  print(res.authToken)
              else:
                  token.sendText(msg.to, "Your DESKTOPWIN token")
                  token.sendText(msg.to,str(res.authToken))
                  
############# LOGIN MAC #############
            elif msg.text.lower().startswith("loginmac"):
              separate = msg.text.split(" ")
              jmlh = int(separate[1])
              for x in range(jmlh):
                  Headers2.update({'x-lpqs' : '/api/v4/TalkService.do'})
                  transport = THttpClient.THttpClient('https://gd2.line.naver.jp/api/v4/TalkService.do')
                  transport.setCustomHeaders(Headers2)
                  protocol = TCompactProtocol.TCompactProtocol(transport)
                  client = LineService.Client(protocol)
                  qr = client.getAuthQrcode(keepLoggedIn=1, systemName=sever2)
                  link = "line://au/q/" + qr.verifier
                  print('\n')
                  print(link)
                  token.sendText(msg.to,str(link))
                  Headers2.update({"x-lpqs" : '/api/v4/TalkService.do', 'X-Line-Access': qr.verifier})
                  json.loads(requests.session().get('https://gd2.line.naver.jp/Q', headers=Headers2).text)
                  Headers2.update({'x-lpqs' : '/api/v4p/rs'})
                  transport = THttpClient.THttpClient('https://gd2.line.naver.jp/api/v4p/rs')
                  transport.setCustomHeaders(Headers2)
                  protocol = TCompactProtocol.TCompactProtocol(transport)
                  client = LineService.Client(protocol)
                  req = LoginRequest()
                  req.type = 1
                  req.verifier = qr.verifier
                  req.e2eeVersion = 1
                  res = client.loginZ(req)
                  print('\n')
                  print(res.authToken)
              else:
                  token.sendText(msg.to, "Your DESKTOPMAC token")
                  token.sendText(msg.to,str(res.authToken))

############# LOGIN CHROMEOS #############
            elif msg.text.lower().startswith("loginchromeos"):
              separate = msg.text.split(" ")
              jmlh = int(separate[1])
              for x in range(jmlh):
                  Headers3.update({'x-lpqs' : '/api/v4/TalkService.do'})
                  transport = THttpClient.THttpClient('https://gd2.line.naver.jp/api/v4/TalkService.do')
                  transport.setCustomHeaders(Headers3)
                  protocol = TCompactProtocol.TCompactProtocol(transport)
                  client = LineService.Client(protocol)
                  qr = client.getAuthQrcode(keepLoggedIn=1, systemName=sever3)
                  link = "line://au/q/" + qr.verifier
                  print('\n')
                  print(link)
                  token.sendText(msg.to,str(link))
                  Headers3.update({"x-lpqs" : '/api/v4/TalkService.do', 'X-Line-Access': qr.verifier})
                  json.loads(requests.session().get('https://gd2.line.naver.jp/Q', headers=Headers3).text)
                  Headers3.update({'x-lpqs' : '/api/v4p/rs'})
                  transport = THttpClient.THttpClient('https://gd2.line.naver.jp/api/v4p/rs')
                  transport.setCustomHeaders(Headers3)
                  protocol = TCompactProtocol.TCompactProtocol(transport)
                  client = LineService.Client(protocol)
                  req = LoginRequest()
                  req.type = 1
                  req.verifier = qr.verifier
                  req.e2eeVersion = 1
                  res = client.loginZ(req)
                  print('\n')
                  print(res.authToken)
              else:
                  token.sendText(msg.to, "Your CHROMEOS token")
                  token.sendText(msg.to,str(res.authToken))

############# LOGIN IOSIPAD #############
            elif msg.text.lower().startswith("loginiosipad"):
              separate = msg.text.split(" ")
              jmlh = int(separate[1])
              for x in range(jmlh):
                  Headers4.update({'x-lpqs' : '/api/v4/TalkService.do'})
                  transport = THttpClient.THttpClient('https://gd2.line.naver.jp/api/v4/TalkService.do')
                  transport.setCustomHeaders(Headers4)
                  protocol = TCompactProtocol.TCompactProtocol(transport)
                  client = LineService.Client(protocol)
                  qr = client.getAuthQrcode(keepLoggedIn=1, systemName=sever4)
                  link = "line://au/q/" + qr.verifier
                  print('\n')
                  print(link)
                  token.sendText(msg.to,str(link))
                  Headers4.update({"x-lpqs" : '/api/v4/TalkService.do', 'X-Line-Access': qr.verifier})
                  json.loads(requests.session().get('https://gd2.line.naver.jp/Q', headers=Headers4).text)
                  Headers4.update({'x-lpqs' : '/api/v4p/rs'})
                  transport = THttpClient.THttpClient('https://gd2.line.naver.jp/api/v4p/rs')
                  transport.setCustomHeaders(Headers4)
                  protocol = TCompactProtocol.TCompactProtocol(transport)
                  client = LineService.Client(protocol)
                  req = LoginRequest()
                  req.type = 1
                  req.verifier = qr.verifier
                  req.e2eeVersion = 1
                  res = client.loginZ(req)
                  print('\n')
                  print(res.authToken)
              else:
                  token.sendText(msg.to, "Your IOSIPAD token")
                  token.sendText(msg.to,str(res.authToken))

############## BYE BOT ###################
            elif msg.text.lower().startswith("@bye"):
              if msg.toType == 2:
                  ginfo = token.getGroup(msg.to)
                  try:
                      token.sendText(msg.to,"Bye Bye")
                      token.leaveGroup(msg.to)
                  except:
                    pass
            elif msg.text.lower().startswith("leave allgroups"):
             if msg.from_ in creator:
               token.leaveGroup(token.getGroupIdsJoined())
        if op.type == 59:
            print (op)

    except Exception as error:
        print (error)
        
while True:
  try:
    try:
        Ops = token.fetchOperation(token.Poll.rev, 10)
    except EOFError:
        raise Exception("It might be wrong revision\n" + str(token.Poll.rev))
        
    for Op in Ops:
        if (Op.type != OpType.END_OF_OPERATION):
            token.Poll.rev = max(token.Poll.rev, Op.revision)
            bot(Op)      
         
  except Exception as E:
    E = str(E)
    if "reason=None" in E:
      print (E)
      time.sleep(60)
      restart_program()  
