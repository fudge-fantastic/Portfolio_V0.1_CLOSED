import os
import dotenv
import pandas as pd
from groq import Groq

dotenv.load_dotenv()
api_key_llama = os.getenv("GROQ_API_KEY")
if not api_key_llama:
    raise ValueError("GROQ_API_KEY environment variable not set")

def get_llama_assistance_qb(prompt, formatted_metadata, table_name):
    main_purpose = f"""
    As an SQL Query Expert, your primary role is to understand the given data, answer the questions based on the provided input and generate accurate SQL queries ONLY. 
    Remember, you only have to answer the Query for the given input, don't give any explanation, just the query. 
    Here are the column names with respect to their information: 
    {formatted_metadata}
    The table name is {table_name}
    Here is/are the Questions:"""

    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "user",
                "content": f"{main_purpose} {prompt}"
            },
            {
                "role": "assistant",
                "content": ""
            }
        ],
        temperature=1.4,
        max_tokens=8192,
        top_p=1,
        stream=True,
        stop=None,
    )

    response_text = ""
    for chunk in completion:
        response_text += chunk.choices[0].delta.content or ""
    
    # Remove backticks from the response
    cleaned_response = response_text.replace("```", "").strip()
    
    return cleaned_response