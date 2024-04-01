import asyncio
import io
from urllib.parse import quote

import aiofiles
from PIL import Image
import aiohttp
import nonebot
from nonebot.adapters.onebot import v11, v12
from typing import Any

from . import load_from_yaml
from .liteyuki_api import liteyuki_api
from .ly_typing import T_Bot, T_MessageEvent

config = load_from_yaml("config.yml")


class Markdown:
    @staticmethod
    async def send_md(
            markdown: str,
            bot: T_Bot, *,
            message_type: str = None,
            session_id: str | int = None,
            event: T_MessageEvent = None,
            **kwargs
    ) -> dict[str, Any]:
        formatted_md = v11.unescape(markdown).replace("\n", r"\n").replace('"', r'\\\"')
        if event is not None and message_type is None:
            message_type = event.message_type
            session_id = event.user_id if event.message_type == "private" else event.group_id
        try:
            forward_id = await bot.call_api(
                api="send_forward_msg",
                messages=[
                        v11.MessageSegment(
                            type="node",
                            data={
                                    "name"   : "Liteyuki.OneBot",
                                    "uin"    : bot.self_id,
                                    "content": [
                                            {
                                                    "type": "markdown",
                                                    "data": {
                                                            "content": '{"content":"%s"}' % formatted_md
                                                    }
                                            },
                                    ]
                            },
                        )
                ]
            )
            data = await bot.send_msg(
                user_id=session_id,
                group_id=session_id,
                message_type=message_type,
                message=[
                        v11.MessageSegment(
                            type="longmsg",
                            data={
                                    "id": forward_id
                            }
                        ),
                ],
                **kwargs
            )
        except Exception as e:
            nonebot.logger.warning("send_markdown error, send as plain text: %s" % e.__repr__())
            if isinstance(bot, v11.Bot):
                data = await bot.send_msg(
                    message_type=message_type,
                    message=markdown,
                    user_id=int(session_id),
                    group_id=int(session_id),
                    **kwargs
                )
            elif isinstance(bot, v12.Bot):
                data = await bot.send_message(
                    detail_type=message_type,
                    message=v12.Message(
                        v12.MessageSegment.text(
                            text=markdown
                        )
                    ),
                    user_id=str(session_id),
                    group_id=str(session_id),
                    **kwargs
                )
            else:
                nonebot.logger.error("send_markdown: bot type not supported")
                data = {}
        return data

    @staticmethod
    async def send_image(
            image: bytes | str,
            bot: T_Bot, *,
            message_type: str = None,
            session_id: str | int = None,
            event: T_MessageEvent = None,
            **kwargs
    ) -> dict:
        """
        发送单张装逼大图
        Args:
            image: 图片字节流或图片本地路径，链接请使用Markdown.image_async方法获取后通过send_md发送
            bot: bot instance
            message_type: message type
            session_id: session id
            event: event
            kwargs: other arguments
        Returns:
            dict: response data

        """
        print("\n\n\n发送图片\n\n\n")
        if isinstance(image, str):
            async with aiofiles.open(image, "rb") as f:
                image = await f.read()
        # 1.轻雪图床方案
        image_url = await liteyuki_api.upload_image(image)
        image_size = Image.open(io.BytesIO(image)).size
        image_md = Markdown.image(image_url, image_size)
        return await Markdown.send_md(image_md, bot, message_type=message_type, session_id=session_id, event=event, **kwargs)

        # 2.此方案等林文轩修好后再用QQ图床，再嵌入markdown发送
        # image_message_id = (await bot.send_private_msg(
        #     user_id=bot.self_id,
        #     message=[
        #         v11.MessageSegment.image(file=image)
        #     ]
        # ))["message_id"]
        # await asyncio.sleep(3)
        # await bot.delete_msg(message_id=image_message_id)
        # image_message = await bot.get_msg(message_id=image_message_id)
        # image_url = (await bot.get_msg(message_id=image_message_id))["message"][0]["data"]["url"]
        # image_size = Image.open(io.BytesIO(image)).size
        # image_md = Markdown.image(image_url, image_size)
        # return await Markdown.send_md(image_md, bot, message_type=message_type, session_id=session_id, event=event, **kwargs)

    @staticmethod
    async def get_image_url(image: bytes | str, bot: T_Bot) -> str:
        """把图片上传到图床，返回链接
        Args:
            bot: 发送的bot
            image: 图片字节流或图片本地路径
        Returns:
        """
        # 等林文轩修好Lagrange.OneBot再说

    @staticmethod
    def button(name: str, cmd: str, reply: bool = False, enter: bool = True) -> str:
        """生成点击回调按钮
        Args:
            name: 按钮显示内容
            cmd: 发送的命令，已在函数内url编码，不需要再次编码
            reply: 是否以回复的方式发送消息
            enter: 自动发送消息则为True，否则填充到输入框

        Returns:
            markdown格式的可点击回调按钮

        """
        if "" not in config.get("command_start", ["/"]) and config.get("alconna_use_command_start", False):
            cmd = f"{config['command_start'][0]}{cmd}"
        return f"[{name}](mqqapi://aio/inlinecmd?command={quote(cmd)}&reply={str(reply).lower()}&enter={str(enter).lower()})"

    @staticmethod
    def link(name: str, url: str) -> str:
        """生成点击链接按钮
        Args:
            name: 链接显示内容
            url: 链接地址

        Returns:
            markdown格式的链接

        """
        return f"[🔗{name}]({url})"

    @staticmethod
    def image(url: str, size: tuple[int, int]) -> str:
        """构建图片链接
        Args:
            size:
            url: 图片链接

        Returns:
            markdown格式的图片

        """
        return f"![image #{size[0]}px #{size[1]}px]({url})"

    @staticmethod
    async def image_async(url: str) -> str:
        """获取图片，自动请求获取大小，异步
        Args:
            url: 图片链接

        Returns:
            图片Markdown语法: ![image #{width}px #{height}px](link)

        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    image = Image.open(io.BytesIO(await resp.read()))
                    return Markdown.image(url, image.size)
        except Exception as e:
            nonebot.logger.error(f"get image error: {e}")
            return "[Image Error]"

    @staticmethod
    def escape(text: str) -> str:
        """转义特殊字符
        Args:
            text: 需要转义的文本，请勿直接把整个markdown文本传入，否则会转义掉所有字符

        Returns:
            转义后的文本

        """
        chars = "*[]()~_`>#+=|{}.!"
        for char in chars:
            text = text.replace(char, f"\\\\{char}")
        return text
