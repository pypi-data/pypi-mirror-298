import pandas as pd
from tqdm import tqdm
import time
from datetime import datetime
import json
from models import initialize_model

def get_category_and_subcategory(text):
    try:
        ollama_model = initialize_model('llama3_1_T0_00.json', 'IT_Categorizer.txt')
        response = ollama_model(text)
        data = json.loads(response)
        category = data.get('category', None)
        subcategory = data.get('subcategory', None)
        return pd.Series({'ai_category': category, 'ai_subcategory': subcategory})
    except Exception as e:
        print(f"Error processing text: {text}\nException: {e}")
        return pd.Series({'ai_category': None, 'ai_subcategory': None})

def process_dataframe(df, text_column_name, ollama_model):
    tqdm.pandas()
    start_time = time.time()
    
    # Apply the function with progress bar
    df[['ai_category', 'ai_subcategory']] = df[text_column_name].progress_apply(
        lambda text: get_category_and_subcategory(ollama_model, text)
    )
    
    end_time = time.time()
    formatted_start_time = datetime.fromtimestamp(start_time).strftime('%H:%M:%S')
    formatted_end_time = datetime.fromtimestamp(end_time).strftime('%H:%M:%S')
    print(f"Start time: {formatted_start_time}")
    print(f"End time: {formatted_end_time}")
    return df