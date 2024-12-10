
# Open-Webui-Function-Tencent-Hunyuan-AI

[中文](README_CN.md) | English

A plugin for Open-Webui to access Tencent Hunyuan LLM via API key.

---

## Features
- **Integrates Tencent Hunyuan LLM**: Access powerful language processing capabilities directly within Open-Webui.
- **Simple Setup**: Get started quickly with minimal configuration.
- **Docker Compatibility**: Works seamlessly with Docker setups like Unraid.

---
## prerequisite
1. Make sure you have SECRET_ID and SECRET_KEY, which can get on tencent clound website.

## Configuratoin Guide

1. Open the Open-Webui console.
2. Clone the TencentCloud SDK repository:
   ```bash
   git clone https://gitee.com/tencentcloud/tencentcloud-sdk-python.git
   ```
3. Navigate to the cloned directory:
   ```bash
   cd tencentcloud-sdk-python
   ```
4. Install the SDK:
   ```bash
   pip install .
   ```
5. Go to oenwebui offical website to get function or just copy main.py to your funcation library.
   ```bash
   https://openwebui.com/f/lkevincc/tencent_hunyuanai
   ```
6. Nav to function page and click configure button set SECRET_ID and SECRET_KEY, which can get on tencent clound website.

---
## Others

1. You can find logo [here](https://lobehub.com/icons/hunyuan)


## Usage
After installation, use your Tencent Cloud API key to enable access to Hunyuan LLM in Open-Webui. Check the [official documentation](llm.hunyuan.tencent.com) for API details.
