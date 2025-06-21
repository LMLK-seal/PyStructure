# 📁 PyStructure

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Gemini API](https://img.shields.io/badge/Powered%20by-Google%20Gemini-orange.svg)](https://ai.google.dev/)

> 🤖 **AI-Powered Directory Structure Creator** - Transform directory tree screenshots into actual folder structures using Google's Gemini Vision AI.

## 🌟 Overview

PyStructure is a Python desktop application that uses Google's Gemini 1.5 Flash model to analyze images of directory trees and automatically recreate the exact folder and file structure on your local filesystem. Perfect for developers who want to quickly replicate project structures from documentation, tutorials, or screenshots.

## ✨ Features

- 🖼️ **Image Analysis**: Upload screenshots of directory trees from any source
- 🧠 **AI-Powered**: Uses Google Gemini 1.5 Flash for accurate structure recognition
- 📂 **Automatic Creation**: Creates folders and files with proper hierarchy
- 🖥️ **User-Friendly GUI**: Clean, modern Tkinter interface
- 📝 **Real-time Logging**: See the creation process in real-time
- 🔒 **Secure**: API key handling with masked input
- 🎯 **Accurate**: Ignores tree-drawing characters and comments automatically

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Google Gemini API key ([Get one here](https://ai.google.dev/))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/LMLK-Seal/PyStructure.git
   cd PyStructure
   ```

2. **Install dependencies**
   ```bash
   pip install google-generativeai pillow
   ```

3. **Run the application**
   ```bash
   python PyStructure.py
   ```

## 📖 How to Use

1. **🔑 Enter API Key**: Input your Google Gemini API key
2. **🖼️ Select Image**: Choose an image containing a directory tree structure
3. **📁 Choose Destination**: Select where you want the structure created
4. **▶️ Generate**: Click "Generate Structure" and watch the magic happen!

### Supported Image Formats
- PNG, JPG, JPEG, BMP, WebP

## 🎯 Example Usage

**Input Image:**
```
project/
├── src/
│   ├── main.py
│   └── utils/
│       └── helpers.py
├── tests/
│   └── test_main.py
├── docs/
│   └── README.md
└── requirements.txt
```

**Generated Structure:**
```
your-destination-folder/
├── project/
│   ├── src/
│   │   ├── main.py
│   │   └── utils/
│   │       └── helpers.py
│   ├── tests/
│   │   └── test_main.py
│   ├── docs/
│   │   └── README.md
│   └── requirements.txt
```

## 🛠️ Technical Details

- **AI Model**: Google Gemini 1.5 Flash Latest
- **GUI Framework**: Tkinter with ttk styling
- **Image Processing**: PIL (Pillow)
- **Threading**: Background processing to maintain UI responsiveness
- **Path Handling**: Cross-platform compatible using pathlib

## 📋 Requirements

```txt
google-generativeai>=0.3.0
pillow>=9.0.0
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔧 Troubleshooting

### Common Issues

**"google-generativeai not installed"**
```bash
pip install google-generativeai
```

**"API_KEY_INVALID error"**
- Verify your Gemini API key is correct
- Check if your API key has proper permissions
- Ensure you have credits/quota available

**"Image not recognized properly"**
- Ensure the image is clear and readable
- Try images with standard directory tree formatting
- Avoid images with too much background noise

## 🙏 Acknowledgments

- Google AI for the powerful Gemini Vision API
- The Python community for excellent libraries
- Contributors and users who help improve this tool

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

Made with ❤️ 

</div>
