from openagi.actions.tools.ddg_search import DuckDuckGoSearch

response = DuckDuckGoSearch.execute("Tarun Jain",max_results=10)
print(response)