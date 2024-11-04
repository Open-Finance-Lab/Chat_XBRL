import os
import yaml
import gradio as gr
import pandas as pd

# ---- Model Class ---- #
class Model:
    def __init__(self, model_data):
        """
        Initializes the model with the provided model_data dictionary (from YAML).
        """
        self.data = model_data

    def get_name(self):
        return self.data.get("release", {}).get("name", "Unknown")

    def get_producer(self):
        return self.data.get("release", {}).get("producer", "Unknown")

    def get_classification(self):
        return self.data.get("release", {}).get("classification", "Unclassified")

    def get_last_updated(self):
        return self.data.get("release", {}).get("date", "Unknown")

    def get_badge(self):
        return self.data.get("release", {}).get("badge", "")

# ---- Load and Process Models in a Directory ---- #
def load_all_models(directory):
    """
    Load all models from the specified directory.
    Each model is expected to have a .yml file.
    """
    models_data = []

    for filename in os.listdir(directory):
        if filename.endswith(".yml"):
            filepath = os.path.join(directory, filename)
            # Specify encoding as 'utf-8' to avoid decoding issues
            with open(filepath, 'r', encoding='utf-8') as file:
                model_data = yaml.safe_load(file)
                model = Model(model_data)

                # Append the model information to our list
                models_data.append({
                    "Name": model.get_name(),
                    "Organization": model.get_producer(),
                    "Classification": model.get_classification(),
                    "Last Updated": model.get_last_updated(),
                    "Badge": model.get_badge()
                })

    return models_data

# ---- Convert Model Data to a DataFrame ---- #
def get_model_table(directory):
    """
    Get a table of all models and their information.
    """
    models_data = load_all_models(directory)

    # Create a Pandas DataFrame for easy table generation
    df = pd.DataFrame(models_data)
    return df

# ---- Global DataFrame ---- #
# Load the data once and reuse it for filtering and pagination
directory = "./models"  # You can change this to your actual models folder path
global_df = get_model_table(directory)

# ---- Filtering and Pagination Functions ---- #
def filter_data(name_query, org_query):
    """
    Filter the global dataframe based on the search queries.
    """
    df = global_df.copy()
    if name_query:
        df = df[df['Name'].str.contains(name_query, case=False, na=False)]
    if org_query:
        df = df[df['Organization'].str.contains(org_query, case=False, na=False)]
    return df.reset_index(drop=True)

def paginate_data(df, page_size, page_number):
    """
    Paginate the filtered dataframe.
    """
    total_rows = len(df)
    total_pages = (total_rows + page_size - 1) // page_size  # Calculate total pages

    # Ensure page_number is within valid range
    if page_number < 1:
        page_number = 1
    elif page_number > total_pages:
        page_number = total_pages

    start_row = (page_number - 1) * page_size
    end_row = start_row + page_size
    page_data = df.iloc[start_row:end_row]
    return page_data, total_pages

# ---- Gradio Interface ---- #
def update_table(name_query, org_query, page_size, page_number):
    """
    Update the table based on search queries and pagination.
    """
    filtered_df = filter_data(name_query, org_query)
    page_size = int(page_size)
    page_number = int(page_number)
    page_data, total_pages = paginate_data(filtered_df, page_size, page_number)
    return page_data, total_pages

def go_to_page(name_query, org_query, page_size, go_to_page_number):
    """
    Go to a specific page number.
    """
    return update_table(name_query, org_query, page_size, go_to_page_number)

# Define the Gradio interface using Blocks
with gr.Blocks() as demo:
    # MOF Description
    gr.Markdown("""
    # Model Openness Framework (MOF)

    The Generative AI Commons at the LF AI & Data Foundation has designed and developed the **Model Openness Framework (MOF)**, a comprehensive system for evaluating and classifying the completeness and openness of machine learning models. This framework assesses which components of the model development lifecycle are publicly released and under what licenses, ensuring an objective evaluation. The framework is constantly evolving. Please participate in the Generative AI Commons to provide feedback and suggestions.

    ## Model Openness Tool (MOT)

    To implement the MOF, we’ve created the **Model Openness Tool (MOT)**. This tool evaluates each criterion from the MOF and generates a score based on how well each item is met. The MOT provides a practical, user-friendly way to apply the MOF framework to your model and produce a clear, self-service score.

    ### How It Works

    The MOT presents users with 16 questions about their model. Users need to provide detailed responses for each question. Based on these inputs, the tool calculates a score, classifying the model’s openness on a scale of 1, 2, or 3.

    ### Why We Developed MOT

    Our goal in developing the MOT was to offer a straightforward tool for evaluating machine learning models against the MOF framework. This tool helps users understand what components are included with each model and the licenses associated with those components, providing clarity on what can and cannot be done with the model and its parts.

    **Explore the Model Openness Framework and try the [Model Openness Tool](https://mot.isitopen.ai/) today to see how your models measure up.**
    """)

    # Search Filters
    with gr.Row():
        name_query = gr.Textbox(label="Search by Name")
        org_query = gr.Textbox(label="Search by Organization")

    # Table and Pagination Controls
    with gr.Column():
        # Initialize with the first page of data
        initial_page_data, initial_total_pages = paginate_data(global_df, page_size=50, page_number=1)
        table_output = gr.Dataframe(
            value=initial_page_data,
            headers=["Name", "Organization", "Classification", "Last Updated", "Badge"],
            label="Models Table"
        )

        # Pagination Controls
        with gr.Row():
            prev_button = gr.Button("← Previous")
            next_button = gr.Button("Next →")
            page_numbers = gr.State(value=1)  # Keep track of the current page
            total_pages_text = gr.Markdown(value=f"Page 1 of {initial_total_pages}")
            go_to_input = gr.Number(label="Go to Page", value=1, precision=0)
            go_to_button = gr.Button("Go")

    # Event Handlers
    def update_pagination(name_query, org_query, page_size, page_number):
        page_data, total_pages = update_table(name_query, org_query, page_size, page_number)
        total_pages_text.value = f"Page {page_number} of {total_pages}"
        return page_data, total_pages_text.value, page_number

    # When search filters change, reset to page 1
    def on_search_change(name_query, org_query):
        page_data, total_pages = update_table(name_query, org_query, page_size=50, page_number=1)
        total_pages_text.value = f"Page 1 of {total_pages}"
        return page_data, total_pages_text.value, 1

    name_query.change(
        fn=on_search_change,
        inputs=[name_query, org_query],
        outputs=[table_output, total_pages_text, page_numbers]
    )
    org_query.change(
        fn=on_search_change,
        inputs=[name_query, org_query],
        outputs=[table_output, total_pages_text, page_numbers]
    )

    # Previous Button
    def on_prev(name_query, org_query, page_size, current_page):
        new_page = max(1, current_page - 1)
        return update_pagination(name_query, org_query, page_size, new_page)

    prev_button.click(
        fn=on_prev,
        inputs=[name_query, org_query, gr.State(value=50), page_numbers],
        outputs=[table_output, total_pages_text, page_numbers]
    )

    # Next Button
    def on_next(name_query, org_query, page_size, current_page):
        new_page = current_page + 1
        return update_pagination(name_query, org_query, page_size, new_page)

    next_button.click(
        fn=on_next,
        inputs=[name_query, org_query, gr.State(value=50), page_numbers],
        outputs=[table_output, total_pages_text, page_numbers]
    )

    # Go To Page
    def on_go(name_query, org_query, page_size, go_to_page_number):
        return update_pagination(name_query, org_query, page_size, int(go_to_page_number))

    go_to_button.click(
        fn=on_go,
        inputs=[name_query, org_query, gr.State(value=50), go_to_input],
        outputs=[table_output, total_pages_text, page_numbers]
    )

# Launch the Gradio app
demo.launch()
