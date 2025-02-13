# 基于 LLOneBot 实现的 QQ 接入 DeepSeek 小脚本

本项目通过 [LLOneBot](https://github.com/LLOneBot) 实现 QQ 与 [ollama](https://ollama.com) 的接入，允许用户通过 QQ 发送消息并获取 DeepSeek 的响应。

## 功能特性

- **QQ 消息接收与发送**：通过 LLOneBot 实现 QQ 消息的接收与发送。
- **DeepSeek 接入**：将用户发送的消息转发至 Ollama本地模型deepseek-r1，并获取响应返回给用户。
- **简单易用**：只需配置好相关参数，即可快速上手使用。

## 环境要求

- Python 3.8+
- LLOneBot
- Ollama

## 安装与配置

1. **克隆本项目**

   ```bash
   git clone https://github.com/zuitingqingyin/qq-deepseek.git
   cd qq-deepseek
   ```

2. **安装依赖**

   ```bash
   pip install -r requirements.txt
   ```

3.**安装Ollama并配置模型**
  前往官网下载[Ollama](https://ollama.com/)

  打开命令行
  ```bash
  ollama run deepseek-r1:7b//根据你的需求
  ```

4. **配置 LLOneBot**

   在 `config.json` 中配置 请求Ollama 的相关参数：
```json
  {
    "model":"deepseek-r1:8b",
    "host":"localhost",
    "port":11434,
    "temperature":0.7,
    "prompt":"你是一个qq聊天机器人，负责回答用户的问题，与用户进行对话。你将以平和的语气回答问题，并以友善的方式与用户交流。如果用户询问你是谁，你应该回答我是你的聊天助手。现在我们来对话吧！"
  }
```


## 使用说明

1. **启动 LLOneBot**

   确保 LLOneBot 已正确安装并启动。
   在LLOneBOt设置中启用事件上报，添加上报地址。
   ```bash
   http://localhost:8080
   ```

3. **运行脚本**

   ```bash
   python main.py
   ```

4. **在 QQ 中发送消息**

   在 QQ群 中@机器人发送消息，机器人会将消息转发至 本地Ollama 并将响应返回给你。

## 示例

用户发送：

```
@机器人 你好!
```

机器人响应：

```
@用户 你好!有什么我可以帮助你的吗?
```

## 贡献

欢迎提交 Issue 和 Pull Request 来帮助改进本项目。

## 许可证

本项目采用 [MIT 许可证](LICENSE)。

