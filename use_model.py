
import json
import langchain
import langchain_community
from langchain_ollama import OllamaLLM as Ollama
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
import re
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
import os

os.environ["OPENAI_API_KEY"]="yourapikey"
os.environ["OPENAI_API_BASE"]="https://api.deepseek.com"
store = {} #对话记忆，根据user_id来区分不同的对话
scenario_store = {}#对应的情景存储
# 获取配置
def get_config()->dict:
    with open("config.json",'r',encoding='utf-8') as f:
        config=json.loads(f.read())
    return config


# 隐藏思考的过程
def hide_think(response)->str:
    response=re.sub(r"<think>\n.*\n</think>","",response,flags=re.DOTALL)
    return response

# 初始化模型
def init_model(model, scenarios, temperature, scenario_name):
    messages = [
        {"role":"system","content": scenarios[scenario_name]},
        {"role":"user","content": "{input}"}
    ]



    llm = ChatOpenAI(model=model,temperature=temperature)
    output_parser=StrOutputParser()
    prompttemplate = ChatPromptTemplate.from_messages(
		messages=messages
	)

    r = prompttemplate|llm|output_parser

    return r

# 获取对话历史
def get_session_history(user_id):
    if user_id not in store:
        store[user_id] = ChatMessageHistory()
    return store[user_id]

# 使用模型
def use_model(model,data: str,store,user_id)->str:
    runable_with_history = RunnableWithMessageHistory(
        model,
        get_session_history
    )
    runable_with_history.config.update({"session_id":user_id})
    print (runable_with_history.config.get("session_id"))

    res= runable_with_history.invoke({"input":data})
    return hide_think(res)



#数据预处理
def preprocess(data)->str:
    result=""
    for value in data:
        if value["type"]=="text":
            result+=value["data"]['text']
    return result

def getlen(history):
    print(history.messages)
    return len(history.messages)



#对外提供的接口
def use_model_interface(input,user_id)->str:
    config = get_config()
    # 获取当前情景
    current_scenario = scenario_store.get(user_id, config["default_scenario"])
    data = preprocess(input)
    print(data)
    # 处理情景切换命令
    if data.startswith(" /情景"):
        new_scenario = data.split()[-1]
        print(new_scenario)
        if new_scenario in config["scenarios"]:
            scenario_store[user_id] = new_scenario
            if user_id in store:
                store[user_id].clear()  # 切换情景时清空历史
            return f"已切换到{new_scenario}模式"
        else:
            return "未知的情景模式"
    


    if user_id in store:
        if getlen(store[user_id])>20:
            store[user_id].clear()
            return "对话太长了，请重新开始"
    config = get_config()
    
    model = init_model(model=config["model"],scenarios=config["scenarios"],temperature=config["temperature"],scenario_name=current_scenario)
    return use_model(model,data,store,user_id)


