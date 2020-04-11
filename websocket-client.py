# coding:utf-8
import json
import websocket


def on_message(ws, message):
    """
    监听消息
    :param ws:
    :param message:
    :return:
    """

    print('收到消息:', json.loads(message))

    print(ws.title)


def on_error(ws, error):
    """
    :param ws:
    :param error:
    :return:
    """
    print('出错了')


def on_close(ws):
    """
    :param ws:
    :return:
    """
    print('已关闭')


def on_open(ws):
    """
    :param ws:
    :return:
    """
    print('打开连接: ', ws.title)
    data = {
        'message': 'hello world'
    }
    ws.send(json.dumps(data))


def start_websocket():
    """
    启动websocket服务
    :return:
    """
    websocket.enableTrace(True)
    uri = 'ws://127.0.0.1:8000/ws/1'
    ws = websocket.WebSocketApp(uri,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open

    ws.title = '我是外部绑定的标题'  # 通过ws设置一个title, 在绑定方法遍可以拿到这个属性

    ws.run_forever()


if __name__ == '__main__':
    start_websocket()
