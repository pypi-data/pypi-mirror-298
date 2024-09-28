# -*- coding: utf-8 -*-
import asyncio
import json
import traceback
from datetime import datetime
from typing import Optional
from aiohttp import WSMessage, ClientWebSocketResponse, TCPConnector, ClientSession, WSMsgType
from ssl import SSLContext
from . import logging
from .connection import ConnectionSession
from .types import gateway
from .types.session import Session

_log = logging.get_logger()


class BotWebSocket:
    """Bot的Websocket实现

    CODE	名称	客户端操作	描述
    0	Dispatch	Receive	服务端进行消息推送
    1	Heartbeat	Send/Receive	客户端或服务端发送心跳
    2	Identify	Send	客户端发送鉴权
    6	Resume	Send	客户端恢复连接
    7	Reconnect	Receive	服务端通知客户端重新连接
    9	Invalid Session	Receive	当identify或resume的时候，如果参数有错，服务端会返回该消息
    10	Hello	Receive	当客户端与网关建立ws连接之后，网关下发的第一条消息
    11	Heartbeat ACK	Receive	当发送心跳成功之后，就会收到该消息
    """

    WS_DISPATCH_EVENT = 0
    WS_HEARTBEAT = 1
    WS_IDENTITY = 2
    WS_RESUME = 6
    WS_RECONNECT = 7
    WS_INVALID_SESSION = 9
    WS_HELLO = 10
    WS_HEARTBEAT_ACK = 11

    def __init__(self, session: Session, _connection: ConnectionSession):
        """初始化BotWebSocket类的实例
        
        :param session: 会话信息
        :param _connection: 连接会话
        """
        self._conn: Optional[ClientWebSocketResponse] = None
        self._session = session
        self._connection = _connection
        self._parser = _connection.parser
        self._can_reconnect = True
        self._INVALID_RECONNECT_CODE = [9001, 9005]
        self._AUTH_FAIL_CODE = [4004]

    async def on_error(self, exception: BaseException):
        """处理WebSocket连接中的错误
        
        :param exception: 异常信息
        """
        _log.error("[botpy] websocket连接: %s, 异常信息 : %s" % (self._conn, exception))
        traceback.print_exc()
        self._connection.add(self._session)

    async def on_closed(self, close_status_code, close_msg):
        """处理WebSocket连接关闭的事件
        
        :param close_status_code: 关闭状态码
        :param close_msg: 关闭信息
        """
        _log.info("[botpy] 关闭, 返回码: %s" % close_status_code + ", 返回信息: %s" % close_msg)
        if close_status_code in self._AUTH_FAIL_CODE:
            _log.info("[botpy] 鉴权失败，重置token...")
            self._session["token"].access_token = None
        # 这种不能重新链接
        if close_status_code in self._INVALID_RECONNECT_CODE or not self._can_reconnect:
            _log.info("[botpy] 无法重连，创建新连接!")
            self._session["session_id"] = ""
            self._session["last_seq"] = 0
        # 断连后启动一个新的链接并透传当前的session，不使用内部重连的方式，避免死循环
        self._connection.add(self._session)

    async def on_message(self, ws, message):
        """处理接收到的消息
        
        :param ws: WebSocket对象
        :param message: 接收到的消息内容
        """
        _log.debug("[botpy] 接收消息: %s" % message)
        msg = json.loads(message)
        

        if await self._is_system_event(msg, ws):
            return

        event = msg.get("t")
        opcode = msg.get("op")
        event_seq = msg["s"]
        if event_seq > 0:
            self._session["last_seq"] = event_seq

        if event == "READY":
            # 心跳检查
            self._connection.loop.create_task(self._send_heart(interval=30))
            ready = await self._ready_handler(msg)
            _log.info(f"[botpy] 机器人「{ready['user']['username']}」启动成功！")

        if event == "RESUMED":
            # 心跳检查
            self._connection.loop.create_task(self._send_heart(interval=30))
            _log.info("[botpy] 机器人重连成功! ")

        if event and opcode == self.WS_DISPATCH_EVENT:
            event = msg["t"].lower()
            try:
                func = self._parser[event]
            except KeyError:
                _log.error("_parser unknown event %s.", event)
            else:
                func(msg)

    async def on_connected(self, ws: ClientWebSocketResponse):
        """处理WebSocket连接成功事件
        
        :param ws: WebSocket对象
        """
        self._conn = ws
        if self._conn is None:
            raise Exception("[botpy] websocket连接失败")
        if self._session["session_id"]:
            await self.ws_resume()
        else:
            await self.ws_identify()

    async def ws_connect(self):
        """发起WebSocket连接，并定时发送心跳"""
        _log.info("[botpy] 启动中...")
        ws_url = self._session["url"]
        if not ws_url:
            raise Exception("[botpy] 会话url为空")

        # adding SSLContext-containing connector to prevent SSL certificate verify failed error
        async with ClientSession(connector=TCPConnector(limit=10, ssl=SSLContext())) as session:
            async with session.ws_connect(self._session["url"]) as ws_conn:
                while True:
                    msg: WSMessage
                    msg = await ws_conn.receive()
                    if msg.type == WSMsgType.TEXT:
                        await self.on_message(ws_conn, msg.data)
                    elif msg.type == WSMsgType.ERROR:
                        await self.on_error(ws_conn.exception())
                        await ws_conn.close()
                    elif msg.type == WSMsgType.CLOSED or msg.type == WSMsgType.CLOSE:
                        await self.on_closed(ws_conn.close_code, msg.extra)
                    if ws_conn.closed:
                        _log.info("[botpy] ws关闭, 停止接收消息!")
                        break

    async def ws_identify(self):
        """websocket鉴权"""
        if not self._session["intent"]:
            self._session["intent"] = 1

        _log.info("[botpy] 鉴权中...")
        await self._session["token"].check_token()
        payload = {
            "op": self.WS_IDENTITY,
            "d": {
                "shard": [
                    self._session["shards"]["shard_id"],
                    self._session["shards"]["shard_count"],
                ],
                "token": self._session["token"].get_string(),
                "intents": self._session["intent"],
            },
        }

        await self.send_msg(json.dumps(payload))

    async def send_msg(self, event_json):
        """发送WebSocket消息
        
        :param event_json: 消息内容
        """
        send_msg = event_json
        _log.debug("[botpy] 发送消息: %s" % send_msg)
        if isinstance(self._conn, ClientWebSocketResponse):
            if self._conn.closed:
                _log.debug("[botpy] ws连接已关闭! ws对象: %s" % self._conn)
            else:
                await self._conn.send_str(data=send_msg)

    async def ws_resume(self):
        """恢复WebSocket连接"""
        _log.info("[botpy] 重连启动...")
        await self._session["token"].check_token()
        payload = {
            "op": self.WS_RESUME,
            "d": {
                "token": self._session["token"].get_string(),
                "session_id": self._session["session_id"],
                "seq": self._session["last_seq"],
            },
        }

        await self.send_msg(json.dumps(payload))

    async def _ready_handler(self, message_event) -> gateway.ReadyEvent:
        """处理准备就绪事件
        
        :param message_event: 消息事件
        :return: 就绪事件数据
        """
        data = message_event["d"]
        self.version = data["version"]
        self._session["session_id"] = data["session_id"]
        self._session["shards"]["shard_id"] = data["shard"][0]
        self._session["shards"]["shard_count"] = data["shard"][1]
        self.user = data["user"]
        return data

    async def _is_system_event(self, message_event, ws):
        """检查是否为系统事件
        
        :param message_event: 消息事件
        :param ws: WebSocket对象
        :return: 是否为系统事件
        """
        event_op = message_event["op"]
        if event_op == self.WS_HELLO:
            await self.on_connected(ws)
            return True
        if event_op == self.WS_HEARTBEAT_ACK:
            return True
        if event_op == self.WS_RECONNECT:
            self._can_reconnect = True
            return True
        if event_op == self.WS_INVALID_SESSION:
            self._can_reconnect = False
            return True
        return False

    async def _send_heart(self, interval):
        """发送心跳包
        
        :param interval: 间隔时间
        """
        _log.info("[botpy] 心跳维持启动...")
        while True:
            payload = {
                "op": self.WS_HEARTBEAT,
                "d": self._session["last_seq"],
            }

            if self._conn is None:
                _log.debug("[botpy] 连接已关闭!")
                return
            if self._conn.closed:
                _log.debug("[botpy] ws连接已关闭, 心跳检测停止，ws对象: %s" % self._conn)
                return

            await self.send_msg(json.dumps(payload))
            await asyncio.sleep(interval)


class NewWebSocket:
    received_data = None
    """新的 WebSocket 实现"""

    def __init__(self, url, show_heartbeat_info=False,show_system_message=False):
        """初始化NewWebSocket类的实例
        
        :param url: WebSocket服务器的URL
        :param show_heartbeat_info: 是否显示心跳信息
        """
        self.url = url
        self._conn: Optional[ClientWebSocketResponse] = None
        self.is_connected = False  # 启动连接判断标志
        self.startup_info = {}  # 用于保存启动相关参数
        self.show_heartbeat_info = show_heartbeat_info  # 控制心跳信息显示
        self.show_system_message = show_system_message  # 控制系统消息显示
    async def on_error(self, exception: BaseException):
        """处理WebSocket连接中的错误
        
        :param exception: 异常信息
        """
        _log.error("[NewWebSocket] 连接错误: %s" % exception)
        traceback.print_exc()

    async def on_closed(self, close_status_code, close_msg):
        """处理WebSocket连接关闭的事件
        
        :param close_status_code: 关闭状态码
        :param close_msg: 关闭信息
        """
        _log.info("[NewWebSocket] 关闭, 返回码: %s, 返回信息: %s" % (close_status_code, close_msg))

    async def on_message(self, ws, message):
        """处理接收到的消息
        
        :param ws: WebSocket对象
        :param message: 接收到的消息内容
        """
        _log.debug("[NewWebSocket] 接收消息: %s" % message)
        try:
            json_data = json.loads(message)
            await self.handle_message(json_data)
        except json.JSONDecodeError:
            _log.error("[NewWebSocket] JSON 解码错误: %s" % message)

    async def handle_message(self, json_data):
        NewWebSocket.received_data = json_data
        """处理接收到的 JSON 数据
        
        :param json_data: 解析后的 JSON 数据
        """
        # 检查是否为启动标志
        if json_data.get('post_type') == 'meta_event':
            if json_data.get('meta_event_type') == 'lifecycle' and json_data.get('sub_type') == 'connect':
                self.is_connected = True  # 设置连接成功标志
                
                # 保存启动相关参数
                self.startup_info = {
                    'time': json_data.get('time'),
                    'self_id': json_data.get('self_id'),
                }
                
                # 转换时间戳为可读格式
                readable_time = datetime.fromtimestamp(self.startup_info['time']).strftime('%Y-%m-%d %H:%M:%S')
                _log.info(
                    "[NewWebSocket] 机器人QQ号 %s 成功连接，连接时间: %s" % (
                        self.startup_info['self_id'],
                        readable_time
                    )
                )
                return  # 直接返回，不继续处理此消息

            # 检查是否为心跳消息
            if json_data.get('meta_event_type') == 'heartbeat':
                if self.show_heartbeat_info:  # 判断是否显示心跳信息
                    online_status = json_data['status']['online']
                    good_status = json_data['status']['good']
                    interval = json_data.get('interval', 0)

                    # 记录心跳消息状态
                    _log.info(
                        "[NewWebSocket] 心跳检测: 在线状态: %s, 状态良好: %s, 心跳间隔: %dms" % (
                            online_status,
                            good_status,
                            interval
                        )
                    )
                return  # 直接返回，不继续处理此消息

        # 这里可以处理正常的消息（如果需要）
        if self.show_system_message:
            _log.info("[NewWebSocket] 接收到新消息: %s" % json_data)



    async def connect(self):
        """发起WebSocket连接"""
        _log.info("[NewWebSocket] 启动中...")
        async with ClientSession(connector=TCPConnector(limit=10, ssl=SSLContext())) as session:
            async with session.ws_connect(self.url) as ws_conn:
                self._conn = ws_conn
                while True:
                    msg: WSMessage
                    msg = await ws_conn.receive()
                    
                    if msg.type == WSMsgType.TEXT:
                        await self.on_message(ws_conn, msg.data)
                    elif msg.type == WSMsgType.ERROR:
                        await self.on_error(ws_conn.exception())
                        await ws_conn.close()
                    elif msg.type == WSMsgType.CLOSED or msg.type == WSMsgType.CLOSE:
                        await self.on_closed(ws_conn.close_code, msg.extra)
                        break

                if ws_conn.closed:
                    _log.info("[NewWebSocket] ws关闭, 停止接收消息!")
