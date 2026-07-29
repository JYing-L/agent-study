#此模块用于封装llm，方便其他抹开进行调用

import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()

class openai_LLM:
    """
    本项目的通用llm客户端
    """
    def __init__(self,model: str,api_key:str,base_url:str,timeout:int) :
        """
        初始化客户端
        其中self的作用为调用之后自动生成相关属性
        :param model:
        :param apikey:
        :param baseUrl:
        :param timeout:
        """
        self.model = model
        self.client = OpenAI(api_key=api_key, base_url=base_url,timeout=timeout)
        error_param= []
        if not model :
            error_param.append(model)
        if not api_key :
            error_param.append(api_key)
        if not base_url :
            error_param.append(base_url)

        if error_param :
            raise ValueError(f"以下参数错误：{','.join(error_param)}。请检查.env文件是否完整")

    def think(self,messages: List[Dict[str,str]],temperature:float =0) -> str :

        """
        调用大语言模型进行思考，并返回其响应。
        """
        print(f"🧠 正在调用 {self.model} 模型...")

        try :
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=True,
            )
            # 处理流式响应
            print("✅ 大语言模型响应成功:")
            collected_content=[]
            for chunk in response:
                if not chunk.choices:
                    continue
                content = chunk.choices[0].delta.content or ""
                print(content, end="", flush=True)
                collected_content.append(content)
            print()  # 在流式输出结束后换行
        except Exception as e:
            print(f"❌ 调用LLM API时发生错误: {e}")
            return None


# --- 客户端使用示例 ---
if __name__ == '__main__':
    model = os.getenv("MODEL_ID")
    api_key = os.getenv("Qwen_API_KEY")
    base_url = os.getenv("Qwen_BASE_URL")
    try:
        llmClient = openai_LLM(model,api_key,base_url,1)

        exampleMessages = [
            {"role": "system", "content": "You are a helpful assistant that writes Python code."
                                          ""},
            {"role": "user", "content": "写一个快速排序算法"}
        ]

        print("--- 调用LLM ---")
        responseText = llmClient.think(exampleMessages)
        if responseText:
            print("\n\n--- 完整模型响应 ---")
            print(responseText)

    except ValueError as e:
        print(e)


#并没什么卵用，其实用人家原生的就行封装得也麻烦，并没什么用。