import streamlit as st
import io
import uuid # Generates a totally random, unique name for every image file
from supabase import create_client, Client

# 1. Connect securely to Supabase using settings keys
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "")

# Initialize the Supabase program client helper
if SUPABASE_URL and SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    supabase = None

# 2. Main File Uploader Widget element
uploaded_file = st.file_uploader("Upload your starting image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None and supabase is not None:
    # Read raw image upload bytes
    file_bytes = uploaded_file.getvalue()
    
    # Check if user clicked a trigger save button
    if st.button("💾 Save Permanently to Cloud Vault"):
        with st.spinner("Uploading to Supabase cloud storage..."):
            try:
                # Generate a unique file pathway like: uploads/abc-123-xyz.png
                file_extension = uploaded_file.name.split(".")[-1]
                unique_filename = f"uploads/{uuid.uuid4()}.{file_extension}"
                
                # Execute upload stream right into your storage bucket named 'user-images'
                response = supabase.storage.from_("user-images").upload(
                    path=unique_filename,
                    file=file_bytes,
                    file_options={"content-type": uploaded_file.type}
                )
                
                # Extract the permanent live public web asset link URL
                public_url = supabase.storage.from_("user-images").get_public_url(unique_filename)
                
                st.success("Successfully saved to the cloud forever!")
                st.info(f"Permanent Cloud URL: {public_url}")
                
            except Exception as e:
                st.error(f"Cloud Upload Failed: {e}")
