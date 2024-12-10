
# Open-Webui-Function-Tencent-Hunyuan-AI

[English](README_EN.md) | 中文

用于 Open-Webui 的插件，通过 API 密钥接入腾讯混元大模型。

---
## 前置条件
1. 确保您拥有 SECRET_ID 和 SECRET_KEY，可在腾讯云官网获取。

## 配置指南

1. 打开 Open-Webui 的Docker控制台。
2. 克隆 TencentCloud SDK 仓库：
   ```bash
   git clone https://gitee.com/tencentcloud/tencentcloud-sdk-python.git
   ```
3. 进入克隆的目录：
   ```bash
   cd tencentcloud-sdk-python
   ```
4. 安装 SDK：
   ```bash
   pip install .
   ```
5. 前往 OpenWebui 官方网站获取功能模块，或直接将 main.py 复制到您的功能库中。
   ```bash
   https://openwebui.com/f/lkevincc/tencent_hunyuanai
   ```
6. 进入功能页面，点击配置按钮，设置 SECRET_ID 和 SECRET_KEY，可在腾讯云官网获取。

---
## 其他信息

1. 您可以在 [此处](https://lobehub.com/icons/hunyuan) 获取 Logo。

## 使用方法
安装完成后，通过您的腾讯云 API 密钥在 Open-Webui 中启用混元大模型访问功能。有关 API 详细信息，请查看[官方文档](llm.hunyuan.tencent.com)。
