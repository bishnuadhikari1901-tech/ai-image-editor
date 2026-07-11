import streamlit as st
import requests
import io
from PIL import Image

# 1. Page Settings
st.set_page_config(page_title="AI Image Transformer", layout="centered")
st.title("🎨 Free AI Image-to-Image Converter")
st.write("Upload an image, give a text prompt, and watch the AI redesign it!")

# 2. Get API Token securely from settings
HF_TOKEN = st.secrets.get("HF_TOKEN", "")

# Using an open-source image editing model
API_URL = "https://api-inference.huggingface.co/models/stable-diffusion-v1-5/stable-diffusion-v1-5"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# 3. Sidebar adjustments
st.sidebar.header("AI Control Panel")
strength = st.sidebar.slider("Change Intensity", min_value=0.1, max_value=0.9, value=0.6, step=0.05)
st.sidebar.caption("Higher changes the image drastically. Lower keeps it close to original structure.")

# 4. Image upload layout
uploaded_file = st.file_uploader("Step 1: Upload your starting image (JPG/PNG)", type=["jpg", "jpeg", "png"])
prompt = st.text_input("Step 2: Describe what the AI should change or add", placeholder="e.g., Make it look like a futuristic cyberpunk city skyline")

if uploaded_file is not None:
    init_image = Image.open(uploaded_file)
    st.image(init_image, caption="Original Image", use_container_width=True)
    
    # 5. Execution button
    if st.button("✨ Transform Image"):
        if not prompt:
            st.error("Please provide a text prompt first!")
        elif not HF_TOKEN:
            st.error("API Key missing! Please add HF_TOKEN to your Streamlit Advanced Settings.")
        else:
            with st.spinner("The AI is processing your image... (may take 15-30 seconds)"):
                try:
                    # Convert image file to bytes payload
                    img_byte_arr = io.BytesIO()
                    init_image.save(img_byte_arr, format=init_image.format)
                    img_bytes = img_byte_arr.getvalue()

                    payload = {
                        "inputs": img_bytes,
                        "parameters": {"prompt": prompt, "strength": strength}
                    }

                    # Ask Hugging Face to process the image
                    response = requests.post(API_URL, headers=headers, json=payload)
                    
                    if response.status_code == 200:
                        output_image = Image.open(io.BytesIO(response.content))
                        st.success("All done!")
                        st.image(output_image, caption="AI Transformed Image", use_container_width=True)
                    else:
                        st.error(f"AI Server busy or error. Try again in a few seconds. Status: {response.status_code}")
                except Exception as e:
                    st.error(f"Error: {e}")
