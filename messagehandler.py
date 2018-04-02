def blackhole(*args,**kwargs):
    pass
class WeiXinHandler():
    def __init__(self,gotMsgCallback=blackhole,gotImgCallback=blackhole):
        from weixin import WebWeixin
        self.bot=WebWeixin(gotMsgCallback,gotImgCallback)
        '''
        self.gotMsgCallback=gotMsgCallback
    def handlecallback(self,data):
        self.gotMsgCallback(data)
        '''
    def start(self):
        self.bot.start()
    def sendMsg(self,name,word):
        res=self.bot.sendMsg(name,word)
        return res

class MatrixHandler():
    def __init__(self,username,password,room,gotMsgCallback=blackhole):
        try:
            from matrix_client.client import MatrixClient
        except ImportError:
            print("ERR:matrix_client import fail: Please exec:")
            print("cd ./matrix-python-sdk")
            print("pip install ./")
            raise RuntimeError("Failed to import matrix_client sdk")
        self.matrix=MatrixClient("https://matrix.org")
        self.matrix.login_with_password(username=username,password=password)
        self.matrix.start_listener_thread()
        self.room=self.matrix.join_room(room)
        self.room.send_text("Hello!")
        self.room.add_listener(gotMsgCallback)
        #self.gotMsgCallback=gotMsgCallback
    def sendMsg(self,msgData):
        res=self.room.send_text(msgData)
        return res
    def sendImg(self,imgdir):
        with open(imgdir,mode="rb") as f:
            uri=self.matrix.upload(f.read(),"image/jpeg")
            self.room.send_image(uri,'wximg')
            f.close()
    def sendHtml(self,htmlData):
        res=self.room.send_html(htmlData)
        return res
    '''
    def on_matrix_massage(self,event):
        print("got matrix event:",event)
        if event['type'] == "m.room.message":
            if event['content']['msgtype'] == "m.text":
                self.handlecallback(event['content']['body'])
    def handlecallback(self,msgData):
        self.gotMsgCallback(msgData)
    '''
        

if __name__=="__main__":
    MatrixHandler("eternal_flame_wxbridge","kJS31vdaLBs6aB2iYodh","#efwxMsg:matrix.org")