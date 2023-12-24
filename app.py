import streamlit as st
import requests

key = st.secrets.HF_KEY

# Set the title and heading
st.title("Check if the text is AI generated")
st.header("Enter text and select the model")

# Input text box for user input
user_text = st.text_area("Enter your text here:")

# Dropdown menu for model selection
model_option = st.selectbox("Select AI Model:", ["BERT", "DistilBERT", "RoBERTa", "DeBERTa", "MPNet"])

# Create a function to check if your text is AI-generated

def is_ai_generated(text, model):
    model_dict = {"BERT":"bert-classification-10ksamples", 
                  "DistilBERT":"distilbert-classification-10ksamples",
                  "DeBERTa": "deberta-classification-10ksamples",
                  "RoBERTa": "roberta-classification-10ksamples",
                  "MPNet": "mpnet-classification-10ksamples"}
    model_name = model_dict[model]
    API_URL = "https://api-inference.huggingface.co/models/jayavibhav/{}".format(model_name)
    headers = {"Authorization": "Bearer {}".format(key)}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
        
    output = query({
        "inputs": text[:2048],
    })
    not_ai = output[0][1]['score'] if output[0][1]['label'] == 'NEGATIVE' else output[0][0]['score']
    yes_ai = output[0][0]['score'] if output[0][0]['label'] == 'POSITIVE' else output[0][1]['score']

    if yes_ai>not_ai:
        return True, yes_ai
    else:
        return False, yes_ai

# Check if the text is AI-generated when the user clicks the button
if st.button("Check"):
    if user_text:
        result, ai = is_ai_generated(user_text, model_option)
        if result:
            st.error("This text is AI-generated, AI percentage " + str(ai))
        else:
            st.success("This text is not AI-generated, AI percentage " + str(ai))
    else:
        st.warning("Please enter some text to check.")

# Optionally, you can add a description or instructions
st.markdown("### Instructions:")
st.write("1. Enter text in the input box.")
st.write("2. Select an AI model from the dropdown menu.")
st.write("3. Click the 'Check' button to determine if the text is AI-generated.")


st.write("\n")

st.write('\n')

st.write('Created by Jayavibhav N K')
