
import json
import langchain
import langchain_community
from langchain_ollama import OllamaLLM as Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage, AIMessage
import re
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory


store = {} #对话记忆，根据user_id来区分不同的对话

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
def init_model(host,port,model,prompt,temperature):
     
    messages: dict = [
        {"role":"system","content":prompt},
        {"role":"user","content":"{input}"}
    ]



    llm = Ollama(base_url=f"http://{host}:{port}",model=model,temperature=temperature)
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



#对外提供的接口
def use_model_interface(input,user_id)->str:
    if user_id in store:
        if store[user_id]._len_()>20:
            store[user_id].clear()
            return "对话太长了，请重新开始"
    config = get_config()
    data = preprocess(input)
    model = init_model(**config)
    return use_model(model,data,store,user_id)


