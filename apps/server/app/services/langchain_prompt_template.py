"""
LangChain + Streamlit Movie Analyzer
Run: streamlit run app.py
"""

import os
from dotenv import load_dotenv
import streamlit as st

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# =========================
# 🔹 LOAD ENV
# =========================
load_dotenv()

# =========================
# 🔹 PAGE CONFIG
# =========================
st.set_page_config(
    page_title="🎬 Movie Analyzer",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 Movie Analyzer (LangChain)")
st.write("Enter a movie description and get structured insights.")

# =========================
# 🔹 LLM SETUP
# =========================
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.5
)

parser = StrOutputParser()

# =========================
# 🔹 PROMPTS
# =========================
summary_prompt = PromptTemplate.from_template(
"""
Summarize the movie description clearly and concisely.

Input:
{movie_input}
"""
)

extract_prompt = PromptTemplate.from_template(
"""
Extract structured information from this movie summary.

Return ONLY:

Movie Name:
Main Characters:
Genre:
IMDb Rating (out of 10):
Short Summary:

Summary:
{summary}
"""
)

# Chains
summary_chain = summary_prompt | llm | parser
extract_chain = extract_prompt | llm | parser

# =========================
# 🔹 UI INPUT
# =========================
movie_text = st.text_area(
    "✍️ Enter Movie Description:",
    height=200,
    placeholder="Example: A boy discovers he is a wizard and goes to a magical school..."
)

analyze_btn = st.button("🚀 Analyze Movie")

# =========================
# 🔹 PROCESS
# =========================
if analyze_btn:

    if not movie_text.strip():
        st.warning("⚠️ Please enter a movie description.")
        st.stop()

    with st.spinner("⏳ Processing..."):

        try:
            # Detect summary
            is_summary = len(movie_text) < 700 and movie_text.count("\n") < 5

            if is_summary:
                summary = movie_text
            else:
                summary = summary_chain.invoke({"movie_input": movie_text})

            # Show summary
            if not is_summary:
                st.subheader("🔹 Summary")
                st.write(summary)

            # Extract
            final_output = extract_chain.invoke({"summary": summary})

            st.subheader("🎬 Final Output")
            st.text(final_output)

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")