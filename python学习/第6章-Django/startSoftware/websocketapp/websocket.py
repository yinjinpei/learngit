from channels.generic.websocket import AsyncJsonWebsocketConsumer


# 这里继承了AsyncJsonWebsocketConsumer类，该类是异步且支持接收或发送josn,实际上在WebsocketConsumer上的做的封装
class WbConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # 当客户端发起连接直接接受连接
        await self.accept()

    async def disconnect(self, code):
        # 断开连接后会调用次方法
        print('关闭连接')

    async def receive_json(self, content, **kwargs):
        # 收到客户端发送的信息在进行回复
        print('接收数据:', content)

        await self.send_json(content={
            'message': '收到收到over!'
        })