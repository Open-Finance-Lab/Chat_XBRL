import os
import yaml
import gradio as gr
import pandas as pd

# ---- Model Class ---- #
class Model:
    def __init__(self, model_data):
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

# ---- Load and Process YAML Models ---- #
def load_all_models(directory):
    """
    Load all models from the specified directory.
    Each model is expected to have a .yml file.
    """
    models_data = []

    for filename in os.listdir(directory):
        if filename.endswith(".yml"):
            filepath = os.path.join(directory, filename)
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

    return pd.DataFrame(models_data)

# ---- Scraper Placeholder ---- #
def scrape_model_data():
    """
    Scrapes model data from the web.
    Replace this with your actual scraper implementation.
    """
    # Example structure of scraped data
    scraped_data = [
        {"Name": "Scraped Model 1", "Organization": "Org A", "Classification": "Open", "Last Updated": "2024-11-01", "Badge": "Gold"},
        {"Name": "Scraped Model 2", "Organization": "Org B", "Classification": "Restricted", "Last Updated": "2024-11-02", "Badge": "Silver"}
    ]
    return pd.DataFrame(scraped_data)

# ---- Combine YAML and Scraped Data ---- #
def get_combined_data(directory):
    """
    Combine local YAML data with scraped data.
    """
    yaml_data = load_all_models(directory)
    scraped_data = scrape_model_data()
    return pd.concat([yaml_data, scraped_data], ignore_index=True)

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
directory = "./models"
global_df = get_combined_data(directory)

def update_table(name_query, org_query, page_size, page_number):
    """
    Update the table based on search queries and pagination.
    """
    filtered_df = filter_data(name_query, org_query)
    page_size = int(page_size)
    page_number = int(page_number)
    page_data, total_pages = paginate_data(filtered_df, page_size, page_number)
    return page_data, total_pages

def refresh_data():
    """
    Refresh the global data by reloading YAML and scraping new data.
    Resets the table to the first page.
    """
    global global_df
    global_df = get_combined_data(directory)
    page_data, total_pages = paginate_data(global_df, page_size=50, page_number=1)
    return page_data, total_pages, 1  # Reset to page 1

# Define the Gradio interface using Blocks
with gr.Blocks() as demo:
    gr.Markdown("""
    # Model Openness Framework (MOF)
    A tool for evaluating and classifying machine learning models.
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
            refresh_button = gr.Button("🔄 Refresh Data")
            page_numbers = gr.State(value=1)  # Keep track of the current page
            total_pages_text = gr.Markdown(value=f"Page 1 of {initial_total_pages}")
            go_to_input = gr.Number(label="Go to Page", value=1, precision=0)
            go_to_button = gr.Button("Go")

    # Event Handlers
    def on_search_change(name_query, org_query):
        page_data, total_pages = update_table(name_query, org_query, page_size=50, page_number=1)
        return page_data, total_pages, 1

    def on_prev(name_query, org_query, page_size, current_page):
        new_page = max(1, current_page - 1)
        page_data, total_pages = update_table(name_query, org_query, page_size, new_page)
        return page_data, total_pages, new_page

    def on_next(name_query, org_query, page_size, current_page):
        new_page = current_page + 1
        page_data, total_pages = update_table(name_query, org_query, page_size, new_page)
        return page_data, total_pages, new_page

    def on_go(name_query, org_query, page_size, go_to_page_number):
        page_data, total_pages = update_table(name_query, org_query, page_size, int(go_to_page_number))
        return page_data, total_pages, int(go_to_page_number)

    # Link Buttons to Functions
    name_query.change(on_search_change, inputs=[name_query, org_query], outputs=[table_output, total_pages_text, page_numbers])
    org_query.change(on_search_change, inputs=[name_query, org_query], outputs=[table_output, total_pages_text, page_numbers])
    prev_button.click(on_prev, inputs=[name_query, org_query, gr.State(value=50), page_numbers], outputs=[table_output, total_pages_text, page_numbers])
    next_button.click(on_next, inputs=[name_query, org_query, gr.State(value=50), page_numbers], outputs=[table_output, total_pages_text, page_numbers])
    go_to_button.click(on_go, inputs=[name_query, org_query, gr.State(value=50), go_to_input], outputs=[table_output, total_pages_text, page_numbers])
    refresh_button.click(refresh_data, outputs=[table_output, total_pages_text, page_numbers])

# Launch the Gradio app
demo.launch()
