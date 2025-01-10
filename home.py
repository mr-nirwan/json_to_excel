import requests
import streamlit as st
from streamlit_lottie import st_lottie
from PIL import Image
from io import BytesIO
import base64

def app():  # <-- Add this function
 
    def load_lottieurl(url):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
        
    # Function to convert PIL image to base64
    def pil_to_base64(img):
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()    

    # Use local CSS
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            
    local_css("style/style.css")

    # ---- LOAD ASSETS ----
    lottie_AI = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_y7VH7yWmJE.json")
    lottie_rocket = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_5py5ru1u.json")
    img_linkedin = Image.open("images/linkedin.png")
    
    # Convert PIL image to base64
    img_b64 = pil_to_base64(img_linkedin)

    # ---- HEADER SECTION ----
    with st.container():
        left_column, right_column = st.columns((5, 1))
        with left_column:
            st.markdown("<h1><span style='color: #F24903;'>Accu</span><span style='color: #0067B9;'>AI</span></h1>", unsafe_allow_html=True)
            st.write("Unlock the power of Accu AI Tools: Smarter and Accurate!")
            st.write("EFFICIENCY · ACCURACY · PRODUCTIVITY")
            st.info("Click on Account Button to Login and access the Accu AI Tools")
        with right_column:
            st_lottie(lottie_AI, height=170, key="Rocket")  

    # ---- WHAT I DO ----
    with st.container():
        st.write("---")
        left_column, right_column = st.columns((3, 1))
        with left_column:
            #st.write("##")
            st.empty()
        with right_column:
            st_lottie(lottie_rocket, height=200, key="AI")
            
    with st.container():
        left_column, right_column = st.columns((1, 5))
        with left_column:
            # Embed base64 image inside HTML and make it clickable
            st.markdown(
                f'<a href="https://www.linkedin.com/company/accuscript-consultancy-pvt-ltd/mycompany/"><img src="data:image/png;base64,{img_b64}" alt="LinkedIn" style="width:32px;height:32px;"></a>',
                unsafe_allow_html=True,)  
        with right_column: 
            st.empty()