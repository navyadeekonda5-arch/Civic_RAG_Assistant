import streamlit as st
from ask import answer

st.title("Civic Services Q&A Assistant")
st.caption("Answers come only from the GHMC Citizen's Charter, with page numbers.")

q = st.text_input("Ask a question")
if q:
    with st.spinner("Searching the charter..."):
        text, metas = answer(q)
    st.write(text)
    if "couldn't find" not in text.lower():
        pages = ", ".join(str(p) for p in sorted({m["page"] for m in metas}))
        st.caption(f"Sources: pages {pages}")