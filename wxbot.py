import time
start_time = time.time()
for i in range(1000000):
    _ = i ** 2
from wxauto import WeChat
import os
import openai


# 初始化微信BOT
wx = WeChat()
wx.GetSessionList()
print(wx.GetSessionList())
#存放关键词消息时间
msgs_list = []

def gpt_api(prompt):
    try:
        openai.api_key = "sk-YU06tTBOszaIy8yS34A1A66300F248FbAf52275a87984e5e"
        openai.base_url = "https://free.v36.cm/v1/"
        openai.default_headers = {"x-foo": "true"}
        response = openai.chat.completions.create(
            model="gpt-4o-mini", #或者gpt-3.5-turbo（留着备用）
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,  # 控制生成内容的随机性
        )
        response = response.choices[0].message.content.strip()
        print(f"GPT 回复: {response}")
        wx.SendMsg(at=sender,msg=response)
        print(f"已回复 {sender}: {response}")
        
    except Exception as e:
        print(f"调用GPT-API失败: {e}")
        return "抱歉，我暂时无法处理你的请求，请稍后再试。"

def start():
    end_time = time.time()
    starting_time = end_time - start_time
    print(f"Done!{starting_time}s")

if __name__ == "__main__":
    start()
    while True:
        msgs = wx.GetAllMessage()
        for msg in msgs:
            if (msg[1])[:5] == "@一二三四":
                if msg[2] not in msgs_list:
                    msgs_list.append(msg[2])
                    sender, content = msg[0], msg[1]
                    print(f"{sender}: {msg}")
                    last_msg = msg
                    if (msg[1])[6:] == "时间":  #询问时间
                        wx.SendMsg(f"@{msg[0]} 现在是{(time.asctime())[11:20]}")
                        print(f"已回复 [{sender}]: @{msg[0]} 现在是{(time.asctime())[11:20]}")
                    if (msg[1])[6:9] != "小爱 " and (msg[1])[6:12] != "生成二维码 " and (msg[1])[6:] != "pixiv" and (msg[1])[6:] != "猫咪图片" and (msg[1])[6:] != "时间" and (msg[1])[6:] != "帮助":
                        gpt_api(prompt=(msg[1])[6:])
        

