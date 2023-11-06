# import io

import gradio as gr
import pandas as pd

from dataloader import DataLoader
from filter_agent import filter_agent


# Modify the load_df functions to update the global variable
def load_df(df_name):
    dl = DataLoader("Formula1.sqlite")

    if df_name == "drivers":
        return dl.load_data("drivers")
    elif df_name == "stats":
        return dl.load_data("stats")
    # elif df_name == "races":  TODO: fix data formatting issues with this table
    #     return dl.load_data("races")
    elif df_name == "constructors":
        return dl.load_data("constructors")


def execute_query(sql_query):
    dl = DataLoader("Formula1.sqlite")
    df = dl.filter_table(sql_query)
    return df


# Function to convert natural language to SQL and execute the query
def filter(table_name, nl_query):
    result = filter_agent(table_name, nl_query)

    try:
        output, kwargs = result
        df = pd.DataFrame(output)
        return df, kwargs["sql_query"]
    except ValueError:
        raise gr.Error(result)


# Create the Gradio interface
with gr.Blocks() as demo:
    with gr.Group():
        with gr.Accordion(label="Generate Query", open=True) as accordion1:
            df_name_input = gr.Radio(
                choices=["drivers", "stats", "constructors"],
                label="Select table",
                info="Select a table to view",
            )
            filter_query = gr.Textbox(
                label="Filter",
                info="Enter a natural language query to filter the table",
            )
            filter_button = gr.Button(value="Filter Table", variant="primary")

        with gr.Accordion(label="Review/Edit Query", open=False) as accordion2:
            edit_sql = gr.Textbox(
                label="SQL",
                info="Review and/or edit the SQL query to filter the table",
                interactive=True,
            )
            edit_query_button = gr.Button(value="Modify Query", variant="primary")
            reset_button = gr.ClearButton(components=[filter_query, edit_sql], value="Reset")

    with gr.Row():
        df_display = gr.Dataframe()

    # Set the button click event
    df_name_input.change(fn=load_df, inputs=df_name_input, outputs=df_display)

    filter_button.click(
        lambda table_name, query: [accordion1.update(open=False), accordion2.update(open=True), *filter(table_name, query)],
        inputs=[df_name_input, filter_query],
        outputs=[accordion1, accordion2, df_display, edit_sql],
        
    )
    edit_query_button.click(
        fn=execute_query,
        inputs=edit_sql,
        outputs=df_display
    )
    reset_button.click(
        lambda df_name: [accordion1.update(open=True), accordion2.update(open=False), load_df(df_name)],
        inputs=df_name_input,
        outputs=[accordion1, accordion2, df_display]
    )
        


# Launch the interface
demo.launch(share=False)
