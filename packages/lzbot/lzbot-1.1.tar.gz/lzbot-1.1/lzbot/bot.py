import json
import os
import requests
import asyncio
import websocket
import threading
from .logging import get_logger
_log = get_logger()

class Bot:
    def __init__(self,ws_url):
        self.ws_url = ws_url
        
    def send_text(self, group_id, user_id, data):
        """发送群消息的函数"""
        return requests.post(
                    "http://localhost:3000/send_group_msg",
                    json={
                        "group_id": group_id,
                        "message": [
                            {"type": "at", "data": {"qq": user_id}},
                            {"type": "text", "data": {"text": f"\n{data}"}}
                        ]
                    }
                )


    def send_image(self, group_id,user_id,summary, file_image):
        """发送群消息的函数"""
        try:
            # 获取当前文件所在目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # 获取父目录
            parent_dir = os.path.dirname(current_dir)
            
            # 将相对路径转换为绝对路径，双杠的
            # 原因是绝对路径中不能出现单杠，而在 Windows 系统中，路径分隔符为双杠
            # 所以需要将相对路径中的单杠转换为双杠
            absolute_image_path = os.path.join(parent_dir, file_image).replace("\\", "\\\\")
            response = requests.post(
                "http://localhost:3000/send_group_msg",
                
                json={
                    "group_id": group_id,
                    "message": [{"type": "at", "data": {"qq": user_id}},
                                    {
                                    "type": "image",
                                    "data": {
                                        "file": f"file://{absolute_image_path}",
                                        "summary": f"{summary}"
                                    }
                                    }
                                ]
                }
            )
            response.raise_for_status()
        except requests.RequestException as e:
            _log.error(f"[botpy] 发送群消息失败: {e}")


    def parse_message(self, message):
        """解析消息的函数"""
        try:
            message_dict = json.loads(message)
            return message_dict
        except json.JSONDecodeError:
            _log.error(f"[botpy] 消息解析失败: {message}")
            return None

    async def on_group_message(self, message):
        """处理群消息的异步方法"""
        pass  # 这里可以在子类中重写

    def on_message(self, ws, message):
        """WebSocket 消息接收的回调函数"""
        message_dict = self.parse_message(message)
        self_id = message_dict.get("self_id")
        if message_dict and "post_type" in message_dict:
            if message_dict["post_type"] == "message" and message_dict["message_type"] == "group" and message_dict["raw_message"].startswith(f"[CQ:at,qq={self_id}]"):
                # 处理群消息
                asyncio.run(self.on_group_message(message_dict))

    def on_error(self, ws, error):
        _log.error(f"[botpy] WebSocket 连接出错: {error}")

    def on_close(self, ws):
        _log.info("[botpy] WebSocket 连接关闭")

    def on_open(self, ws):
        _log.info("[botpy] WebSocket 连接成功")

    def run_websocket(self):
        """定义 WebSocket 连接的函数"""

        ws = websocket.WebSocketApp(
            self.ws_url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        
        # 在新线程启动 WebSocket
        threading.Thread(target=ws.run_forever).start()
        _log.info(f"[botpy] WebSocket 连接成功: {self.ws_url}")


