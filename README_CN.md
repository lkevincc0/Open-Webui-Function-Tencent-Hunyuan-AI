
# Open-Webui-Function-Tencent-Hunyuan-AI

[English](README.md) | 中文

用于 Open-Webui 的插件，通过 API 密钥接入腾讯混元大模型。

---

## 功能特色
- **接入腾讯混元大模型**：在 Open-Webui 中直接使用强大的语言处理能力。
- **简单设置**：快速开始，配置简单。
- **支持 Docker**：无缝兼容如 Unraid 的 Docker 部署。

---

## 安装指南

1. 打开 Open-Webui 控制台。
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

---

## 使用方法
安装完成后，通过您的腾讯云 API 密钥在 Open-Webui 中启用混元大模型访问功能。有关 API 详细信息，请查看[官方文档](https://cloud.tencent.com/document/product/xxx)。
