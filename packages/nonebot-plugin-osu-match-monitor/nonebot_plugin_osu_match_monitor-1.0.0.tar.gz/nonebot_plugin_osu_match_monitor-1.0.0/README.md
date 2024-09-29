<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-osu-match-monitor/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-osu-match-monitor/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-osu-match-monitor

_✨ NoneBot osu! 比赛监控 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/Sevenyine/nonebot-plugin-osu-match-monitor.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-osu-match-monitor">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-osu-match-monitor.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">

</div>

## 📖 介绍

这是一个监控 osu! 游戏比赛并自动将动态播报到 QQ 群内的插件。

## 💿 安装

使用 nb-cli 安装

在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-osu-match-monitor


## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

| 配置项 | 必填 | 默认值 | 类型 |
|:-----:|:----:|:----:|:----:|
| osu_api_key | 是 | "" | str |
| osu_refresh_interval | 否 | 2 | int |

## 🎉 使用
### 指令表

在使用时，请自行添加对应的指令前缀。

| 指令 | 权限 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| osu match monitor <id> | 群员 | 否 | 群聊+私聊 | 开始监控比赛 |
| osu match stop <id> | 群员 | 否 | 群聊+私聊 | 停止监控比赛 |
### 效果图

