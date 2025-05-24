from langchain.agents import Tool
from tools.qa_tool import QATool
from tools.search_tool import SearchTool
from tools.weather_tool import WeatherTool
from tools.life_expectancy import LifeExpectancyTool

def get_tools(retriever):
    qa_tool = QATool(retriever)
    search_tool = SearchTool()
    weather_tool = WeatherTool()
    life_tool = LifeExpectancyTool()

    return [
        Tool(
            name="DocumentQA",
            func=lambda q: qa_tool.ask(q)["answer"],
            description="Answer questions based on internal company documents. If unsure, say 'I don't know'."
        ),
        Tool(
            name="WebSearch",
            func=search_tool.search,
            description="Use only if DocumentQA is unsure or says 'I don't know'. Good for general or recent information."
        ),
        Tool(
            name="WeatherFood",
            func=weather_tool.get_weather,
            description="Suggest food based on the weather in a city. Input should be a city name."
        ),
        Tool(
            name="LifeExpectancyEstimator",
            func=lambda _: life_tool.ask_questions(),
            description="Estimates remaining life expectancy based on fixed lifestyle questions."
        )
    ]
