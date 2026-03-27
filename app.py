import streamlit as st
import pandas as pd
from openai import OpenAI

st.set_page_config(
    page_title="Operation Sindoor Fact Checker | Groq AI",
    page_icon="🇮🇳",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {background-color: #0f172a; color: #f1f5f9;}
    .fact-card {background-color: #1e2937; padding: 20px; border-radius: 12px; border-left: 6px solid #f59e0b; margin: 10px 0;}
    .verdict-box {padding: 20px; border-radius: 12px; background-color: #166534; color: #dcfce7; font-size: 1.05rem;}
    h1, h2 {color: #f59e0b;}
    .groq-badge {background-color: #22c55e; color: #1e2937; padding: 4px 14px; border-radius: 9999px; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# ====================== OFFICIAL INDIGENOUS FACTS (PIB / MEA) ======================
facts_data = [
    {"fact": "Trigger Event", "details": "22 April 2025 Pahalgam terrorist attack by Pakistan-backed TRF (Lashkar-e-Taiba front) killed 26 civilians.", "source": "PIB", "link": "https://www.pib.gov.in/Pressreleaseshare.aspx?PRID=2128748"},
    {"fact": "Operation Launch", "details": "Operation Sindoor launched on the night of 6–7 May 2025 as a precise, measured, non-escalatory counter-terror operation.", "source": "PIB & MEA", "link": "https://www.pib.gov.in/PressReleasePage.aspx?PRID=2128748"},
    {"fact": "Targets", "details": "Nine terrorist infrastructure / launchpads in Pakistan and PoJK (LeT, JeM, Hizbul). No Pakistani military or civilian facilities were targeted.", "source": "PIB Strategic Clarity", "link": "https://www.pib.gov.in/Pressreleaseshare.aspx?PRID=2128748"},
    {"fact": "Results", "details": "Over 100 terrorists eliminated. India showed precision, restraint and strategic dominance while providing evidence of terror camp strikes.", "source": "PIB", "link": "https://www.pib.gov.in/PressReleasePage.aspx?PRID=2128748"},
    {"fact": "Pakistan Response", "details": "Pakistan retaliated on 8 May 2025, killing 16 Indian civilians. India responded proportionately. DGMO ceasefire understanding on 10 May 2025.", "source": "MEA Briefing", "link": "https://www.mea.gov.in/Speeches-Statements.htm?dtl/39478"},
    {"fact": "Non-military measures", "details": "Indus Waters Treaty kept in abeyance, trade suspended, diplomats declared persona non grata until Pakistan ends cross-border terrorism.", "source": "Government of India"},
]

context = "\n\n".join([f"Fact {i+1}: {row['fact']}\nDetails: {row['details']}\nSource: {row['source']} ({row['link']})" for i, row in pd.DataFrame(facts_data).iterrows()])

# ====================== APP ======================
st.title("🇮🇳 Operation Sindoor Fact Checker")
st.caption("**AI-Powered with Free Groq Models** • Updated March 2026 • 100% Grounded in Official Indian Sources")

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Flag_of_India.svg/1280px-Flag_of_India.svg.png", width=150)
    st.markdown("### 🔑 Groq API (Free Tier)")
    st.info("Get free API key at https://console.groq.com/keys")
    api_key = st.text_input("Groq API Key", type="password")
    
    model = st.selectbox(
        "Select Groq Model",
        [
            "llama-3.3-70b-versatile",      # Best reasoning
            "llama-3.1-8b-instant",         # Fast & cheap
            "openai/gpt-oss-120b"           # Larger model
        ],
        index=0
    )
    st.caption("llama-3.3-70b-versatile recommended for accurate fact-checking")

tab1, tab2, tab3, tab4 = st.tabs(["🔍 AI Claim Verifier (Groq)", "📋 Official Facts", "🚫 Misinfo", "📡 Sources Feed"])

with tab1:
    st.subheader("Verify Any Claim with Groq AI")
    st.markdown('<span class="groq-badge">UPDATED MODELS • FIXED</span>', unsafe_allow_html=True)
    
    claim = st.text_area("Paste any claim about Operation Sindoor", height=140,
                         placeholder="Example: India attacked Pakistani civilian areas during Operation Sindoor")
    
    if st.button("🚀 Verify with Groq AI", type="primary", use_container_width=True):
        if not api_key:
            st.error("❌ Please enter your Groq API key in the sidebar.")
        elif not claim.strip():
            st.warning("Please enter a claim.")
        else:
            with st.spinner("Groq is analysing using official Indian records..."):
                try:
                    client = OpenAI(
                        api_key=api_key,
                        base_url="https://api.groq.com/openai/v1"
                    )
                    
                    system_prompt = f"""You are a strict Fact Checker for Operation Sindoor.
Answer **only** using the verified Indian government sources below (PIB, MEA, Armed Forces).
Do not add any external information, foreign media, or speculation.
If the claim contradicts official records, clearly state it is false or misleading and quote the relevant facts.
Always cite sources and links.

OFFICIAL CONTEXT:
{context}

Analyse the claim carefully and give a clear verdict."""

                    response = client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": f"Claim to verify: {claim}"}
                        ],
                        temperature=0.1,
                        max_tokens=900
                    )
                    
                    verdict = response.choices[0].message.content
                    
                    st.success("✅ Groq Analysis Complete")
                    st.markdown(f'<div class="verdict-box">{verdict}</div>', unsafe_allow_html=True)
                    st.caption("Strictly grounded in provided official Indian sources only.")
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}\nCommon fixes:\n• Check if your API key has quota\n• Try a different model\n• Wait 30–60 seconds and retry")

with tab2:
    st.subheader("📋 Verified Official Facts Database")
    df = pd.DataFrame(facts_data)
    search = st.text_input("Search facts...")
    filtered = df[df.apply(lambda x: search.lower() in str(x).lower(), axis=1)] if search else df
    st.dataframe(filtered, use_container_width=True, hide_index=True)

with tab3:
    st.subheader("🚫 Common Misinformation")
    st.info("Copy-paste any of these into the AI verifier for instant analysis.")
    for c in [
        "India struck Pakistani military or civilian areas",
        "Operation Sindoor was unprovoked",
        "Pakistan never retaliated during Operation Sindoor"
    ]:
        st.error(f"**Claim:** {c}")

with tab4:
    st.subheader("📡 Official Sources Feed")
    releases = [
        {"title": "Operation SINDOOR: India’s Strategic Clarity", "date": "14 May 2025", "link": "https://www.pib.gov.in/Pressreleaseshare.aspx?PRID=2128748"},
        {"title": "Foreign Secretary Briefing on Operation Sindoor", "date": "8 May 2025", "link": "https://www.mea.gov.in/Speeches-Statements.htm?dtl/39478"},
    ]
    for r in releases:
        st.markdown(f"**{r['title']}** ({r['date']}) → [Read full release]({r['link']})")

st.caption("v5.1 • Groq Models Updated (March 2026) • mixtral error fixed • 100% Indigenous Official Sources")
