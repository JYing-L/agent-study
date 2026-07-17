"""
tavily-python 是一个强大的AI搜索API客户端
https://www.tavily.com/ 在官网注册一个API
写一个提示词模板
"""
import os
import requests
from dotenv import load_dotenv
from tavily import TavilyClient

# 加载环境变量（只需加载一次）
load_dotenv()

AGENT_SYSTEM_PROMPT = '''
你是一个智能旅行助手。你的任务是分析用户的请求，并使用可用工具一步步地解决问题。

# 可用工具:
- `get_weather(city: str)`: 查询指定城市的实时天气。
- `search_attraction(city: str, weather: str)`: 根据城市和天气搜索推荐的旅游景点。

# 输出格式要求:
你的每次回复必须严格遵循以下格式，包含一对Thought和Action：

Thought: [你的思考过程和下一步计划]
Action: [你要执行的具体行动]

Action的格式必须是以下之一：
1. 调用工具：function_name(arg_name="arg_value")
2. 结束任务：Finish[最终答案]

# 重要提示:
- 每次只输出一对Thought-Action
- Action必须在同一行，不要换行
- 当收集到足够信息可以回答用户问题时，必须使用 Action: Finish[最终答案] 格式结束

请开始吧！
'''


def get_weather(city: str) -> str:
    """通过调用和风天气API查询真实的天气信息"""

    API_KEY = os.getenv("hftq_apikey")
    API_HOST = os.getenv("hftq_apihost")

    # 获取城市对应的 locationID
    url = f"https://{API_HOST}/geo/v2/city/lookup?location={city}&key={API_KEY}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    if not data.get("location"):
        raise ValueError(f"未找到城市: {city}")
    location_id = data["location"][0]["id"]

    # 获取实时天气
    url2 = f"https://{API_HOST}/v7/weather/now?location={location_id}&key={API_KEY}"
    response = requests.get(url2)
    response.raise_for_status()
    data2 = response.json()

    update_time = data2["updateTime"]
    temperature = data2["now"]["temp"]
    print(f"城市：{city}\n温度：{temperature}\n时间：{update_time}")
    return temperature


def search_attraction(city: str, weather: str) -> str:
    """根据城市和天气，使用tavily搜索并返回优化后的景点推荐"""

    T_API = os.getenv("tavily_api")
    client = TavilyClient(T_API)
    response = client.search(
        query=f"根据{weather}天气，推荐{city}最值得去的旅游景点和理由",
        search_depth="basic",
        include_answer=True,
    )
    print(response["answer"])
    return response["answer"]


# 把所有工具放入字典，方便后续 LLM Agent 调用
available_tools = {
    "get_weather": get_weather,
    "search_attraction": search_attraction,
}


# ─── LLM Agent 主循环 ────────────────────────────────────────
# TODO: 接入大模型，将 AGENT_SYSTEM_PROMPT + 用户输入传入，
# 解析 Thought / Action，循环执行工具调用直到 Finish
# ────────────────────────────────────────────────────────────
#
# 使用示例（伪代码）:
#
# def run_agent(user_query: str) -> str:
#     messages = [
#         {"role": "system", "content": AGENT_SYSTEM_PROMPT},
#         {"role": "user", "content": user_query},
#     ]
#     while True:
#         response = llm.chat(messages)          # 调用大模型
#         thought, action = parse(response)      # 解析 Thought / Action
#         if action.startswith("Finish"):
#             return action
#         tool_name, kwargs = parse_tool(action) # 解析工具名和参数
#         result = available_tools[tool_name](**kwargs)
#         messages.append({"role": "user", "content": f"工具返回: {result}"})
