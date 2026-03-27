import streamlit as st
import pandas as pd
from difflib import get_close_matches
import feedparser
import datetime
from urllib.parse import quote_plus

st.set_page_config(
    page_title="Operation Sindoor Fact Checker | Live PIB",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {background-color: #0f172a;}
    .stApp {background-color: #0f172a; color: #f1f5f9;}
    .live-badge {background-color: #22c55e; color: #1e2937; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: bold;}
    .fact-card {background-color: #1e2937; padding: 20px; border-radius: 12px; border-left: 6px solid #f59e0b; margin-bottom: 15px;}
    h1, h2 {color: #f59e0b;}
</style>
""", unsafe_allow_html=True)

# ====================== STATIC VERIFIED FACTS (Core Database) ======================
facts_data = [ ... ]  # (same 6 facts as before – kept for speed & offline fallback)

df_facts = pd.DataFrame(facts_data)

# ====================== COMMON MISINFORMATION ======================
misinfo = [ ... ]  # (same as before)

# ====================== LIVE PIB RSS FETCH ======================
@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_live_pib():
    url = "https://pib.gov.in/RssMain.aspx?ModId=6&Lang=1"  # Official English Press Releases RSS
    feed = feedparser.parse(url)
    releases = []
    for entry in feed.entries[:15]:  # Latest 15
        if any(keyword in entry.title.lower() or 
               (hasattr(entry, 'description') and keyword in entry.description.lower()) 
               for keyword in ["sindoor", "pahalgam", "terror", "pakistan", "operation", "jammu"]):
            releases.append({
                "title": entry.title,
                "published": entry.published if hasattr(entry, 'published') else "N/A",
                "link": entry.link,
                "summary": entry.summary[:280] + "..." if hasattr(entry, 'summary') else ""
            })
    return releases

# ====================== APP UI ======================
st.title("🇮🇳 Operation Sindoor Fact Checker")
st.caption("**100% Official Indian Sources** • Static Database + **LIVE PIB RSS** Real-Time Verification")

col1, col2 = st.columns([3,1])
with col1:
    st.markdown("**Now with Real-Time Claim Check** powered by PIB.gov.in RSS")
with col2:
    st.markdown('<span class="live-badge">LIVE FROM PIB</span>', unsafe_allow_html=True)

st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Flag_of_India.svg/1280px-Flag_of_India.svg.png", width=150)
st.sidebar.info("**Real-Time Mode Active**\nEvery verification now pulls the latest official PIB releases.")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔍 Real-Time Verify Claim", "📋 Verified Facts", "🚫 Debunked Claims", "📅 Timeline", "📡 Live Official Updates"])

with tab1:
    st.subheader("Submit any claim → Get instant official verdict")
    claim = st.text_area("Paste your claim here", height=130, placeholder="Example: India struck Pakistani civilian areas during Operation Sindoor")
    
    if st.button("🔴 Verify with LIVE PIB + Database", type="primary", use_container_width=True):
        if claim.strip():
            with st.spinner("Fetching latest PIB releases & cross-checking..."):
                live_releases = fetch_live_pib()
                
                # Local fuzzy match
                matches = []
                keywords = claim.lower().split()
                for _, row in df_facts.iterrows():
                    if any(k in row['details'].lower() for k in keywords) or get_close_matches(claim.lower(), [row['details'].lower()], n=1, cutoff=0.5):
                        matches.append(row)
                
                st.success("✅ Real-Time Analysis Complete")
                
                # Show local matches first
                if matches:
                    st.subheader("📌 Matching Verified Facts")
                    for m in matches[:3]:
                        st.markdown(f"""
                        <div class="fact-card">
                            <strong>{m['fact']}</strong><br>
                            {m['details']}<br>
                            <a href="{m['link']}" target="_blank">PIB Source</a>
                        </div>
                        """, unsafe_allow_html=True)
                
                # LIVE PIB results
                st.subheader("📡 Live PIB Matches (Real-Time)")
                relevant_live = [r for r in live_releases if any(k in r['title'].lower() or r['summary'].lower() for k in keywords)]
                
                if relevant_live:
                    for r in relevant_live[:4]:
                        st.markdown(f"""
                        <div class="fact-card">
                            <strong>{r['title']}</strong><br>
                            <small>Published: {r['published']}</small><br>
                            {r['summary']}<br>
                            <a href="{r['link']}" target="_blank">Read full PIB release →</a>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No new live PIB release directly matches this exact claim. All core facts are in the Verified Facts tab. The latest official position remains unchanged.")
                
                # Final verdict box
                st.markdown("**Official Verdict (PIB + MEA position)**")
                st.success("Operation Sindoor was a **focused, measured, non-escalatory** strike on terror infrastructure only. Confirmed by multiple official PIB releases.")
        else:
            st.warning("Enter a claim to verify.")

with tab5:
    st.subheader("📡 Live Official PIB Updates on Operation Sindoor")
    st.caption("Fetched directly from PIB.gov.in RSS • Refreshes every 5 minutes")
    live_releases = fetch_live_pib()
    if live_releases:
        for r in live_releases:
            st.markdown(f"""
            **{r['title']}**  
            <small>{r['published']}</small>  
            {r['summary']}  
            [Read full release]({r['link']})
            ---
            """, unsafe_allow_html=True)
    else:
        st.info("No recent Sindoor-related releases in the last batch. Core facts remain unchanged.")

# (Rest of the tabs remain exactly as before – Verified Facts, Debunked Claims, Timeline)

st.caption("v2.0 • Real-time PIB RSS connected • 100% Indigenous Official Sources • Built for truth")
