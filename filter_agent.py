from dataloader import DataLoader
from openai_functions import filter_table_meta
from chat import Chat


# Base system prompt for the filter agent
base_system_message  = """You are a specialized agent designed exclusively to generate a SQL query in order to \
filter an SQLite database table based on relevant user input.
You will avoid engaging in general conversation or responding to inputs unrelated to the given database table. 
A valid question is one that can be answered by the table you have access to. \
If the user's question is valid, use the `filter_table` function to return a filtered table. \
If the question is invalid (irrelevant), reject it and provide a short error message.
"""

# Used to insert specific instructions for a table into the system message
special_instructions_stats = """
Special Instructions:
- A driver is considered to have won a race if positionOrder = 1
- "Best" or "Top" refers to the driver with the most wins (i.e. COUNT of positionOrder = 1)
"""


def filter_agent(table_name, query) -> str:
    dl = DataLoader("Formula1.sqlite")
    system_message = base_system_message

    if table_name == "stats":
        system_message += special_instructions_stats

    filter_agent_meta = {
        "messages": [
            {
                "role": "system",
                "content": system_message +
                           f"\nTable name: {table_name}\nSchema:\n{dl.get_schema(table_name)}\n"
                           f"Sample data:\n{dl.get_sample_data(table_name)}",
            }
        ],
        "functions": [(filter_table_meta, dl.filter_table)],
    }
    # print(filter_agent_meta["messages"][0]["content"])
    # return filter_agent_meta["messages"][0]

    agent = Chat(agent=filter_agent_meta)
    result = agent.predict(query)

    if isinstance(result, tuple):
        output, kwargs = result
        return output, kwargs
    else:
        return result["content"]


# filter_agent("stats", "Show me the best driver?")
