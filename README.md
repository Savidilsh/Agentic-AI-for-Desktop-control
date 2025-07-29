# Desktop Agent Project

A collection of AI-powered desktop automation agents that can control your computer through natural language commands.

## 📋 Project Overview

This project contains two main agents:

1. **`desktop_agent.py`** - Rule-based desktop agent (no LLM required)
2. **`llm_agent.py`** - LLM-powered desktop agent using Ollama

Both agents can:
- Open applications (calculator, browser, notepad, etc.)
- Perform web searches
- Automate calculator operations
- Control browser navigation and scrolling
- Execute keyboard and mouse operations

## 🛠️ Technologies Used

### Desktop Agent (desktop_agent.py)
- **Python 3.7+** - Programming language
- **PyAutoGUI** - Screen automation (mouse, keyboard, screenshots)
- **PyTesseract** - Optical Character Recognition (OCR)
- **Tesseract OCR** - Text extraction from images
- **OpenCV** - Computer vision operations
- **Pillow (PIL)** - Image processing
- **NumPy** - Array operations

### LLM Agent (llm_agent.py)
- **All above dependencies** PLUS:
- **Ollama** - Local LLM inference
- **Llama 3.2** - Language model for decision making
- **JSON parsing** - For LLM response handling
- **Regular expressions** - Text processing

## 📦 Installation

### Prerequisites
1. **Python 3.7 or higher**
2. **Windows 10/11** (tested on Windows)

### Step 1: Install Python Dependencies

```bash
# Use py -m pip if pip is not in PATH
py -m pip install pyautogui pytesseract pillow numpy

# For LLM agent, also install:
py -m pip install ollama
```

### Step 2: Install Tesseract OCR

**Option A: Using winget (Recommended)**
```bash
winget install UB-Mannheim.TesseractOCR
```

**Option B: Manual Installation**
1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install `tesseract-ocr-w64-setup-5.5.0.20241111.exe`
3. Make sure it's installed to: `C:\Program Files\Tesseract-OCR\`

### Step 3: For LLM Agent - Install Ollama

**Option A: Direct Download**
1. Go to: https://ollama.ai/download/windows
2. Download and install Ollama

**Option B: Using winget**
```bash
winget install Ollama.Ollama
```

### Step 4: Download Language Model (LLM Agent Only)

```bash
# Pull Llama 3.2 model (this may take several minutes)
ollama pull llama3.2

# Test if it works
ollama run llama3.2
# Type "hello" and press Enter, then type "/bye" to exit
```

## 🚀 Usage

### Running the Rule-Based Agent (desktop_agent.py)

```bash
py desktop_agent.py
```

**Example commands:**
- `open calculator`
- `open browser`
- `search for python tutorials`
- `open notepad`

### Running the LLM-Powered Agent (llm_agent.py)

```bash
py llm_agent.py
```

**Example commands:**
- `open calculator and add 1 and 2`
- `search for blue car videos and scroll the webpage`
- `open chrome browser and search for AI news`
- `add 5 and 3` (when calculator is open)

## ⚡ Features Comparison

| Feature | desktop_agent.py | llm_agent.py |
|---------|------------------|--------------|
| Rule-based logic | ✅ | ✅ (fallback) |
| LLM reasoning | ❌ | ✅ |
| Calculator operations | Basic | Advanced |
| Web browsing | Basic | Advanced |
| Natural language | Limited | Extensive |
| Complex commands | ❌ | ✅ |
| Offline capability | ✅ | ✅ (with Ollama) |
| Setup complexity | Simple | Moderate |

## 🔧 Configuration

### Tesseract Path
If Tesseract is installed in a different location, update this line in both files:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### LLM Model
To use a different Ollama model, change this line in `llm_agent.py`:
```python
response = ollama.chat(model='llama3.2', messages=[...])
```

Available models: `llama3.2`, `llama2`, `codellama`, etc.

## 🛡️ Safety Features

- **PyAutoGUI Failsafe**: Move mouse to top-left corner to stop execution
- **Configurable delays**: Prevents system overload
- **Error handling**: Graceful fallbacks when operations fail
- **Local execution**: No data sent to external services (when using Ollama)

## 🐛 Troubleshooting

### Common Issues

**1. `'python' is not recognized`**
- Use `py` instead of `python`
- Or add Python to your system PATH

**2. `'tesseract' is not recognized`**
- Tesseract not installed or not in PATH
- Check installation path and update code if needed

**3. `'ollama' is not recognized`**
- Restart command prompt after Ollama installation
- Check if Ollama service is running

**4. PyAutoGUI import error**
- Update PyAutoGUI: `py -m pip install --upgrade pyautogui`
- Install missing dependencies

**5. OCR not detecting text**
- Ensure good screen contrast
- Try different applications
- Check Tesseract installation

### Testing Commands

```bash
# Test Python packages
py -c "import pyautogui; print('PyAutoGUI works!')"
py -c "import pytesseract; print('PyTesseract works!')"
py -c "import ollama; print('Ollama works!')"  # For LLM agent

# Test Tesseract
"C:\Program Files\Tesseract-OCR\tesseract.exe" --version

# Test Ollama
ollama --version
ollama list
```

## 📈 Future Enhancements

- Voice command integration
- Multi-monitor support
- Advanced computer vision
- Web automation with Selenium
- Mobile device control
- Plugin system for custom actions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## ⚠️ Disclaimer

This software is for educational and automation purposes. Use responsibly and ensure you comply with the terms of service of applications you're automating. The authors are not responsible for any misuse or damage caused by this software.

---

**Happy Automating!** 🤖✨
