
import json
import langchain
import langchain_community
from langchain_ollama import OllamaLLM as Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage, AIMessage
import re

# 获取配置
def get_config()->dict:
    with open("config.json",'r',encoding='utf-8') as f:
        config=json.loads(f.read())
    return config


# 隐藏思考的过程
def hide_think(response)->str:
    response=re.sub(r"<think>\n.*\n</think>","",response,flags=re.DOTALL)
    return response

# 使用模型
def use_model(host,port,model,prompt,data,temperature)->str:
     
    messages = [
        SystemMessage(content=prompt),
        HumanMessage(content=data)
    ]
    llm = Ollama(base_url=f"http://{host}:{port}",model=model)
    output_parser=StrOutputParser()
    prompttemplate = ChatPromptTemplate(
		messages=messages
	)

    r = prompttemplate|llm|output_parser

    res = r.invoke({"input":""},temperature=temperature)
	
    return hide_think(res)


#数据预处理
def preprocess(data)->str:
    result=""
    for value in data:
        if value["type"]=="text":
            result+=value["data"]['text']
    return result



#对外提供的接口
def use_model_interface(input)->str:
    config = get_config()
    data = preprocess(input)
    return use_model(**config,data=data)


