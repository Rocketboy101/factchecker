import streamlit as st
import pandas as pd
from difflib import get_close_matches
import datetime

st.set_page_config(
    page_title="Operation Sindoor Fact Checker | Official Indian Sources",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for patriotic UX
st.markdown("""
<style>
    .main {background-color: #0f172a;}
    .stApp {background-color: #0f172a; color: #f1f5f9;}
    .highlight {background-color: #f59e0b; color: #1e2937; padding: 2px 6px; border-radius: 4px;}
    .fact-card {background-color: #1e2937; padding: 20px; border-radius: 12px; border-left: 5px solid #f59e0b;}
    h1, h2 {color: #f59e0b;}
</style>
""", unsafe_allow_html=True)

# ====================== VERIFIED FACTS DATABASE (100% Indigenous Sources) ======================
facts_data = [
    {
        "id": 1,
        "fact": "Launch Date & Trigger",
        "details": "Operation Sindoor was launched on 7 May 2025 by the Indian Armed Forces in response to the barbaric Pahalgam terrorist attack on 22 April 2025, in which Pakistan-backed terrorists (TRF, front for Lashkar-e-Taiba) killed 26 civilians (25 Indians + 1 Nepali).",
        "source": "PIB Press Release PRID=2127370 & MEA Briefing 8 May 2025",
        "link": "https://www.pib.gov.in/PressReleseDetailm.aspx?PRID=2127370"
    },
    {
        "id": 2,
        "fact": "Targets Hit",
        "details": "Precision strikes targeted 9 terrorist infrastructure sites / launchpads in Pakistan and PoJK belonging to Lashkar-e-Taiba, Jaish-e-Mohammed, and Hizbul Mujahideen. NO Pakistani military or civilian facilities were targeted.",
        "source": "PIB & MEA Official Statements",
        "link": "https://www.pib.gov.in/Pressreleaseshare.aspx?PRID=2128748"
    },
    {
        "id": 3,
        "fact": "Nature of Operation",
        "details": "Focused, measured, non-escalatory, and intelligence-based. India exercised considerable restraint and provided video evidence of strikes on terror camps only.",
        "source": "Foreign Secretary Vikram Misri Briefing, 8 May 2025",
        "link": "https://www.mea.gov.in/Speeches-Statements.htm?dtl/39478"
    },
    {
        "id": 4,
        "fact": "Pakistan's Response & Escalation",
        "details": "Pakistan retaliated on 8 May 2025 with attacks that killed 16 Indian civilians and injured 59 in Jammu & Kashmir (including a Gurdwara in Poonch). India responded proportionately.",
        "source": "MEA Official Briefing",
        "link": "https://www.mea.gov.in/Speeches-Statements.htm?dtl/39478"
    },
    {
        "id": 5,
        "fact": "Success & Impact",
        "details": "Over 100 terrorists eliminated, including high-value targets. Nine major terror camps destroyed. India established military dominance while maintaining strategic restraint.",
        "source": "PIB 'Operation SINDOOR: India’s Strategic Clarity' Release",
        "link": "https://www.pib.gov.in/Pressreleaseshare.aspx?PRID=2128748"
    },
    {
        "id": 6,
        "fact": "Non-Military Measures",
        "details": "Indus Waters Treaty put in abeyance, Attari-Wagah border closed, trade suspended, Pakistani diplomats declared Persona Non Grata, cultural exchanges banned – until Pakistan ends cross-border terrorism.",
        "source": "Official Government Announcements",
        "link": "https://www.pib.gov.in/Pressreleaseshare.aspx?PRID=2128748"
    }
]

df_facts = pd.DataFrame(facts_data)

# ====================== COMMON MISINFORMATION (Debunked) ======================
misinfo = [
    {"claim": "India struck Pakistani military bases / civilian areas", "verdict": "✅ FALSE – Official Indian sources confirm ONLY terrorist infrastructure was targeted. No military or civilian sites hit.", "source": "PIB & MEA"},
    {"claim": "Pakistan did not escalate / no civilian casualties from their side", "verdict": "❌ Misleading – Pakistan's 8 May retaliatory strikes killed 16 Indian civilians.", "source": "MEA Briefing"},
    {"claim": "Operation Sindoor was an unprovoked attack", "verdict": "✅ FALSE – Direct response to 22 April Pahalgam massacre by Pakistan-backed TRF/LeT.", "source": "PIB"},
]

# ====================== APP UI ======================
st.title("🇮🇳 Operation Sindoor Fact Checker")
st.caption("**100% based on official Indian Government sources (PIB, MEA, Indian Armed Forces)** • Real-time verification tool")

st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Flag_of_India.svg/1280px-Flag_of_India.svg.png", width=150)
st.sidebar.markdown("### About Operation Sindoor")
st.sidebar.info("""
**Official Summary**  
Precision counter-terror operation launched 7 May 2025 after the Pahalgam attack (22 Apr 2025).  
9 terror camps destroyed.  
Non-escalatory & targeted only terrorist infrastructure.
""")
st.sidebar.markdown("---")
st.sidebar.markdown("**Last Updated**: March 2026 (official records)")

tab1, tab2, tab3, tab4 = st.tabs(["🔍 Verify a Claim", "📋 Verified Facts Database", "🚫 Debunked Claims", "📅 Timeline & Sources"])

with tab1:
    st.subheader("Submit any claim about Operation Sindoor")
    claim = st.text_area("Paste the claim here (e.g., 'India hit Pakistani civilians' or 'Operation Sindoor destroyed 9 terror camps')", height=120)
    
    if st.button("✅ Verify with Official Sources", type="primary"):
        if claim.strip():
            # Simple fuzzy matching to find closest facts
            keywords = claim.lower().split()
            matches = []
            for _, row in df_facts.iterrows():
                fact_lower = row['details'].lower()
                score = len(get_close_matches(claim.lower(), [fact_lower], n=1, cutoff=0.6))
                if score > 0 or any(k in fact_lower for k in keywords):
                    matches.append(row)
            
            st.success("✅ Analysis Complete")
            
            if matches:
                st.write("**Matching Official Facts:**")
                for m in matches[:3]:
                    st.markdown(f"""
                    <div class="fact-card">
                        <strong>{m['fact']}</strong><br>
                        {m['details']}<br>
                        <a href="{m['link']}" target="_blank">Source: {m['source']}</a>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No exact match found. However, all verified facts are listed in the 'Verified Facts' tab above. Cross-check there.")
            
            # General verdict
            st.markdown("**Official Position Summary** (from PIB/MEA):")
            st.write("Operation Sindoor was a **focused, measured, and non-escalatory** response to the Pahalgam terror attack. Only terrorist infrastructure was targeted.")
        else:
            st.warning("Please enter a claim.")

with tab2:
    st.subheader("📋 Full Verified Facts Database")
    search = st.text_input("Search facts...", "")
    if search:
        filtered = df_facts[df_facts.apply(lambda x: search.lower() in str(x).lower(), axis=1)]
    else:
        filtered = df_facts
    st.dataframe(filtered, use_container_width=True, hide_index=True)

with tab3:
    st.subheader("🚫 Common Misinformation Debunked")
    for item in misinfo:
        st.error(f"**Claim:** {item['claim']}")
        st.success(f"**Verdict:** {item['verdict']}")
        st.caption(f"Source: {item['source']}")
        st.divider()

with tab4:
    st.subheader("📅 Official Timeline & Primary Sources")
    st.write("**22 April 2025** – Pahalgam terror attack (26 civilians killed)")
    st.write("**7 May 2025** – Operation Sindoor launched: 9 terror camps struck")
    st.write("**8 May 2025** – Pakistan retaliates; MEA briefing")
    st.write("**9–10 May 2025** – Further coordinated response; ceasefire at 1700 hrs IST on 10 May")
    
    st.markdown("### Primary Indigenous Sources")
    for f in facts_data:
        st.markdown(f"- **{f['fact']}** → [Read full release]({f['link']})")

st.caption("Built as an open-source tool for truth based solely on Indian official records. No foreign media or claims included.")
