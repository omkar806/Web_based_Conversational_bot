
import streamlit as st
import requests

st.title("LLM-based RAG Search")

# Input for user query
query = st.text_input("Enter your query:")

if st.button("Search"):
    # Make a POST request to the Flask API
    with st.spinner("Searching and generating response..."):
        print("accessing ", "<Flask app string>", " with query ", query)
        api_url = "http://127.0.0.1:5000/query"
        response = requests.post(api_url, json={"query": query})

        # implement the flask call here
        
        if response.status_code == 200:
            # Display the generated answer
            answer = response.json().get('answer', "No answer received.")
            st.write("Answer:", answer)
        else:
            st.error(f"Error: {response.status_code}")
