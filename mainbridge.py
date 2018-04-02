from messagehandler import WeiXinHandler,MatrixHandler
import config,time
weixin=None
matrix=None
def wx2riot(wxMsgData):
    global weixin,matrix
    matrix.sendMsg(wxMsgData)
def riot2wx(room,rtEvent):
    global weixin,matrix
    rtMsgData=""
    print("got matrix event:",rtEvent)
    if rtEvent['type'] == "m.room.message":
        if rtEvent['content']['msgtype'] == "m.text":
            rtMsgData=rtEvent['content']['body']
    sendcmd=rtMsgData.split("<-")
    if len(sendcmd)==2:
        matrix.sendMsg('Sending...')
        res=weixin.sendMsg(sendcmd[0],sendcmd[1])
        matrix.sendMsg(str(res))
    else:
        if rtMsgData=="getuserlist":
            matrix.sendMsg("Grabbing Userlist:")
            resp=""
            for user in weixin.bot.MemberList:
                resp+=user['NickName']+((' aka: '+user['RemarkName']) if len(user['RemarkName'])>0 else "")+"<br />"
            matrix.sendHtml(resp)
        elif rtMsgData=="checkalive":
            matrix.sendMsg("I'm alive")
def main():
    global weixin,matrix
    matrix=MatrixHandler(config.matrix_username,config.matrix_password,config.matrix_room,gotMsgCallback=riot2wx)
    weixin=WeiXinHandler(gotMsgCallback=wx2riot)
    weixin.start()
if __name__=="__main__":
    main()