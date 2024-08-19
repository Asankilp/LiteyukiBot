---
title: liteyuki.comm.channel
order: 1
icon: laptop-code
category: API
---

### ***def*** `set_channel(name: str, channel: Channel) -> None`

设置通道实例

Args:

    name: 通道名称

    channel: 通道实例

### ***def*** `set_channels(channels: dict[str, Channel]) -> None`

设置通道实例

Args:

    channels: 通道名称

### ***def*** `get_channel(name: str) -> Channel`

获取通道实例

Args:

    name: 通道名称

Returns:

### ***def*** `get_channels() -> dict[str, Channel]`

获取通道实例

Returns:

### ***def*** `on_set_channel(data: tuple[str, dict[str, Any]]) -> None`



### ***def*** `on_get_channel(data: tuple[str, dict[str, Any]]) -> None`



### ***def*** `on_get_channels(data: tuple[str, dict[str, Any]]) -> None`



### ***def*** `decorator(func: Callable[[T], Any]) -> Callable[[T], Any]`



### ***async def*** `wrapper(data: T) -> Any`



### ***class*** `Channel(Generic[T])`

通道类，可以在进程间和进程内通信，双向但同时只能有一个发送者和一个接收者

有两种接收工作方式，但是只能选择一种，主动接收和被动接收，主动接收使用 `receive` 方法，被动接收使用 `on_receive` 装饰器

### &emsp; ***def*** `send(self: Any, data: T) -> None`

&emsp;发送数据

Args:

    data: 数据

### &emsp; ***def*** `receive(self: Any) -> T`

&emsp;接收数据

Args:

### &emsp; ***def*** `close(self: Any) -> None`

&emsp;关闭通道

### &emsp; ***def*** `on_receive(self: Any, filter_func: Optional[FILTER_FUNC]) -> Callable[[Callable[[T], Any]], Callable[[T], Any]]`

&emsp;接收数据并执行函数

Args:

    filter_func: 过滤函数，为None则不过滤

Returns:

    装饰器，装饰一个函数在接收到数据后执行
