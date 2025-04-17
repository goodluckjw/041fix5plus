
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from utils.xml_parser import parse_law_xml

st.title("부칙 개정 도우미")
st.write("법령 본문 중 검색어를 포함하는 조문을 찾아줍니다.")

query = st.text_input("🔍 찾을 단어", key="search_word")

if st.button("법률 검색"):
    if not query:
        st.warning("검색어를 입력하세요.")
    else:
        st.info(f"🔍 '{query}'을(를) 포함하는 조문을 검색 중입니다...")
        xml_files = [f for f in os.listdir("./data") if f.endswith(".xml")]
        found = False
        for file in xml_files:
            law_path = os.path.join("data", file)
            try:
                matched = parse_law_xml(law_path, query)
                if matched:
                    found = True
                    with st.expander(matched["법령명"]):
                        st.markdown(f"[📘 원문 보기]({matched['원문링크']})", unsafe_allow_html=True)
                        for 조문 in matched["조문들"]:
                            st.markdown(조문, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"⚠️ 파일 로드 중 오류 발생: {e}")
        if not found:
            st.warning("해당 검색어를 포함한 조문이 없습니다.")
