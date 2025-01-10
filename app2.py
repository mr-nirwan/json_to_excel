import streamlit as st
from streamlit_option_menu import option_menu
import Modules.json_to_excel as json_to_excel
import Modules.file_parser as file_parser



st.set_page_config(page_title="AccuAI", page_icon="app-indicator", layout="wide")
# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        
local_css("style/style.css")

def footer():
    st.markdown("---")
    col1, col2 = st.columns([5, 5])

    with col1:
        st.markdown("Copyright © Accu AI 2025", unsafe_allow_html=True)

    with col2:
        st.empty()
        
st.markdown('<div class="fullScreenDiv">', unsafe_allow_html=True)
with st.container():
    left_column, right_column = st.columns((2, 7))
    
    with left_column:
        selected = option_menu(
            menu_title=None,
            options=["JSON to Excel", "File Parser"],             
            icons=['house', 'person-circle', 'file-earmark-word-fill', 'person-lines-fill', 'shield-check', 'translate', 'envelope', 'file-lock'], 
            menu_icon="cast", 
            default_index=0, 
            orientation="vertical"
        )


    with right_column:
        if selected == "JSON to Excel":
            json_to_excel.main()
        if selected == "File Parser":
            file_parser.main()


footer()
st.markdown('</div>', unsafe_allow_html=True)