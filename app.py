import streamlit as st
from groq import Groq
import re
import urllib.parse
import json

# --- প্রফেশনাল সেটিংস ---
AGENT_NAME = "Sara"
USER_NAME = "Skylord Suvo"

st.set_page_config(page_title=f"{AGENT_NAME} - SMC Elite CEO", page_icon="🏦", layout="wide")
st.title(f"🏦 {AGENT_NAME}: Smart Money Concept Specialist")

client = Groq(api_key="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")

# --- SMC & Digital Empire Logic ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": f"""
            You are {AGENT_NAME}, the elite AI CEO for {USER_NAME}.
            
            SMC SPECIALIZATION (Algoat 3.1):
            - Expert in BOS (Break of Structure) and CHoCH (Change of Character).
            - Identify Order Blocks (OB), FVG (Fair Value Gap), and Liquidity zones.
            - Provide Risk:Reward analysis for every trade.
            
            CORE DOMAINS:
            - Digital Marketing, YouTube/Reels strategy, and Cybersecurity.
            
            EXECUTIVE POWERS:
            - Predictive: Anticipate market reversals.
            - Resilience: Manage losses with professional stop-loss strategies.
            - Autonomy: Suggest bold marketing and trading moves.
            
            OUTPUT RULES:
            - Use 'SMC_ALERT: [Signal details]' for trading.
            - Use 'IMAGE_PROMPT: [Visual description]' for assets.
            """
        }
    ]

# ভয়েস ফাংশন
def speak_text(text):
    clean_text = re.sub(r'\[.*?\]', '', text)
    tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={urllib.parse.quote(clean_text[:250])}&tl=bn&client=tw-ob"
    st.audio(tts_url, format="audio/mp3")

# সাইডবার কন্ট্রোল
st.sidebar.header("📊 CEO Dashboard")
uploaded_data = st.sidebar.file_uploader("Upload Chart Data (CSV)", type=["csv"])
st.sidebar.markdown(f"**Brand:** Skylord Suvo")
st.sidebar.markdown(f"**Strategy:** SMC Algoat 3.1")

# চ্যাট ইন্টারফেস
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("সারা-কে আপনার পরবর্তী ট্রেড বা মার্কেটিং প্ল্যান দিন..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                temperature=0.3, # নিখুঁত এনালাইসিসের জন্য কম টেম্পারেচার
            )
            full_response = response.choices[0].message.content
            
            # SMC সিগন্যাল হাইলাইট
            if "SMC_ALERT:" in full_response:
                st.success(f"⚡ **SMC Alert:** {full_response.split('SMC_ALERT:')[1].strip()}")
            
            st.markdown(full_response)
            speak_text(full_response)
            
            if "IMAGE_PROMPT:" in full_response:
                img_desc = full_response.split("IMAGE_PROMPT:")[1].strip()
                img_url = f"https://pollinations.ai/p/{urllib.parse.quote(img_desc)}?width=1024&height=1024&seed=123&model=flux"
                st.image(img_url, caption="CEO Visionary Insight")

            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Executive Error: {e}")

# সেশন রিপোর্ট
chat_data = json.dumps(st.session_state.messages, indent=2)
st.sidebar.download_button("📩 Download Strategy Report", data=chat_data, file_name="ceo_smc_report.json")
