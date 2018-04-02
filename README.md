# wx2matrix_bridge

## Description
  实在无法忍受手机上装这样一个软件所以写了一个微信2Matrix桥，目前支持文字 语音 图片的转发，使用了matrix-org/matrix-python-sdk（见./matrix-python-sdk/LICENSE）和Urinx/WeixinBot（均为Apache 2.0协议故没有另加LICENSE文件）的代码

## Usage
PS：还没有写daemon的代码所以如果要挂机可以使用screen或者nohup
### 初始化依赖
  pip insall -r requirements.txt
  
  pip install ./matrix-python-sdk/
### 配置文件
  cp ./config.py.sample ./config.py
  
  vim ./config.py
### 运行
  python ./mainbridge.py
### 使用
  所有命令都在matrix房间里发送：
  
  发送消息：【昵称/微信号/备注】<-【内容】 **注意： <-和前面的名称不能有多余的空格！**
  
  发送信息给上一个发送人: <-[内容] **注意：<-前不可有多余的空格**
  
  获取好友列表：getuserlist
  
  检查状态：status
  
  清除媒体文件: cleartrash
### 安全性：
  1. matrix-python-sdk暂时还不支持端到端加密，所以尽量用https的服务器
  2. matrix的房间请不要让其他人加入，目前只要在房间里的人都有权限发送命令
