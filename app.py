import streamlit as st
from groq import Groq
import webbrowser
import re
from datetime import datetime

# --- সেটিংস ---
AGENT_NAME = "Sara" 
USER_NAME = "Skylord"
# --------------

st.set_page_config(page_title=AGENT_NAME, page_icon="🤖", layout="wide")
st.title(f"🤖 {AGENT_NAME} - Advanced AI Agent")

client = Groq(api_key="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")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system", 
            "content": f"You are {AGENT_NAME}, an autonomous AI. Always help {USER_NAME}. If asked for a site or song, output 'GO_TO: [URL]' or 'SEARCH: [query]'. Be fast."
        }
    ]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("সারা-কে কমান্ড দিন..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            )
            full_response = response.choices[0].message.content
            
            # --- সরাসরি লিঙ্ক বানানোর লজিক ---
            final_link = None
            
            if ".com" in prompt.lower() or "open" in prompt.lower():
                # সরাসরি URL তৈরি করা (যেমন: facebook.com)
                match = re.search(r'[a-zA-Z0-0]+\.[a-z]{2,}', prompt)
                if match:
                    final_link = f"https://www.{match.group()}"
            
            if "youtube" in prompt.lower() or "song" in prompt.lower():
                # ইউটিউব সার্চ লিঙ্ক তৈরি করা
                query = prompt.replace("play", "").replace("youtube", "").strip().replace(" ", "+")
                final_link = f"https://www.youtube.com/results?search_query={query}"

            if final_link:
                st.success(f"✅ Sara is opening: {final_link}")
                webbrowser.open(final_link)
                full_response += f"\n\n[Click here to open directly]({final_link})"

            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Error: {e}")
