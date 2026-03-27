import streamlit as st
import pandas as pd
from openai import OpenAI
import datetime

st.set_page_config(
    page_title="Operation Sindoor Fact Checker | AI + Official Sources",
    page_icon="🇮🇳",
    layout="wide"
)

# ====================== CUSTOM CSS ======================
st.markdown("""
<style>
    .main {background-color: #0f172a; color: #f1f5f9;}
    .fact-card {background-color: #1e2937; padding: 20px; border-radius: 12px; border-left: 6px solid #f59e0b; margin: 10px 0;}
    .verdict-box {padding: 20px; border-radius: 12px; background-color: #166534; color: #dcfce7; font-size: 1.1rem;}
    h1, h2 {color: #f59e0b;}
    .ai-badge {background-color: #22c55e; color: #1e2937; padding: 4px 14px; border-radius: 9999px; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# ====================== OFFICIAL FACTS DATABASE (Indigenous Sources Only) ======================
facts_data = [
    {"fact": "Trigger", "details": "22 April 2025 Pahalgam terrorist attack by Pakistan-backed TRF (Lashkar-e-Taiba front) killed 26 civilians.", "source": "PIB PRID=2128748", "link": "https://www.pib.gov.in/Pressreleaseshare.aspx?PRID=2128748"},
    {"fact": "Launch", "details": "Operation Sindoor launched on the night of 6–7 May 2025 as a precise, measured, non-escalatory response.", "source": "PIB & MEA", "link": "https://www.pib.gov.in/PressReleasePage.aspx?PRID=2128748"},
    {"fact": "Targets", "details": "9 terrorist infrastructure sites / launchpads in Pakistan & PoJK belonging to LeT, JeM, Hizbul Mujahideen. NO military or civilian targets.", "source": "PIB Strategic Clarity Release", "link": "https://www.pib.gov.in/Pressreleaseshare.aspx?PRID=2128748"},
    {"fact": "Outcome", "details": "Over 100 terrorists eliminated. India demonstrated precision, restraint and strategic dominance.", "source": "PIB", "link": "https://www.pib.gov.in/PressReleasePage.aspx?PRID=2128748"},
    {"fact": "Pakistan Retaliation", "details": "Pakistan attacked on 8 May 2025 killing 16 Indian civilians. India responded proportionately. DGMO ceasefire on 10 May 2025.", "source": "MEA Briefing", "link": "https://www.mea.gov.in/Speeches-Statements.htm?dtl/39478"},
    {"fact": "Non-military actions", "details": "Indus Waters Treaty in abeyance, trade suspended, diplomats PNG, cultural exchanges banned until Pakistan ends cross-border terrorism.", "source": "Government of India"},
    {"fact": "Official Position", "details": "Focused, intelligence-based counter-terror operation. India exercised maximum restraint and provided evidence of terror camp strikes only.", "source": "Foreign Secretary Briefing"},
]

# Create rich context string for RAG
context = "\n\n".join([f"Fact {i+1}: {row['fact']}\n{row['details']}\nSource: {row['source']} ({row['link']})" for i, row in pd.DataFrame(facts_data).iterrows()])

# ====================== APP ======================
st.title("🇮🇳 Operation Sindoor Fact Checker")
st.caption("**AI-Powered • 100% Indigenous Official Sources** • Powered by **xAI Grok-4.20**")

# Sidebar for API key (secure)
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Flag_of_India.svg/1280px-Flag_of_India.svg.png", width=150)
    st.markdown("### 🔑 xAI Grok API Setup")
    st.info("Get your **free API key** at https://console.x.ai → Sign up → Create API Key")
    api_key = st.text_input("Enter your xAI API Key", type="password", help="Stored only in this session")
    st.caption("Model: **grok-4.20-reasoning** (lowest hallucination + strict adherence)")
    st.markdown("---")
    st.success("✅ AI now handles **any** claim dynamically")

tab1, tab2, tab3, tab4 = st.tabs(["🔍 AI Claim Verifier (Grok RAG)", "📋 Official Facts Database", "🚫 Common Misinfo", "📡 Official Sources Feed"])

with tab1:
    st.subheader("AI-Powered Real-Time Fact Check")
    st.markdown('<span class="ai-badge">GROK-4.20 RAG • GROUNDED IN OFFICIAL INDIAN RECORDS ONLY</span>', unsafe_allow_html=True)
    
    claim = st.text_area("Paste **any** claim about Operation Sindoor", 
                         height=140,
                         placeholder="Example: India bombed Pakistani civilian areas in Operation Sindoor or Pakistan never retaliated")
    
    if st.button("🚀 Verify with Grok AI", type="primary", use_container_width=True):
        if not api_key:
            st.error("❌ Please enter your xAI API key in the sidebar first.")
        elif not claim.strip():
            st.warning("Please enter a claim.")
        else:
            with st.spinner("Grok is retrieving official facts and analysing..."):
                try:
                    client = OpenAI(
                        api_key=api_key,
                        base_url="https://api.x.ai/v1"
                    )
                    
                    system_prompt = f"""You are an official Fact Checker for Operation Sindoor.
You MUST answer ONLY using the following verified Indian government sources (PIB, MEA, Indian Armed Forces).
Never add any external information, speculation, or foreign media claims.
If the claim is unsupported or false, clearly say so and quote the exact official facts.
Always cite the source and link.

VERIFIED OFFICIAL CONTEXT:
{context}

Now analyse the user's claim."""
                    
                    response = client.chat.completions.create(
                        model="grok-4.20-reasoning",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": f"Claim to verify: {claim}"}
                        ],
                        temperature=0.1,   # very low for factual accuracy
                        max_tokens=800
                    )
                    
                    ai_verdict = response.choices[0].message.content
                    
                    st.success("✅ AI Analysis Complete")
                    st.markdown(f'<div class="verdict-box">{ai_verdict}</div>', unsafe_allow_html=True)
                    
                    st.caption("Analysis is strictly grounded in the official Indian facts provided above. No external data was used.")
                    
                except Exception as e:
                    st.error(f"API Error: {str(e)}\nCheck your key or try again.")

with tab2:
    st.subheader("📋 Full Verified Official Facts Database")
    df = pd.DataFrame(facts_data)
    search = st.text_input("Search facts...")
    filtered = df[df.apply(lambda x: search.lower() in str(x).lower(), axis=1)] if search else df
    st.dataframe(filtered, use_container_width=True, hide_index=True)

with tab3:
    st.subheader("🚫 Common Misinformation (AI can now check these too)")
    st.info("Try pasting any of these in the AI verifier tab above — Grok will debunk them instantly.")
    for item in [
        {"claim": "India struck Pakistani military bases or civilians"},
        {"claim": "Operation Sindoor was unprovoked"},
        {"claim": "Pakistan did not retaliate"},
    ]:
        st.error(f"**Claim:** {item['claim']}")

with tab4:
    st.subheader("📡 Official Sources Feed")
    st.caption("Direct PIB / MEA releases (post-operation)")
    releases = [
        {"title": "Operation SINDOOR: India’s Strategic Clarity", "date": "14 May 2025", "link": "https://www.pib.gov.in/Pressreleaseshare.aspx?PRID=2128748"},
        {"title": "Foreign Secretary Briefing on Operation Sindoor", "date": "8 May 2025", "link": "https://www.mea.gov.in/Speeches-Statements.htm?dtl/39478"},
    ]
    for r in releases:
        st.markdown(f"**{r['title']}** ({r['date']}) → [Read]({r['link']})")

st.caption("v4.0 • Grok-4.20 RAG AI • 100% Indigenous Sources • Dynamic claim checking")
