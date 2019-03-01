import os, sys, time
path = os.path.join(os.path.dirname(__file__), '../lib/')
sys.path.insert(0, path)

from thrift.transport import THttpClient
from thrift.protocol import TCompactProtocol

#from .client import LineClient
from curve.ttypes import *
from curve import LineService
#from types import *

class Poll:

  client = None

  auth_query_path = "/api/v4/TalkService.do";
  http_query_path = "/S4";
  polling_path = "/P4";
  host = "gd2.line.naver.jp";
  port = 443;

  UA = "Line/8.4.2 iPad4,1 9.0.2"
  LA = "DESKTOPWIN\t5.5.5DESKTOPWIN\t18.99"

  rev = 0

  def __init__(self, authToken):
    self.transport = THttpClient.THttpClient('https://gd2.line.naver.jp:443'+ self.http_query_path)
    self.transport.setCustomHeaders({
      "User-Agent" : self.UA,
      "X-Line-Application" : self.LA,
      "X-Line-Access": authToken
    });
    self.protocol = TCompactProtocol.TCompactProtocol(self.transport);
    self.client = LineService.Client(self.protocol)
    self.rev = self.client.getLastOpRevision()
    self.transport.path = self.polling_path
    self.transport.open()
      
  #def __init__(self, client):
      #if type(client) is not LineClient:
          #raise Exception("You need to set LineClient instance to initialize LinePoll")
      #self.client = client      
      
  def __fetchOperation(self, revision, count=1):
      return self.client.poll.fetchOperations(revision, count)      

  def addOpInterruptWithDict(self, OpInterruptDict):
      self.OpInterrupt.update(OpInterruptDict)

  def addOpInterrupt(self, OperationType, DisposeFunc):
      self.OpInterrupt[OperationType] = DisposeFunc
        
  def execute(self, op, threading):
      try:
          if threading:
              _td = threading.Thread(target=self.OpInterrupt[op.type](op))
              _td.daemon = False
              _td.start()
          else:
              self.OpInterrupt[op.type](op)
      except Exception as e:
          self.client.log(e)
    
  def setRevision(self, revision):
      self.client.revision = max(revision, self.client.revision)

  def singleTrace(self, count=1):
      try:
          operations = self.fetchOperation(self.client.revision, count=count)
      except KeyboardInterrupt:
          exit()
      except:
          return
        
      if operations is None:
          return []
      else:
          return operations

  def trace(self, threading=False):
      try:
          operations = self.fetchOperation(self.client.revision)
      except KeyboardInterrupt:
          exit()
      except:
          return
        
      for op in operations:
          if op.type in self.OpInterrupt.keys():
              self.execute(op, threading)
          self.setRevision(op.revision)
          
  def stream(self, sleep=50000):
      usleep = lambda x: time.sleep(x/1000000.0)
      while True:
        try:
          Ops = self.client.fetchOperations(self.rev, 5)
        except EOFError:
          raise Exception("It might be wrong revision\n" + str(self.rev.decode))

        for Op in Ops:
            # print Op.type
          if (Op.type != OpType.END_OF_OPERATION):
            self.rev = max(self.rev, Op.revision)
            return Op

        usleep(sleep)
                
          
          
          
