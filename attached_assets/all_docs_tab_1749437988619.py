import streamlit as st
from utils.db import fetch_documents, delete_doc_by_id
import os
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
from serpapi import GoogleSearch
from utils.hf_ai_scoring import evaluate_quantum_maturity_hf

# 🔐 SerpAPI Key (cached search)
SERPAPI_KEY = "5b378023b71970f07637be85b74396be5abc04d54978a0e6eaa93ac378d5c266"

@st.cache_data(show_spinner=False)
def get_serpapi_results(title, num_results=3):
    params = {
        "engine": "google",
        "q": title,
        "num": num_results,
        "api_key": SERPAPI_KEY
    }
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        links = []
        for idx, result in enumerate(results.get("organic_results", [])[:num_results]):
            links.append(f"[{idx+1}⃣ {result.get('title')}]({result.get('link')})")
        return links if links else ["❌ No results found."]
    except Exception as e:
        return [f"❌ Search error: {e}"]

def get_badge(score):
    if score >= 80:
        return f"<span style='background-color:#2eb875;color:white;padding:2px 6px;border-radius:6px'>{score}</span>"
    elif score >= 50:
        return f"<span style='background-color:#ff0f27;color:black;padding:2px 6px;border-radius:6px'>{score}</span>"
    else:
        return f"<span style='background-color:#dc3545;color:white;padding:2px 6px;border-radius:6px'>{score}</span>"

def is_probably_quantum(content):
    if not content:
        return False
    keywords = ["quantum", "pqc", "post-quantum", "nist pqc", "qkd", "quantum-safe", "fips 203", "fips 204"]
    return any(kw in content.lower() for kw in keywords)

def render():
    st.markdown("<h2 style='text-align:center;'>📄 All Uploaded Documents</h2>", unsafe_allow_html=True)
    all_docs = fetch_documents(with_ids=True)
    if not all_docs:
        st.info("No documents found.")
        return

    doc_types = sorted(set(doc.get("doc_type", "Unknown") for doc in all_docs))
    years = sorted(set(doc.get("year") for doc in all_docs if isinstance(doc.get("year"), int)))
    sources = sorted(set(doc.get("source", "Unknown")[:30] for doc in all_docs if doc.get("source")))

    if "filters" not in st.session_state:
        st.session_state["filters"] = {
            "doc_type": "All",
            "year_range": (min(years), max(years)) if years else (2000, 2025),
            "source_multi": []
        }

    col1, col2, col3 = st.columns([3, 3, 4])
    with col1:
        st.session_state["filters"]["doc_type"] = st.selectbox("📂 Document Type", ["All"] + doc_types, index=(["All"] + doc_types).index(st.session_state["filters"]["doc_type"]))
    with col2:
        if years:
            st.session_state["filters"]["year_range"] = st.slider("📅 Year Range", min_value=min(years), max_value=max(years), value=st.session_state["filters"]["year_range"])
    with col3:
        st.session_state["filters"]["source_multi"] = st.multiselect("🌍 Filter by Source Prefix", sources, default=st.session_state["filters"]["source_multi"])

    if st.button("🩼 Clear Filters"):
        st.session_state["filters"] = {
            "doc_type": "All",
            "year_range": (min(years), max(years)) if years else (2000, 2025),
            "source_multi": []
        }
        st.experimental_rerun()

    f = st.session_state["filters"]
    docs = all_docs
    if f["doc_type"] != "All":
        docs = [d for d in docs if d.get("doc_type") == f["doc_type"]]
    if years:
        docs = [d for d in docs if isinstance(d.get("year"), int) and f["year_range"][0] <= d["year"] <= f["year_range"][1]]
    if f["source_multi"]:
        docs = [d for d in docs if any(d.get("source", "").startswith(s) for s in f["source_multi"])]

    compact = st.session_state.get("card_mode", False)
    compact_toggle = st.checkbox("📦 Compact Mode", value=compact)
    st.session_state["card_mode"] = compact_toggle

    per_page = 10
    page = st.session_state.get("doc_page", 0)
    total_pages = len(docs) // per_page + (1 if len(docs) % per_page else 0)

    if total_pages > 1:
        col1, col2, col3 = st.columns((1, 2, 1))
        with col1:
            if st.button("⬅️ Prev") and page > 0:
                st.session_state["doc_page"] = page - 1
                st.experimental_rerun()
        with col3:
            if st.button("Next ➡️") and page < total_pages - 1:
                st.session_state["doc_page"] = page + 1
                st.experimental_rerun()

    start = page * per_page
    end = start + per_page
    page_docs = docs[start:end]

    with st.expander("🩷 What do these scores mean?"):
        st.markdown("""
        **🧐 Ethics-Based Scores**
        - `AI-Ethics`: Policy alignment with responsible AI principles (e.g., fairness, transparency)
        - `Q-Ethics`: Quantum governance ethics — inclusion of risk mitigation, safety, or oversight

        **🔐 Maturity-Based Scores**
        - `Cybersecurity Maturity`: Implementation of security frameworks, controls, and resilience plans
        - `Quantum Maturity`: Readiness for quantum threats (e.g., crypto-agility, PQC controls)
        """)

    cols = st.columns(4 if compact_toggle else 3)
    for i, doc in enumerate(page_docs):
        with cols[i % len(cols)]:
            with st.container():
                st.markdown("""
                    <div style='border:1px solid #ddd;padding:14px;border-radius:10px;margin:6px;
                    box-shadow:2px 4px rgba(0,0,0,0.05); transition:0.3s'>
                """, unsafe_allow_html=True)

                st.markdown(f"**📜 {doc['title'][:60]}**", unsafe_allow_html=True)
                st.markdown(f"<small>{doc['doc_type']} · {doc.get('year','N/A')}</small>", unsafe_allow_html=True)

                st.markdown(f"AI-Ethics: {get_badge(doc.get('ethics_ai',0))}", unsafe_allow_html=True)
                st.markdown(f"Q-Ethics: {get_badge(doc.get('ethics_q',0))}", unsafe_allow_html=True)
                st.markdown(f"Cybersecurity Maturity: {get_badge(doc.get('cyber_score',0))}", unsafe_allow_html=True)

                text_blob = doc.get("text") or doc.get("content")
                hf_result = evaluate_quantum_maturity_hf(text_blob) if text_blob else {}
                quantum_score = hf_result.get("patent_score", 0)

                if is_probably_quantum(text_blob) and quantum_score > 0:
                    st.markdown(f"Quantum Maturity: {get_badge(quantum_score)}", unsafe_allow_html=True)
                else:
                    st.markdown(f"Quantum Maturity: <span style='color:#888'>N/A</span>", unsafe_allow_html=True)

                with st.expander("📖 Full Preview"):
                    st.markdown(f"**Summary:** {doc.get('summary','')[:1000]}", unsafe_allow_html=True)

                with st.expander("🔎 Why this Quantum Score?"):
                    st.markdown("This score is based on AI evaluation of the document content using semantic classification.")
                    traits = hf_result.get("traits", {})
                    st.markdown(f"- Implementation Plan: {'✅' if traits.get('implementation_plan') else '❌'}")
                    st.markdown(f"- Standards Reference: {'✅' if traits.get('standards_reference') else '❌'}")
                    st.markdown(f"- Roadmap/Timeline: {'✅' if traits.get('roadmap_timeline') else '❌'}")

                if doc.get("source") and doc["source"].startswith("http"):
                    st.markdown(f"[🌐 Open Source]({doc['source']})", unsafe_allow_html=True)
                else:
                    st.markdown("ℹ️ No direct source available.")
                    with st.expander("🔎 Top 3 Google Search Results"):
                        for result in get_serpapi_results(doc.get("title", "")):
                            st.markdown(result, unsafe_allow_html=True)

                with st.expander("⚙️ Manage Document"):
                    confirm_key = f"confirm_{doc['id']}"
                    confirm_delete = st.checkbox("Confirm delete", key=confirm_key)
                    if confirm_delete:
                        if st.button("❌ Delete Permanently", key=f"del_{doc['id']}"):
                            delete_doc_by_id(doc["id"])
                            st.success(f"Deleted: {doc['title']}")
                            st.experimental_rerun()
                    else:
                        st.markdown("*Check the box above to enable deletion.*")

                st.markdown("</div>", unsafe_allow_html=True)

