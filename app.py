import streamlit as st
import zipfile
import os
import tempfile
from pathlib import Path
from PIL import Image
from pillow_heif import register_heif_opener
import io

# Register HEIF opener with Pillow
register_heif_opener()

st.set_page_config(page_title="HEIC Converter", page_icon="🖼️", layout="wide")

st.title("🖼️ HEIC to PNG/JPG Converter")
st.markdown("Upload HEIC files and convert them to PNG or JPG format with customizable quality settings.")

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Conversion Settings")
    
    # Output format selection
    output_format = st.radio(
        "Output Format",
        ["PNG", "JPG"],
        help="PNG is lossless, JPG is compressed"
    )
    
    # Quality setting (only for JPG)
    if output_format == "JPG":
        quality_setting = st.radio(
            "Quality",
            ["Highest Quality", "Lowest Quality"],
            help="Highest Quality = 95, Lowest Quality = 10"
        )
        quality = 95 if quality_setting == "Highest Quality" else 10
    else:
        quality = None
        st.info("PNG format is lossless and doesn't use quality settings.")
    
    st.divider()
    st.markdown("### 📁 Save Location")
    save_location = st.text_input(
        "Save Directory",
        value=os.path.expanduser("~/Downloads"),
        help="Directory where the zip file will be saved"
    )

# Main content area
uploaded_files = st.file_uploader(
    "Select HEIC files to convert",
    type=["heic", "heif"],
    accept_multiple_files=True,
    help="You can select multiple files at once"
)

if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} file(s) selected")
    
    # Display selected files
    with st.expander("📋 Selected Files"):
        for i, file in enumerate(uploaded_files, 1):
            st.text(f"{i}. {file.name} ({file.size / 1024:.2f} KB)")

    # Convert button
    if st.button("🔄 Convert Files", type="primary", use_container_width=True):
        if not save_location or not os.path.exists(save_location):
            st.error(f"❌ Invalid save location: {save_location}")
            st.info("Please enter a valid directory path in the sidebar.")
        else:
            with st.spinner("Converting files... This may take a moment."):
                # Create temporary directory for converted files
                with tempfile.TemporaryDirectory() as temp_dir:
                    converted_files = []
                    errors = []
                    
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for idx, uploaded_file in enumerate(uploaded_files):
                        try:
                            # Update progress
                            progress = (idx + 1) / len(uploaded_files)
                            progress_bar.progress(progress)
                            status_text.text(f"Processing {uploaded_file.name} ({idx + 1}/{len(uploaded_files)})...")
                            
                            # Read HEIC file
                            image_data = uploaded_file.read()
                            
                            # Open HEIC image
                            image = Image.open(io.BytesIO(image_data))
                            
                            # Convert to RGB if necessary (for JPG)
                            if output_format == "JPG" and image.mode in ("RGBA", "LA", "P"):
                                # Create white background for transparent images
                                rgb_image = Image.new("RGB", image.size, (255, 255, 255))
                                if image.mode == "P":
                                    image = image.convert("RGBA")
                                rgb_image.paste(image, mask=image.split()[-1] if image.mode == "RGBA" else None)
                                image = rgb_image
                            elif output_format == "JPG":
                                image = image.convert("RGB")
                            
                            # Generate output filename
                            base_name = Path(uploaded_file.name).stem
                            extension = "png" if output_format == "PNG" else "jpg"
                            output_filename = f"{base_name}.{extension}"
                            output_path = os.path.join(temp_dir, output_filename)
                            
                            # Save converted image
                            if output_format == "PNG":
                                image.save(output_path, format="PNG", optimize=True)
                            else:
                                image.save(output_path, format="JPEG", quality=quality, optimize=True)
                            
                            converted_files.append((output_path, output_filename))
                            
                        except Exception as e:
                            errors.append(f"{uploaded_file.name}: {str(e)}")
                            st.warning(f"⚠️ Failed to convert {uploaded_file.name}: {str(e)}")
                    
                    progress_bar.progress(1.0)
                    status_text.text("Creating zip file...")
                    
                    if converted_files:
                        # Create zip file
                        zip_filename = f"heic_converted_{output_format.lower()}.zip"
                        zip_path = os.path.join(save_location, zip_filename)
                        
                        # Handle duplicate filenames
                        counter = 1
                        while os.path.exists(zip_path):
                            zip_filename = f"heic_converted_{output_format.lower()}_{counter}.zip"
                            zip_path = os.path.join(save_location, zip_filename)
                            counter += 1
                        
                        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                            for file_path, filename in converted_files:
                                zipf.write(file_path, filename)
                        
                        # Success message
                        st.success(f"✅ Conversion complete! {len(converted_files)} file(s) converted.")
                        st.info(f"📦 Zip file saved to: `{zip_path}`")
                        
                        # Display file size
                        zip_size = os.path.getsize(zip_path) / (1024 * 1024)  # MB
                        st.metric("Zip File Size", f"{zip_size:.2f} MB")
                        
                        # Download button
                        with open(zip_path, 'rb') as f:
                            st.download_button(
                                label="📥 Download Zip File",
                                data=f.read(),
                                file_name=zip_filename,
                                mime="application/zip",
                                use_container_width=True
                            )
                    else:
                        st.error("❌ No files were successfully converted.")
                    
                    if errors:
                        with st.expander("⚠️ Errors"):
                            for error in errors:
                                st.text(error)

else:
    st.info("👆 Please upload one or more HEIC files to get started.")

# Footer
st.divider()
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        <small>HEIC Converter App | Supports .heic and .heif files</small>
    </div>
    """,
    unsafe_allow_html=True
)

