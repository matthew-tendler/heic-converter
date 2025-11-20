# HEIC Converter App

A Streamlit web application that converts HEIC/HEIF image files to PNG or JPG format with customizable quality settings.

## Features

- 📤 Upload multiple HEIC/HEIF files at once
- 🎨 Choose output format: PNG (lossless) or JPG (compressed)
- ⚙️ Quality settings for JPG: Highest Quality (95) or Lowest Quality (10)
- 📦 Automatic zip file creation with all converted images
- 💾 Customizable save location
- 📥 Direct download option

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

**Note for macOS users:** You may need to install additional system dependencies for `pillow-heif`:
```bash
brew install libheif
```

**Note for Linux users:** You may need:
```bash
sudo apt-get install libheif-dev  # Ubuntu/Debian
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. The app will open in your default web browser.

3. Use the sidebar to configure:
   - Output format (PNG or JPG)
   - Quality setting (for JPG only)
   - Save directory location

4. Upload one or more HEIC files using the file uploader.

5. Click "Convert Files" to start the conversion process.

6. Once complete, you can:
   - View the save location
   - Download the zip file directly from the app

## Requirements

- Python 3.8+
- Streamlit
- Pillow
- pillow-heif
- System libraries for HEIF support (libheif)

## Notes

- PNG format is lossless and doesn't use quality settings
- JPG format supports quality settings (Highest: 95, Lowest: 10)
- Transparent images will be converted to white background when saving as JPG
- The app automatically handles duplicate zip filenames by appending a counter

