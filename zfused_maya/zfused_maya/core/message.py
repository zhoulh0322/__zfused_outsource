# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function

import os
import pika
import logging

from PySide2 import QtCore

import zfused_maya
import zfused_login.core.util as util
import zfused_api

logger = logging.getLogger(__name__)

class MessageMonitor(QtCore.QThread):
    receive_message = QtCore.Signal(str)
    def __init__(self, parent = None):
        super(MessageMonitor, self).__init__(parent)

        _credentials = pika.PlainCredentials('root', 'bugeinishuo1')
        # get host
        _addr = util.zfused_server_addr()
        _host = _addr.split("http://")[-1].split(":")[0]
        _connection = pika.BlockingConnection(pika.ConnectionParameters(_host, 5672, "/", _credentials))
        self.channel = _connection.channel()  
        self.channel.exchange_declare(exchange = 'direct_logs', 
                                      exchange_type = 'topic')  
        result = self.channel.queue_declare( exclusive = True) 
        queue_name = result.method.queue
        # user id
        _user_id = zfused_api.zFused.USER_ID
        
        severities = ["message.update","message.*","message.system","message.project.*","message.user.%s"%_user_id,"message.group.*","message.step.*"]
        if not severities:  
            logger.warning(sys.stderr, "Usage: %s [info] [warning] [error]" % (sys.argv[0]))
            sys.exit(1)  
        for severity in severities:  
            self.channel.queue_bind(exchange = 'direct_logs',  
                                    queue = queue_name,
                                    routing_key = severity)  
        self.channel.basic_consume(self.callback,  
                                   queue = queue_name,
                                   no_ack = True)
        self.start()

    def callback(self,ch, method, properties, body):
        self.receive_message.emit(unicode(body,'utf-8'))

    def run(self):
        self.channel.start_consuming() 

    def quit(self): 
        self.channel.close()
        super(worker, self).quit()

    def __del__(self):
        logger.info("message monitor quit")
        self.channel.close()

def analyze(message):
    """ analyze message
        分析消息

    :rtype: None
    """
    logger.info("get message {}".format(message))

    _message = eval(message)
    _message_handle = zfused_api.message.Message(_message["message_id"])

    if _message_handle.data["SubmitterObject"] == "update":
        _msg = eval(_message_handle.data["Data"])
        if _msg["msgtype"] == "update":
            try:
                zfused_api.objects.refresh(_msg["update"]["object"], _msg["update"]["object_id"])
            except:
                pass



if __name__ == "__main__":
    import zfused_maya.core.message as message
    def get(me):
        print(me)
    _me = message.MessageMonitor()
    _me.output.connect(get)