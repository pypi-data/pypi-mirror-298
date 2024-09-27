from openagi.planner.task_decomposer import TaskPlanner
from openagi.actions.tools.ddg_search import DuckDuckGoSearch
from openagi.actions.tools.tavilyqasearch import TavilyWebSearchQA
from openagi.agent import Admin
from openagi.actions.tools.serper_search import SerperSearch
from openagi.actions.tools.exasearch import ExaSearch
from openagi.actions.tools.serp_search import GoogleSerpAPISearch
from openagi.llms.gemini import GeminiModel
from openagi.worker import Worker

import os
os.environ['GOOGLE_API_KEY'] = ""
os.environ['Gemini_MODEL'] = "gemini-1.5-flash"
os.environ['Gemini_TEMP'] = "0.7"

gemini_config = GeminiModel.load_from_env_config()
llm = GeminiModel(config=gemini_config)

plan = TaskPlanner(autonomous=False,human_intervene=False)

#SerperSearch.set_config({"api_key":""})
#TavilyWebSearchQA.set_config({"api_key": "tvly-"})
#ExaSearch.set_config({"api_key":"---"})
#GoogleSerpAPISearch.set_config({"api_key":""})

cricket_worker = Worker(
    role = "Cricket Analyst and Finder",
    instructions = "You need to analyse the user query and gather the information on what is required. You only trust on the source you get",
    actions = [TavilyWebSearchQA]    
)

admin = Admin(
    actions = [TavilyWebSearchQA],
    planner = plan,
    llm = llm,
)
admin.assign_workers([cricket_worker])

res = admin.run(
    query="how many runs did Rohit sharma scored in 3rd ODI match against Sri Lanka during Sri Lanka tour 2024",
    description=f"give me the results of Rohit sharma scores during India vs Sri Lanka ODI 2024 series",
)
print(res)