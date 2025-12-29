import streamlit as st
from tavily import TavilyClient
import google.generativeai as genai
import re

from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API = os.getenv('GEMINI_API')
TAVILY_API = os.getenv('TAVILY_API')
genai.configure(api_key=GEMINI_API)
tavily = TavilyClient(api_key=TAVILY_API)

st.title("Real-Time AI Chat")

query = st.text_input("Enter your query")

# AI Model for generating content
model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction="You are a helpful assistant. For any given query, provide a brief and summary of the topic and include relevant YouTube links for learning more about it. Ensure the YouTube links are educational and appropriate for the topic.")
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search(query):
    response = tavily.search(
        query=query,
        search_depth="basic",
        include_domains=["youtube.com"],
        max_results=5
    )

    content = ""
    for item in response.get("results", []):
        content += item.get("content", "") + "\n"

    return content
def extract_youtube_links(text):
    # Regular expression to find YouTube video IDs
    youtube_regex = r'(?:https?://(?:www\.)?youtube\.com/watch\?v=|https?://youtu\.be/)([\w-]+)'
    video_ids = re.findall(youtube_regex, text)
    # Remove duplicates by converting to a set and back to list
    video_ids = list(set(video_ids))
    youtube_links = [f"https://www.youtube.com/watch?v={video_id}" for video_id in video_ids]
    return youtube_links

if st.button("Submit"):
    # Search and get response
    response = search(query)
    
    # Generate content using AI
    answer = model.generate_content(response)
    st.markdown(answer.text)
    
    # Extract and display YouTube links
    youtube_links = extract_youtube_links(answer.text)
    
    if youtube_links:
        st.subheader("YouTube Links:")
        for link in youtube_links:
            st.video(link)
    else:
        st.warning("No YouTube links found in the response.")
    
    # Display results from Google and Wikipedia
    st.subheader("Search Results:")
    
    # Display results for Google and Wikipedia
    if 'google.com' in response:
        st.write("Google Search Results:")
        # Extract Google search results
        google_results = re.findall(r'(https?://(?:www\.)?google\.com[^"]+)', response)
        for result in google_results:
            st.write(f"[Google Result]({result})")
    
    if 'wikipedia.org' in response:
        st.write("Wikipedia Search Results:")
        # Extract Wikipedia search results
        wikipedia_results = re.findall(r'(https?://(?:www\.)?wikipedia\.org[^"]+)', response)
        for result in wikipedia_results:
            st.write(f"[Wikipedia Result]({result})")

