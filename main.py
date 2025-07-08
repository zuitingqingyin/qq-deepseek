import uvicorn
from fastapi import FastAPI, Request
import ollama
import json
import use_model
import requests

app = FastAPI()


#调用模型后回复消息
def reply_message(message,group_id,user_id):
    res = requests.post('http://localhost:3000/send_group_msg',json={
        "group_id": group_id,
        "message":[
            
                {
                    "type":"at",
                    "data":{"qq": user_id}
                },
                {
                    "type":"text",
                    "data": {"text": message}
                }

            
            ]
        }
    )
    print(res.content)


@app.post("/")
async def root(request: Request):
    data = await request.json() # 获取请求体中的数据
    user_id = data['user_id']
    group_id = data['group_id']
    self_id = data['self_id']
    for value in data['message']:
        print(value)
        if value['type']=='at':
            print(value['data']['qq'])
            if value['data']['qq']==str(self_id):
                print("收到艾特我的消息,开始处理")
                
                output = use_model.use_model_interface(data['message'],user_id)
                print(output)
                reply_message(output,group_id,user_id)
                break

    return {}

if __name__ == "__main__":
    uvicorn.run(app,port=8080)




