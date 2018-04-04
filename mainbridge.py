from messagehandler import WeiXinHandler,MatrixHandler
import config,time
weixin=None
matrix=None
lastRecipient=""
lastsync=time.asctime(time.localtime())
import os
def delete_file_folder(src):
    '''delete files and folders'''
    if os.path.isfile(src):
        try:
            os.remove(src)
        except:
            pass
    elif os.path.isdir(src):
        for item in os.listdir(src):
            itemsrc=os.path.join(src,item)
            delete_file_folder(itemsrc) 
        try:
            os.rmdir(src)
        except:
            pass

def wx2riot(wxMsgData):
    global weixin,matrix
    matrix.sendMsg(wxMsgData)
def wximg2riot(imgdir):
    global weixin,matrix
    if imgdir.endswith('.jpg'):
        content_type="image/jpeg"
    elif imgdir.endswith(".png"):
        content_type="image/png"
    elif imgdir.endswith('.gif'):
        content_type="image/gif"
    else:
        content_type="image/jpeg"
    matrix.sendImg(imgdir,content_type)
def wxaudio2riot(fdir):
    global weixin,matrix
    matrix.sendAudio(fdir)
def wxSyncSuccessCallback():
    global lastsync
    lastsync=time.asctime(time.localtime())
def riot2wx(room,rtEvent):
    global weixin,matrix,lastRecipient,lastsync
    rtMsgData=""
    print("got matrix event:",rtEvent)
    if rtEvent['type'] == "m.room.message":
        if rtEvent['content']['msgtype'] == "m.text":
            rtMsgData=rtEvent['content']['body']
    sendcmd=rtMsgData.split("<-")
    if len(sendcmd)==2:
        if sendcmd[0]=="":
            sendcmd[0]=lastRecipient
        matrix.sendMsg('Sending to...'+sendcmd[0])
        res=weixin.sendMsg(sendcmd[0],sendcmd[1])
        matrix.sendMsg(str(res))
        lastRecipient=sendcmd[0]
    else:
        if rtMsgData=="getuserlist":
            matrix.sendMsg("Grabbing Userlist:")
            resp=""
            for user in weixin.bot.MemberList:
                resp+=user['NickName']+((' aka: '+user['RemarkName']) if len(user['RemarkName'])>0 else "")+"<br />"
            matrix.sendHtml(resp)
        elif rtMsgData=="status":
            matrix.sendMsg("I'm alive")
            matrix.sendMsg(str(weixin.bot))
            matrix.sendMsg("Last success sync: "+lastsync)
        elif rtMsgData=="cleartrash":
            delete_file_folder("./saved")
            matrix.sendMsg("Clear command sent...")
        elif rtMsgData=="refreshcontact":
            if weixin.refreshContact():
                matrix.sendMsg("Success")
            else:
                matrix.sendMsg("Fail")

def main():
    global weixin,matrix
    matrix=MatrixHandler(config.matrix_username,config.matrix_password,config.matrix_room,gotMsgCallback=riot2wx)
    weixin=WeiXinHandler(gotMsgCallback=wx2riot,gotImgCallback=wximg2riot,gotAudioCallback=wxaudio2riot,syncSuccessCallback=wxSyncSuccessCallback,sendQRCode2Mat=True)
    weixin.start()
if __name__=="__main__":
    main()