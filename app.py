
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os

# Page setup
st.set_page_config(
    page_title="LinkedIn Post Generator",
    page_icon="💼",
    layout="wide"
)

# Few shot examples
few_shot_posts = [
    {
        "topic": "AI",
        "length": "Medium",
        "post": """Just completed building my first RAG application! 🚀

What I learned:
→ LLMs are powerful but need YOUR data to be truly useful
→ ChromaDB makes vector search surprisingly simple
→ Langchain connects everything beautifully

The feeling when your chatbot answers questions from your own PDF correctly... priceless.

If you're learning AI, start with RAG. It's the most practical skill you can build right now.

#AI #MachineLearning #RAG #Langchain #Python"""
    },
    {
        "topic": "Data Science",
        "length": "Short",
        "post": """3 things I wish I knew before starting Data Science:

1️⃣ Clean data beats fancy models every time
2️⃣ Communication skills matter as much as technical skills
3️⃣ Start with simple models before complex ones

What would you add to this list?

#DataScience #MachineLearning #CareerTips"""
    },
    {
        "topic": "Career",
        "length": "Long",
        "post": """From zero to building AI applications in 3 months. Here's my honest journey.

3 months ago I had no idea what an LLM was. Today I have deployed AI applications that solve real problems.

What changed?

✅ I stopped watching tutorials and started building
✅ I focused on one project at a time
✅ I documented everything on GitHub
✅ I asked questions when stuck instead of giving up

The AI field is moving fast. But that's actually good news for learners. Companies need people who can BUILD with AI — not just talk about it.

You don't need a PhD. You don't need 10 years of experience.
You need consistency, curiosity and real projects.

Start today. Build something. Put it on GitHub.

That's it.

#AI #CareerGrowth #MachineLearning #Python #NeverStopLearning"""
    }
]

def get_length_text(length):
    if length == "Short":
        return "1-3 lines"
    elif length == "Medium":
        return "4-6 lines"
    else:
        return "7-10 lines"

def generate_post(topic, tone, length, use_emoji, api_key):
    llm = ChatGroq(model="llama-3.1-8b-instant", api_key=api_key)
    length_text = get_length_text(length)
    examples = ""
    for i, post in enumerate(few_shot_posts):
        examples += f"\nExample {i+1}:\n{post['post']}\n"
    emoji_instruction = "Use relevant emojis." if use_emoji else "Do not use emojis."

    prompt = ChatPromptTemplate.from_template("""
You are a LinkedIn content expert. Generate a professional LinkedIn post.

Here are some example LinkedIn posts for style reference:
{examples}

Now generate a NEW LinkedIn post with these requirements:
- Topic: {topic}
- Tone: {tone}
- Length: {length_text}
- {emoji_instruction}
- End with 3-5 relevant hashtags
- Make it engaging and authentic
- Do not copy the examples, just match the style

Generate 3 different variations separated by ---
""")

    chain = prompt | llm
    response = chain.invoke({
        "examples": examples,
        "topic": topic,
        "tone": tone,
        "length_text": length_text,
        "emoji_instruction": emoji_instruction
    })
    return response.content

# Header
st.title("💼 LinkedIn Post Generator")
st.markdown("### Built by Mohammad Murtaza | Few Shot Learning + LLaMA + Langchain")
st.markdown("---")

# Info columns
col1, col2, col3 = st.columns(3)
with col1:
    st.info("✍️ Enter your topic")
with col2:
    st.info("🎯 Choose tone and length")
with col3:
    st.info("🚀 Generate 3 variations instantly")

st.markdown("---")

# Sidebar
st.sidebar.title("⚙️ Settings")
st.sidebar.markdown("""
### About
This app uses **Few Shot Learning** to generate LinkedIn posts that match a professional writing style.

**Tech Stack:**
- 🦙 LLaMA 3.1 (Groq)
- 🔗 Langchain
- ✨ Few Shot Learning
- 🎨 Streamlit
""")
st.sidebar.markdown("---")
groq_api_key = st.sidebar.text_input(
    "🔑 Enter Groq API Key",
    type="password",
    help="Get your free key at console.groq.com"
)
st.sidebar.markdown("---")
st.sidebar.markdown("👨‍💻 [GitHub Profile](https://github.com/Murtaza-data)")

# Main inputs
st.markdown("### ✍️ Post Details")

col1, col2 = st.columns(2)
with col1:
    topic = st.text_input(
        "What is your post about?",
        placeholder="e.g. completing an AI project, learning Python, career advice"
    )
    tone = st.selectbox(
        "Select Tone",
        ["Inspirational", "Professional", "Casual", "Educational"]
    )

with col2:
    length = st.selectbox(
        "Select Length",
        ["Short", "Medium", "Long"]
    )
    use_emoji = st.toggle("Include Emojis", value=True)

st.markdown("---")

generate_btn = st.button("🚀 Generate Posts", type="primary", use_container_width=True)

if generate_btn:
    if not groq_api_key:
        st.warning("⚠️ Please enter your Groq API Key in the sidebar.")
    elif not topic:
        st.warning("⚠️ Please enter a topic for your post.")
    else:
        with st.spinner("✨ Generating your LinkedIn posts..."):
            result = generate_post(topic, tone, length, use_emoji, groq_api_key)
            variations = result.split("---")

        st.markdown("### 📝 Your Generated Posts")
        for i, variation in enumerate(variations):
            if variation.strip():
                st.markdown(f"#### Variation {i+1}")
                st.markdown(variation.strip())
                st.code(variation.strip(), language=None)
                st.markdown("---")

# Footer
st.markdown("---")
st.markdown(
    "Built by **Mohammad Murtaza** | "
    "[GitHub](https://github.com/Murtaza-data) | "
    "Powered by Few Shot Learning + LLaMA + Langchain"
)
