# 🏗️ PyStructure

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Gemini API](https://img.shields.io/badge/Powered%20by-Google%20Gemini-orange.svg)](https://ai.google.dev/)
[![GUI](https://img.shields.io/badge/GUI-Tkinter-lightblue.svg)](https://docs.python.org/3/library/tkinter.html)

> 🚀 **Dual-Mode Directory Structure Generator** - Create project structures from images using AI or parse text-based directory trees. Two powerful methods, one seamless experience.

![dev-starter Chat Demo](https://raw.githubusercontent.com/LMLK-seal/PyStructure/refs/heads/main/PyStructure.jpg)

## 🌟 Overview

PyStructure is a versatile Python desktop application that offers **two distinct modes** for generating directory structures:

1. **🤖 AI Mode**: Upload directory tree images and let Google Gemini Vision AI recreate the structure
2. **📝 Text Mode**: Paste text-based directory trees and parse them into real folder structures

Perfect for developers, project managers, and anyone who needs to quickly replicate project structures from documentation, screenshots, or text representations.

## ✨ Features

### 🖼️ **Image Mode (AI-Powered)**
- Upload screenshots of directory trees from any source
- Powered by Google Gemini 1.5 Flash for accurate structure recognition
- Supports PNG, JPG, JPEG, BMP, and WebP formats
- Automatically ignores tree-drawing characters and comments

### 📄 **Text Mode (Parser-Based)**
- Paste directory tree text directly into the application
- Intelligent parsing of indented structures
- Supports various tree formats and indentation styles
- Works offline - no API required

### 🎯 **Common Features**
- **Tabbed Interface**: Switch seamlessly between modes
- **Real-time Logging**: Monitor the creation process step-by-step
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Smart Path Handling**: Automatic parent directory creation
- **Error Recovery**: Comprehensive error handling and user feedback

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- For Image Mode: Google Gemini API key ([Get one here](https://ai.google.dev/))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/LMLK-seal/PyStructure.git
   cd PyStructure
   ```

2. **Install dependencies**
   ```bash
   # For both modes
   pip install tkinter

   # For Image Mode (optional)
   pip install google-generativeai pillow
   ```

3. **Run the application**
   ```bash
   python PyStructure.py
   ```

## 📖 How to Use

### 🖼️ **Image Mode**
1. **Switch to "From Image (AI)" tab**
2. **🔑 Enter API Key**: Input your Google Gemini API key
3. **📸 Select Image**: Choose an image containing a directory tree
4. **📁 Choose Destination**: Select where you want the structure created
5. **▶️ Generate**: Click "Generate Structure" and watch the AI work!

### 📝 **Text Mode**
1. **Switch to "From Text" tab**
2. **📋 Paste Structure**: Copy and paste your directory tree text
3. **📁 Choose Destination**: Select the destination folder
4. **▶️ Generate**: Click "Generate Structure" - no API needed!

## 🎯 Example Usage

### Image/Text Mode Input:
```
project/
├── src/
│   ├── main.py
│   ├── utils/
│   │   └── helpers.py
│   └── models/
│       └── __init__.py
├── tests/
│   ├── test_main.py
│   └── conftest.py
├── docs/
│   └── README.md
├── .gitignore
└── requirements.txt
```

### Generated Structure:
Both modes create the exact same real directory structure in your chosen destination folder!

## 🛠️ Technical Details

### **Architecture**
- **GUI Framework**: Tkinter with modern ttk styling
- **Threading**: Background processing for responsive UI
- **Path Handling**: Cross-platform compatibility with pathlib
- **Error Handling**: Graceful degradation and user-friendly messages

### **AI Integration**
- **Model**: Google Gemini 1.5 Flash Latest
- **Vision Processing**: PIL (Pillow) for image handling
- **Smart Parsing**: Ignores visual artifacts and focuses on structure

### **Text Parsing Engine**
- **Intelligent Indentation**: Auto-detects indentation patterns
- **Flexible Format Support**: Handles various tree drawing styles
- **Comment Recognition**: Automatically filters out comments
- **Robust Error Recovery**: Continues processing even with malformed input

## 📋 Requirements

### **Core Requirements**
```txt
# Built-in Python libraries
tkinter (included with Python)
pathlib (included with Python)
threading (included with Python)
```

### **Optional Requirements (Image Mode)**
```txt
google-generativeai>=0.3.0
pillow>=9.0.0
```

## 🎨 Interface Screenshots

### Dual Tab Interface
- **Image Mode Tab**: Clean interface for AI-powered generation
- **Text Mode Tab**: Simple text area for direct input
- **Unified Controls**: Shared destination selection and generation controls
- **Real-time Logging**: Live feedback during structure creation

## 🤝 Contributing

Contributions are welcome! This project is perfect for adding new features like:

- **New Input Formats**: Support for JSON, YAML, or XML structure definitions
- **Export Options**: Save structures as templates
- **Batch Processing**: Process multiple images or text files
- **Custom Templates**: Pre-defined project structure templates

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔧 Troubleshooting

### **Common Issues**

**"Libraries for 'From Image' mode not found"**
```bash
pip install google-generativeai pillow
```
*Note: Text mode will still work without these libraries*

**"API_KEY_INVALID error"**
- Verify your Gemini API key is correct
- Check API key permissions and quota
- Ensure the key is properly entered (no extra spaces)

**"The parser did not find any valid paths"**
- Check your text formatting and indentation
- Ensure folder names end with `/`
- Try using consistent indentation (spaces or tabs, not mixed)

**"Permission denied" when creating files**
- Ensure the destination folder is writable
- Run with appropriate permissions if needed
- Check if antivirus software is blocking file creation

### **Performance Tips**
- **Large Structures**: For very large directory trees, consider breaking them into smaller chunks
- **Image Quality**: Use clear, high-contrast images for better AI recognition
- **Text Formatting**: Consistent indentation improves parsing accuracy

## 🌟 Advanced Features

### **Supported Text Formats**
- Standard tree format with `├──`, `└──`, `│`
- Simple indented lists
- Mixed indentation styles
- Comments (automatically ignored)

### **Smart Detection**
- **Auto-indentation**: Automatically detects indentation size
- **Path Normalization**: Converts all paths to forward slashes
- **Duplicate Handling**: Safely handles existing files/folders

## 🙏 Acknowledgments

- **Google AI** for the powerful Gemini Vision API
- **Python Community** for excellent standard libraries
- **Open Source Contributors** who help improve this tool
- **Tkinter Team** for the robust GUI framework

## 📞 Support & Community

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/LMLK-seal/PyStructure/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/LMLK-seal/PyStructure/discussions)
- 🌟 **Show Support**: Star this repository if you find it helpful!

---

<div align="center">

**⭐ Star this repository if PyStructure helps streamline your development workflow!**

Made with ❤️ by [LMLK-seal](https://github.com/LMLK-seal)

</div>
