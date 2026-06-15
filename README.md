# ui2code

AI-powered platform for converting UI screenshots into frontend code.

ui2code analyzes interface screenshots, understands layouts, detects components, extracts text, and generates frontend code automatically. The goal is to build an intelligent design-to-code system capable of producing production-ready HTML, CSS, JavaScript, React, and Tailwind code from a single image.

## Features
 
* Screenshot Upload
* UI Layout Analysis
* Component Detection
* OCR Text Extraction
* HTML Generation
* CSS Generation
* JavaScript Generation
* Live Code Preview
* AI-Powered Layout Intelligence
* Design-to-Code Pipeline

## Vision

Modern frontend development spends significant time converting designs into code. ui2code aims to automate this process using Computer Vision, OCR, Layout Understanding, and AI-powered Code Generation.

A user uploads a screenshot of a website, dashboard, mobile application, or wireframe, and ui2code generates structured frontend code automatically.

## Technology Stack

### Frontend

* HTML
* CSS
* JavaScript

### Backend

* Python
* Flask

### Computer Vision

* OpenCV
* EasyOCR

### Planned AI Stack

* YOLOv8
* LayoutParser
* Detectron2
* Transformers
* Vision Language Models

## Project Structure

```text
ui2code/
│
├── backend/
│   ├── app.py
│   ├── detector.py
│   ├── layout_engine.py
│   ├── code_generator.py
│   ├── uploads/
│   ├── templates/
│   └── static/
│
├── requirements.txt
├── .gitignore
└── .env.example
```

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/ui2code.git
cd ui2code
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

Mac/Linux

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
cd backend
python app.py
```

Application runs at:

```text
http://127.0.0.1:5000
```
## Developed by

Smriti Prajapati
