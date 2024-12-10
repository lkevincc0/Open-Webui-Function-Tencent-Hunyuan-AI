"""
title: Open-Webui-Function-Tencent-Hunyuan-AI
author: lkevincc0
author_url: https://github.com/lkevincc0
funding_url: https://github.com/open-webui
version: 1.0.0
license: MIT
"""
# Insipired by Google GenAI - justinh-rahb
# how to use 
# Nav to function page and click configure button set SECRET_ID and SECRET_KEY, which can get on tencent clound website.
# 导航至函数页面然后点击配置按钮，设置 SECRET_ID 和 SECRET_KEY（可在腾讯云网站上获取）。

import os
import json
from typing import List, Union, Iterator
from pydantic import BaseModel, Field
import tencentcloud.common.exception.tencent_cloud_sdk_exception as exce
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.credential import Credential
from tencentcloud.hunyuan.v20230901 import hunyuan_client, models

# Set DEBUG = True to enable detailed logging
DEBUG = False


class Pipe:
    class Valves(BaseModel):
        SECRET_ID: str = Field(default="")
        SECRET_KEY: str = Field(default="")
        USE_PERMISSIVE_SAFETY: bool = Field(default=False)

    def __init__(self):
        self.id = "tencent_hunyuan"
        self.type = "manifold"
        self.name = "Tencent Hunyuan: "
        self.valves = self.Valves(
            **{
                "SECRET_ID": os.getenv("TENCENT_SECRET_ID", ""),
                "SECRET_KEY": os.getenv("TENCENT_SECRET_KEY", ""),
                "USE_PERMISSIVE_SAFETY": False,
            }
        )

    def get_tencent_models(self) -> List[dict]:
        if not self.valves.SECRET_ID or not self.valves.SECRET_KEY:
            return [
                {
                    "id": "error",
                    "name": "SECRET_ID or SECRET_KEY is not set. Please update the credentials in the valves.",
                }
            ]
        try:
            available_models = [
                {"id": "hunyuan-lite", "name": "Hunyuan Lite"},
                {"id": "hunyuan-translation-lite", "name": "Hunyuan Translation Lite"},
                {"id": "hunyuan-pro", "name": "Hunyuan Pro"},
                {"id": "hunyuan-standard", "name": "Hunyuan Standard"},
                {"id": "hunyuan-standard-256", "name": "Hunyuan Standard 256"},
                {"id": "hunyuan-code", "name": "Hunyuan Code"},
                {"id": "hunyuan-functioncall", "name": "Hunyuan functioncall"},
                {"id": "hunyuan-large", "name": "Hunyuan Large"},
                {"id": "hunyuan-large-longcontext", "name": "Hunyuan Large Longcontext"},
                {"id": "hunyuan-turbo", "name": "Hunyuan Turbo"},
                {"id": "hunyuan-turbo-latest", "name": "Hunyuan Turbo Latest"},
            ]

            if DEBUG:
                print("Available Models:", available_models)

            return available_models
        except exce.TencentCloudSDKException as e:
            if DEBUG:
                print(f"Error fetching Tencent models: {e}")
            return [
                {
                    "id": "error",
                    "name": f"Could not fetch models from Tencent: {str(e)}",
                }
            ]

    def pipes(self) -> List[dict]:
        return self.get_tencent_models()

    def pipe(self, body: dict) -> Union[str, Iterator[str]]:
        if not self.valves.SECRET_ID or not self.valves.SECRET_KEY:
            return "Error: SECRET_ID or SECRET_KEY is not set"

        try:
            credential = Credential(self.valves.SECRET_ID, self.valves.SECRET_KEY)
            http_profile = HttpProfile()
            http_profile.req_method = "POST"
            http_profile.req_timeout = 30
            http_profile.endpoint = "hunyuan.tencentcloudapi.com"

            client_profile = ClientProfile()
            client_profile.http_profile = http_profile

            client = hunyuan_client.HunyuanClient(credential, "", client_profile)
            req = models.ChatCompletionsRequest()


            model_id = body["model"]

            if "." in model_id:
                parts = model_id.split(".", 1)
                model_id = parts[-1]

            # if you wanna force (for debug)
            # if model_id != "hunyuan-lite":
                # return f"Error: Invalid model name format: {model_id}"

            messages = body["messages"]
            if not messages:
                return "Error: Messages must contain at least 1 item"

            if DEBUG:
                print("Incoming body:", json.dumps(body, ensure_ascii=False, indent=2))

            # standard message
            system_message = None
            normalized_messages = []
            for m in messages:
                role = m.get("Role", m.get("role"))
                content = m.get("Content", m.get("content"))
                if not role or content is None:
                    return "Error: Each message must have 'Role' and 'Content' keys."

                if isinstance(content, list):
                    parts = []
                    for c in content:
                        if c.get("type") == "text":
                            parts.append(c["text"])
                        elif c.get("type") == "image_url":
                            image_url = c["image_url"]["url"]
                            parts.append(f"[IMAGE: {image_url}]")
                    content = " ".join(parts)

                if role == "system":
                    system_message = content
                else:
                    normalized_messages.append({"Role": role, "Content": content})

            # System message
            if system_message:
                normalized_messages.insert(
                    0, {"Role": "system", "Content": f"System: {system_message}"}
                )

            if len(normalized_messages) == 0:
                return "Error: After processing, no valid messages found."

            params = {
                "TopP": body.get("TopP", 1),
                "Temperature": body.get("Temperature", 0.7),
                "Model": model_id,
                "Stream": body.get("Stream", False),
                "Messages": normalized_messages,
            }

            # security settings
            if self.valves.USE_PERMISSIVE_SAFETY:
                params["SafetySettings"] = {
                    "Harassment": "None",
                    "HateSpeech": "None",
                    "SexuallyExplicit": "None",
                    "DangerousContent": "None",
                }
            else:
                params["SafetySettings"] = body.get("SafetySettings", {})

            req.from_json_string(json.dumps(params, ensure_ascii=False))

            if DEBUG:
                print("Tencent API request:")
                print("  Model:", model_id)
                print(
                    "  Messages:",
                    json.dumps(normalized_messages, ensure_ascii=False, indent=2),
                )
                print("  Parameters:", json.dumps(params, ensure_ascii=False, indent=2))

            stream = params["Stream"]
            if stream:
                # stream logic
                return "Streaming not supported in this implementation."
            else:
                resp = client.ChatCompletions(req)
                response_data = json.loads(resp.to_json_string())

                if (
                    "Choices" in response_data
                    and isinstance(response_data["Choices"], list)
                    and len(response_data["Choices"]) > 0
                    and "Message" in response_data["Choices"][0]
                    and "Content" in response_data["Choices"][0]["Message"]
                ):
                    content = response_data["Choices"][0]["Message"]["Content"]
                    return content
                else:
                    return "No content returned."

        except exce.TencentCloudSDKException as err:
            if DEBUG:
                print(f"Error in pipe method: {err}")
            return f"Error: {err}"
