import gradio as gr


def load_df():
    # accordion1.update(open=True)
    # accordion2.update(open=False)
    print("load_df")

def filter(i):
    # accordion1.update(open=False)
    # accordion2.update(open=True)
    print(f"filter {i}")


with gr.Blocks() as demo:
    with gr.Group():
        with gr.Accordion(label="Input", open=True) as accordion1:
            df_name_input = gr.Radio(
                choices=["drivers", "constructors"],
                label="Select table",
                info="Select a table to view",
            )
            filter_query = gr.Textbox(
                label="Filter",
                info="Enter a natural language query to filter the table",
            )
            filter_button = gr.Button(value="Run", variant="primary")

        with gr.Accordion(label="Output", open=False) as accordion2:
            edit_sql = gr.Textbox(
                label="SQL",
                info="Edit the SQL query to filter the table",
            )
            reset_button = gr.Button(value="Reset")

    # Set the button click event
    filter_button.click(
    lambda query: [accordion1.update(open=False), accordion2.update(open=True), filter(query)],
    inputs=filter_query,
    outputs=[accordion1, accordion2]
)
    reset_button.click(
        lambda: [accordion1.update(open=True), accordion2.update(open=False), load_df()],
        inputs=None,
        outputs=[accordion1, accordion2]
    )

demo.launch()


