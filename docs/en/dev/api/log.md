---
title: liteyuki.log
---
### *func* `get_format() -> str`


<details>
<summary> <b>Source code</b> </summary>

```python
def get_format(level: str) -> str:
    if level == 'DEBUG':
        return debug_format
    else:
        return default_format
```
</details>

### *func* `init_log()`



**Description**: 在语言加载完成后执行


<details>
<summary> <b>Source code</b> </summary>

```python
def init_log(config: dict):
    """
    在语言加载完成后执行
    Returns:

    """
    logger.remove()
    logger.add(sys.stdout, level=0, diagnose=False, format=get_format(config.get('log_level', 'INFO')))
    show_icon = config.get('log_icon', True)
    logger.level('DEBUG', color='<blue>', icon=f"{('🐛' if show_icon else '')}DEBUG")
    logger.level('INFO', color='<normal>', icon=f"{('ℹ️' if show_icon else '')}INFO")
    logger.level('SUCCESS', color='<green>', icon=f"{('✅' if show_icon else '')}SUCCESS")
    logger.level('WARNING', color='<yellow>', icon=f"{('⚠️' if show_icon else '')}WARNING")
    logger.level('ERROR', color='<red>', icon=f"{('⭕' if show_icon else '')}ERROR")
```
</details>

### ***var*** `debug_format = '<c>{time:YYYY-MM-DD HH:mm:ss}</c> <lvl>[{level.icon}]</lvl> <c><{name}.{module}.{function}:{line}></c> {message}'`

- **Type**: `str`

### ***var*** `default_format = '<c>{time:MM-DD HH:mm:ss}</c> <lvl>[{level.icon}]</lvl> <c><{name}></c> {message}'`

- **Type**: `str`

