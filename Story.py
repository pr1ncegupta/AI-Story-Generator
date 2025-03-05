import streamlit as st
import google.generativeai as genai
import os
from fpdf import FPDF

# Configure Gemini API
API_KEY = st.secrets["API_KEY"]
genai.configure(api_key=API_KEY)

st.title("📖 AI Story Writer")
st.subheader("Create and expand your stories effortlessly!")

# Genre selection
genres = ["Fantasy", "Science Fiction", "Mystery", "Horror", "Romance", "Adventure", "Thriller", "Historical Fiction"]
selected_genre = st.selectbox("Choose a genre:", genres)

# Writing Style selection
styles = ["Poetic", "Suspenseful", "Humorous", "Descriptive", "Fast-Paced"]
selected_style = st.selectbox("Choose a writing style:", styles)

# Story prompt input
story_prompt = st.text_area("Enter your story prompt:", "Once upon a time...")

def generate_story(prompt, genre, style):
    model = genai.GenerativeModel("gemini-pro")
    full_prompt = f"Write a {genre} story in a {style} style: {prompt}"
    response = model.generate_content(full_prompt)
    return response.text

if "story" not in st.session_state:
    st.session_state.story = ""

if st.button("Generate Story"):
    if story_prompt.strip():
        story = generate_story(story_prompt, selected_genre, selected_style)
        st.session_state.story = story  # Store generated story
        st.write(story)
    else:
        st.warning("Please enter a story prompt!")

# Chapter builder
st.subheader("📚 Continue the Story")
if st.session_state.story:
    chapter_prompt = st.text_area("Add a new chapter:", "What happens next?")
    
    if st.button("Generate Chapter"):
        if chapter_prompt.strip():
            full_prompt = st.session_state.story + "\n\n" + chapter_prompt
            new_chapter = generate_story(full_prompt, selected_genre, selected_style)
            st.session_state.story += "\n\n" + new_chapter
            st.write(new_chapter)
        else:
            st.warning("Enter some details for the new chapter!")
else:
    st.info("Generate a story first before adding chapters.")

# AI-powered title & chapter suggestions
st.subheader("🎭 AI Title & Chapter Suggestions")
title_prompt = "Generate a captivating title for this story: " + st.session_state.story[:200]
title_response = generate_story(title_prompt, selected_genre, selected_style)
st.text_input("Suggested Story Title:", title_response)

chapter_title_prompt = "Suggest a title for this chapter: " + chapter_prompt
chapter_title_response = generate_story(chapter_title_prompt, selected_genre, selected_style)
st.text_input("Suggested Chapter Title:", chapter_title_response)

# Story summarizer
st.subheader("📌 Story Summary")
summarize_prompt = "Summarize this story briefly: " + st.session_state.story
summary_response = generate_story(summarize_prompt, selected_genre, selected_style)
st.text_area("Story Summary:", summary_response)

# Word count tracker
st.subheader("📝 Word Count Tracker")
word_count = len(st.session_state.story.split())
st.write(f"**Total Word Count:** {word_count}")

# Story editor
st.subheader("📝 Edit Your Story")
st.session_state.story = st.text_area("Edit the story:", st.session_state.story)

# Save and download options
def save_story():
    with open("story.txt", "w", encoding="utf-8") as file:
        file.write(st.session_state.story)

def download_story():
    with open("story.txt", "w", encoding="utf-8") as file:
        file.write(st.session_state.story)
    with open("story.txt", "r", encoding="utf-8") as file:
        st.download_button(label="📥 Download Story", data=file, file_name="story.txt", mime="text/plain")

if st.button("💾 Save Story"):
    save_story()
    st.success("Story saved successfully!")

download_story()

# PDF Export Feature
def save_story_as_pdf():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    for line in st.session_state.story.split("\n"):
        pdf.cell(200, 10, txt=line, ln=True, align='L')
    
    pdf.output("story.pdf")

def download_story_as_pdf():
    save_story_as_pdf()
    with open("story.pdf", "rb") as file:
        st.download_button(label="📥 Download Story as PDF", data=file, file_name="story.pdf", mime="application/pdf")

download_story_as_pdf()
