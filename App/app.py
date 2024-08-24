import streamlit as st
import requests
from bs4 import BeautifulSoup
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Set up Google Custom Search API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
SEARCH_ENGINE_ID = os.getenv('SEARCH_ENGINE_ID')
GEMINI_API_KEY=os.getenv('GEMINI_API_KEY')
# Setting up gemini API
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def google_search(query, num_results=4):
    service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
    result = service.cse().list(q=query, cx=SEARCH_ENGINE_ID, num=num_results).execute()
    return [item['link'] for item in result.get('items', [])]

def fetch_content(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.content, 'html.parser')
        return ' '.join([p.text for p in soup.find_all('p')])
    except:
        return ""

def preprocess_text(text):
    doc = nlp(text)
    return ' '.join([token.lemma_ for token in doc if not token.is_stop and token.is_alpha])

def get_top_contexts(query, texts, top_n=2):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([query] + texts)
    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    top_indices = cosine_similarities.argsort()[-top_n:][::-1]
    return [texts[i] for i in top_indices]

def generate_response(user_query, context):
    system_prompt = f"""You are a helpful assistant. Use the following context to answer the user's query. If the context doesn't contain relevant information, say so.\n
    Below is the context : \n
    {context}\n
    Below is the user query:
    {user_query}\n
    Based on the user query above and the context given provide with highly accurate response for the user query . You should be very precise about the answer based on the user query and content.
    """
    print(f"Prompt that is being passed to the LLM : \n {system_prompt}")
    response = model.generate_content(system_prompt)
    return response.text

def main():
    st.title("Web Search and AI Response Generator")

    query = st.text_input("Enter your query:")

    if st.button("Generate Response"):
        with st.spinner("Searching and generating response..."):
            # Search and fetch content
            urls = google_search(query)
            print(f"Printing the urls found ? \n {urls} \n")
            texts = [fetch_content(url) for url in urls]
            print(f"This is the content extracted from the html . \n {texts} \n")
            # Preprocess texts
            processed_texts = [preprocess_text(text) for text in texts]
            print(f"Preprocessed text : \n {processed_texts} \n")
            # Get top contexts
            top_contexts = get_top_contexts(query, processed_texts)
            print(f"Top contexts : \n {top_contexts}\n")
            # Generate response
            context = " ".join(top_contexts)
            response = generate_response(query, context)

            st.subheader("AI Response:")
            st.write(response)

if __name__ == "__main__":
    main()