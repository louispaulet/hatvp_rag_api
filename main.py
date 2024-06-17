from flask import Flask, request, jsonify
import os
import json
import numpy as np
from datasets import load_dataset
from openai import OpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import tiktoken
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

# Load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)
embed_ds = load_dataset("the-french-artist/hatvp_declarations_text_index_embeds", split='train')
embed_ds.add_faiss_index(column='text_index_embedding')

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def truncate_text_to_stay_under_openai_embedding_limit(input_text):
    backup_input_text = input_text
    openai_embed_limit = 8192
    delta = num_tokens_from_string(input_text, "cl100k_base") - openai_embed_limit
    while delta > 0:
        input_text = input_text[:-int(delta*2)]  # Speed up the process with factor 2
        delta = num_tokens_from_string(input_text, "cl100k_base") - openai_embed_limit
    return input_text if len(input_text) > 0 else backup_input_text[:8000]

def get_embedding(text, model="text-embedding-3-large"):
    text = text.replace("\n", " ")
    text = truncate_text_to_stay_under_openai_embedding_limit(text)
    return client.embeddings.create(input=[text], model=model).data[0].embedding

def perform_query(query, n_samples=1):
    query_embed = np.array(get_embedding(query.lower()))
    scores, retrieved_examples = embed_ds.get_nearest_examples('text_index_embedding', query_embed, k=n_samples)
    return retrieved_examples['declaration_json']

def get_name_surname_from_str_declaration(input_str_json):
    parsed_json = json.loads(input_str_json)
    return parsed_json['declaration']['general']['declarant']['nom'], parsed_json['declaration']['general']['declarant']['prenom']

def get_answer_to_question(question, llm_to_use):
    system = """You are an assistant for question-answering tasks.
    Use the following pieces of retrieved context to answer the question.
    If you don't know the answer, just say that you don't know.
    Use three sentences maximum and keep the answer concise.
    """
    human = "{text}"
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])
    
    results = perform_query(question, 1)
    context = ''.join(results)  # Concatenate top results into a context
    actual_prompt = f"""
    Question: {question}
    Context: {context}
    Answer:
    """
    
    chain = prompt | llm_to_use | StrOutputParser()
    return chain.invoke({"text": actual_prompt})

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.json
    question = data.get('question')
    llm_llama3_70B = ChatGroq(temperature=0, model_name="llama3-70b-8192")
    answer = get_answer_to_question(question, llm_llama3_70B)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
