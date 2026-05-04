"""
LangChain + Streamlit Movie Analyzer (JSON Output Version)
Run: streamlit run app.py
"""

import os
import json
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
    page_title="Movie Analyzer",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 Movie Analyzer (LangChain)")
st.write("Enter a movie description and get structured JSON insights.")

# =========================
# 🔹 LLM SETUP
# =========================
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3   # lower temp = more consistent JSON
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
Extract structured information from the movie summary.

Return ONLY valid JSON. No explanation, no text outside JSON.

Format:
{{
  "movie_name": "",
  "main_characters": [],
  "genre": "",
  "imdb_rating": "",
  "short_summary": ""
}}

Summary:
{summary}
"""
)

# =========================
# 🔹 CHAINS
# =========================
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
            # Detect if already summary
            is_summary = len(movie_text) < 700 and movie_text.count("\n") < 5

            if is_summary:
                summary = movie_text
            else:
                summary = summary_chain.invoke({"movie_input": movie_text})

                st.subheader("🔹 Generated Summary")
                st.write(summary)

            # Extract JSON
            raw_output = extract_chain.invoke({"summary": summary})

            # Parse JSON safely
            try:
                json_output = json.loads(raw_output)

                st.subheader("🎬 Structured Output (JSON)")
                st.json(json_output)

                # Optional: Pretty UI
                st.subheader("✨ Clean View")
                st.write(f"🎬 **Movie:** {json_output.get('movie_name')}")
                st.write(f"🎭 **Characters:** {', '.join(json_output.get('main_characters', []))}")
                st.write(f"🎞️ **Genre:** {json_output.get('genre')}")
                st.write(f"⭐ **IMDb:** {json_output.get('imdb_rating')}")
                st.write(f"📝 **Summary:** {json_output.get('short_summary')}")

                # Download JSON
                st.download_button(
                    label="⬇️ Download JSON",
                    data=json.dumps(json_output, indent=2),
                    file_name="movie_analysis.json",
                    mime="application/json"
                )

            except json.JSONDecodeError:
                st.error("⚠️ Failed to parse JSON. Raw output below:")
                st.text(raw_output)

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

