'''
tavily-python 是一个强大的AI搜索API客户端
https://www.tavily.com/在官网注册一个api
写一个提示词模板
'''
from dotenv import load_dotenv
from matplotlib.style.core import available
from tavily import TavilyClient
import  requests
import  os
from  pprint import pprint
AGENT_SYSTEM_PROMPT='''
你是一个智能旅行助手。你的任务是分析用户的请求，并使用可用工具一步步地解决问题。
# 可用工具:
- `get_weather(city: str)`: 查询指定城市的实时天气。
- `get_attraction(city: str, weather: str)`: 根据城市和天气搜索推荐的旅游景点。

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

#定义一个天气查询工具
def get_weather(city : str) -> str :
    '''
    通过调用和风天气api查询真实的天气信息
    '''

    """
        使用Bocha Web Search API 进行网页搜索。

        参数:
        - query: 搜索关键词
        - freshness: 搜索的时间范围
        - summary: 是否显示文本摘要
        - count: 返回的搜索结果数量

        返回:
        - 搜索结果的详细信息，包括网页标题、网页URL、网页摘要、网站名称、网站Icon、网页发布时间等。
    """
    load_dotenv()# 加载.env文件
    API_KEY=os.getenv("hftq_apikey")
    API_HOST=os.getenv("hftq_apihost")
    #获取城市所需要的locationID
    url=f"https://{API_HOST}/geo/v2/city/lookup?location={city}&key={API_KEY}"
    response=requests.get(url)#响应的是状态码200
    data=response.json()
    # data=json.dumps(response.json())
    locationID=data["location"][0]["id"]
    url2=f"https://{API_HOST}/v7/weather/now?location={locationID}&key={API_KEY}"
    response = requests.get(url2)
    data2 = response.json()
    now_time=data2["updateTime"]
    temprature=data2["now"]["temp"]
    print("城市：{}\n温度：{}\n时间：{}\n".format(city,temprature,now_time))
    return temprature

#定义一个搜索并推荐的旅游景点工具
def  search_attraction(city: str,weather: str) ->str :
    """
    根据城市和天气，使用tavily搜索并返回优化后的景点推荐。
    这里的话不建议手写，因为这些东西都是有模板的，调api有相应的模板，但是我们可以把这些a用到的pi构建
知识库，以后ai直接可以写，省去麻烦
    pip install --upgrade appbuilder-sdk
    """
    T_API=os.getenv("tavily_api")
    client = TavilyClient(T_API)
    response = client.search(
        query=f"根据{weather},推荐{city}最值得去的旅游景点和理由 ",
        search_depth="basic",
        include_answer=True
    )
    # pprint(response)
    print(response["answer"])

"""
工具在这里定义了两个，把所有工具放入字典，方便后续调用
"""

available_tools={
    "get_weather":get_weather,
    "search_attraction":search_attraction
}

"""
使用api调用大语言模型
"""
#
# #传入参数调试
# city="杭州"
# weather=get_weather(city)
# search_attraction(city,weather)
