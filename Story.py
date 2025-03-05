import streamlit as st
import google.generativeai as genai
import os
from fpdf import FPDF

# Configure Gemini API
API_KEY = os.getenv("Gen_API")  # Using your API name
if not API_KEY:
    st.error("API Key is missing! Set Gen_API as an environment variable.")
    st.stop()  # Stop execution if API key is missing

genai.configure(api_key=API_KEY)

st.title("📖 AI Story Writer")
st.subheader("Create and expand your stories effortlessly!")

# Genre selection
genres = ["Fantasy", "Science Fiction", "Mystery", "Horror", "Romance", "Adventure", "Thriller", "Historical Fiction"]
selected_genre = st.selectbox("Choose a genre:", genres)

# Writing style selection
styles = ["Classic", "Modern", "Poetic", "Descriptive", "Minimalistic"]
selected_style = st.selectbox("Choose a writing style:", styles)

# Story prompt input
story_prompt = st.text_area("Enter your story prompt:", "Once upon a time...")

def generate_story(prompt, genre, style):
    """Generates a story using the Gemini API (gemini-2.0-flash)."""
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")  # Using gemini-2.0-flash
        full_prompt = f"Write a {genre} story in {style} style: {prompt}"
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating story: {e}")
        return ""

if "story" not in st.session_state:
    st.session_state.story = ""

if st.button("Generate Story"):
    if story_prompt.strip():
        story = generate_story(story_prompt, selected_genre, selected_style)
        if story:
            st.session_state.story = story  # Store generated story
            st.write(story)
    else:
        st.warning("Please enter a story prompt!")

# Chapter builder
st.subheader("📚 Continue the Story")
if st.session_state.story:
    chapter_prompt = st.text_area("Add a new chapter:", "")

    if st.button("Generate Chapter"):
        if chapter_prompt.strip():
            full_prompt = st.session_state.story + "\n\n" + chapter_prompt
            new_chapter = generate_story(full_prompt, selected_genre, selected_style)
            if new_chapter:
                st.session_state.story += "\n\n" + new_chapter
                st.write(new_chapter)
        else:
            st.warning("Enter some details for the new chapter!")
else:
    st.info("Generate a story first before adding chapters.")

# Story editor
st.subheader("📝 Edit Your Story")
st.session_state.story = st.text_area("Edit the story:", st.session_state.story)

# Save and download options
def save_story():
    """Saves the story to a text file."""
    with open("story.txt", "w", encoding="utf-8") as file:
        file.write(st.session_state.story)

def download_story():
    """Allows downloading the story as a text file."""
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
    """Saves the story to a PDF file."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in st.session_state.story.split("\n"):
        pdf.cell(200, 10, txt=line, ln=True, align='L')

    pdf.output("story.pdf")

def download_story_as_pdf():
    """Allows downloading the story as a PDF file."""
    save_story_as_pdf()
    with open("story.pdf", "rb") as file:
        st.download_button(label="📥 Download Story as PDF", data=file, file_name="story.pdf", mime="application/pdf")

download_story_as_pdf()
