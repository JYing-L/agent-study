#工具管理和执行的逻辑逻辑
import os

from dotenv import load_dotenv
from tavily import TavilyClient
from typing import Dict,Any

load_dotenv()

def search(message: str) -> str:
    """这是一个基于实战网页的搜索引擎，根据以上的回复进行优化回答"""
    T_API = os.getenv("tavily_api")
    client = TavilyClient(T_API)
    response = client.search(
        query=message,
        search_depth="basic",
        include_answer=True,
    )
    print(response["answer"])
    return response["answer"]

class ToolExecutor :
    """
    一个工具执行器，负责管理和执行工具。
    """
    def __init__(self):
        self.tools :Dict[str,Dict[str,Any]]={}

    def registerTool(self,name:str,description:str,func:callable) :
        """
        向工具箱中注册一个新工具。
        """
        if name in self.tools :
            print(f"警告：工具 '{name}' 已存在，将被覆盖。")

        self.tools[name] = {"description": description, "func": func}
        print(f"工具 '{name}' 已注册。")

    def getTool(self,name:str) ->callable :
        """
        根据名称获取一个工具的执行函数。
        """
        return self.tools.get(name,{}).get("func")

    def getAvailableTools(self) -> str :
        """
        获取所有可用工具的格式化描述字符串。
        """
        return "\n".join([
            f"- {name}: {info['description']}"
            for name, info in self.tools.items()
        ])

# --- 工具初始化与使用示例 ---
if __name__== "__main__" :
    # 1. 初始化工具执行器
    toolExecutor= ToolExecutor()
    # 2. 注册我们的实战搜索工具
    search_description= "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
    toolExecutor.registerTool("search",search_description,search)
    # 3. 打印可用的工具
    print("\n--- 可用的工具 ---")
    print(toolExecutor.getAvailableTools())
    # 4. 智能体的Action调用，这次我们问一个实时性的问题
    print("\n--- 执行 Action: Search['武功山徒步需要准备什么，包含路线图'] ---")
    tool_name = "search"
    query="武功山徒步需要准备什么，包含路线图"

    tool_function=toolExecutor.getTool(tool_name)
    if tool_function:
        observation = tool_function(query)
        print("--- 观察 (Observation) ---")
        print(observation)
    else:
        print(f"错误：未找到名为 '{tool_name}' 的工具。")