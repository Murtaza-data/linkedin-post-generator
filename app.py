
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

st.set_page_config(page_title="LinkedIn Post Generator", page_icon="💼", layout="wide")

# Default example posts
default_posts = [
"""Just completed building my first RAG application! 🚀

What I learned:
→ LLMs are powerful but need YOUR data to be truly useful
→ ChromaDB makes vector search surprisingly simple
→ Langchain connects everything beautifully

#AI #MachineLearning #RAG #Langchain #Python""",

"""3 things I wish I knew before starting Data Science:

1️⃣ Clean data beats fancy models every time
2️⃣ Communication skills matter as much as technical skills
3️⃣ Start with simple models before complex ones

#DataScience #MachineLearning #CareerTips""",

"""From zero to building AI applications in 3 months.

What changed?
✅ I stopped watching tutorials and started building
✅ I focused on one project at a time
✅ I documented everything on GitHub

#AI #CareerGrowth #MachineLearning #Python"""
]

def extract_style(posts, api_key):
    llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=api_key)
    posts_text = "\n---\n".join(posts)
    prompt = ChatPromptTemplate.from_template("""
Analyze these LinkedIn posts and extract the writing style profile:

{posts}

Return ONLY this format:
Tone: [one word: Inspirational/Professional/Casual/Educational]
Sentence style: [short description of how sentences are structured]
Structure: [e.g. bullet points, numbered lists, paragraphs]
Vocabulary: [simple/technical/motivational]
Signature patterns: [any repeated patterns like arrows →, checkmarks ✅, etc.]
""")
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"posts": posts_text})

def generate_post(topic, length, use_emoji, api_key, posts, style_profile):
    llm = ChatGroq(model="llama-3.1-8b-instant", api_key=api_key)

    length_map = {"Short": "1-3 lines", "Medium": "4-6 lines", "Long": "7-10 lines"}
    length_text = length_map[length]

    examples = "\n---\n".join(posts)
    emoji_instruction = "Use relevant emojis matching the style above." if use_emoji else "Do not use any emojis."

    prompt = ChatPromptTemplate.from_template("""
You are writing a LinkedIn post on behalf of a real person.
Your goal is to write exactly how THEY write — same tone, same structure, same vocabulary, same personality.

Here is their writing style profile:
{style_profile}

Here are examples of their actual posts:
{examples}

Now write a NEW LinkedIn post with:
- Topic: {topic}
- Length: {length_text}
- {emoji_instruction}
- End with 3-5 relevant hashtags
- Match their style so closely it sounds like THEY wrote it, not an AI

Generate 3 variations separated by ---
""")

    chain = prompt | llm | StrOutputParser()
    return chain.invoke({
        "style_profile": style_profile,
        "examples": examples,
        "topic": topic,
        "length_text": length_text,
        "emoji_instruction": emoji_instruction
    })

# --- Sidebar ---
st.sidebar.title("⚙️ Settings")
groq_api_key = st.sidebar.text_input(
    "🔑 Enter Groq API Key",
    type="password",
    help="Get your free key at console.groq.com"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### ✍️ Paste Your LinkedIn Posts")
st.sidebar.markdown("Paste 2-3 of your own posts below, separated by **---**. The app will match your personal writing style.")

pasted_posts = st.sidebar.text_area(
    "Your posts:",
    height=250,
    placeholder="Paste your first post here...\n---\nPaste your second post here...\n---\nPaste your third post here..."
)

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.markdown("""
**Tech Stack:**
- 🦙 LLaMA 3.1 (Groq)
- 🔗 Langchain
- ✨ Few Shot Learning
- 🎨 Streamlit
""")
st.sidebar.markdown("---")
st.sidebar.markdown("👨‍💻 [GitHub Profile](https://github.com/Murtaza-data)")

# --- Header ---
st.title("💼 LinkedIn Post Generator")
st.markdown("### Few Shot Learning + LLaMA + Langchain")
st.markdown("---")

col1, col2, col3 = st.columns(3)
with col1:
    st.info("✍️ Paste your LinkedIn posts")
with col2:
    st.info("🎯 Choose topic and length")
with col3:
    st.info("🚀 Get posts in YOUR style")

st.markdown("---")

# --- Load posts ---
if pasted_posts.strip():
    posts = [p.strip() for p in pasted_posts.split("---") if p.strip()]
    st.success(f"✅ {len(posts)} posts loaded. The app will match your personal writing style.")
    using_custom = True
else:
    posts = default_posts
    st.info("💡 Using default example posts. Paste your own posts in the sidebar to match your personal style.")
    using_custom = False

# --- Main inputs ---
st.markdown("### ✍️ Post Details")

col1, col2 = st.columns(2)
with col1:
    topic = st.text_input(
        "What is your post about?",
        placeholder="e.g. completing an AI project, learning Python, career advice"
    )
with col2:
    length = st.selectbox("Select Length", ["Short", "Medium", "Long"])
    use_emoji = st.toggle("Include Emojis", value=True)

st.markdown("---")

generate_btn = st.button("🚀 Generate Posts", type="primary", use_container_width=True)

if generate_btn:
    if not groq_api_key:
        st.warning("⚠️ Please enter your Groq API Key in the sidebar.")
    elif not topic:
        st.warning("⚠️ Please enter a topic for your post.")
    else:
        with st.spinner("🔍 Analyzing your writing style..."):
            style_profile = extract_style(posts, groq_api_key)

        with st.spinner("✨ Generating posts in your style..."):
            result = generate_post(topic, length, use_emoji, groq_api_key, posts, style_profile)
            variations = result.split("---")

        st.markdown("### 📝 Your Generated Posts")
        for i, variation in enumerate(variations):
            if variation.strip():
                st.markdown(f"#### Variation {i+1}")
                st.markdown(variation.strip())
                st.code(variation.strip(), language=None)
                st.markdown("---")

# --- Footer ---
st.markdown("---")
st.markdown(
    "Powered by Few Shot Learning + LLaMA + Langchain | "
    "[GitHub](https://github.com/Murtaza-data)"
)
