# 🤟 ISL Buddy — Indian Sign Language to Speech Assistant

[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?logo=streamlit)](https://streamlit.io)
[![MediaPipe](https://img.shields.io/badge/AI%20Engine-MediaPipe-0070F3?logo=google)](https://developers.google.com/mediapipe)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Bridging the communication gap for the deaf and hard-of-hearing community in India through real-time, browser-based AI.**

## 🌟 Problem Statement
Over 5 million deaf individuals in India rely on Indian Sign Language (ISL). However, most shopkeepers, doctors, and emergency responders do not understand ISL, creating a critical barrier to basic needs, healthcare, and safety. Existing solutions are often expensive, require heavy app downloads, or fail in low-light/rural conditions.

## 🚀 Solution: ISL Buddy
ISL Buddy is a lightweight, real-time web application that translates ISL fingerspelling and core vocabulary into spoken language (English, Hindi, Tamil, Telugu) directly in the browser. 

### ✨ Key Features
- **📷 Real-Time 21-Point Landmark Tracking:** Uses Google MediaPipe Hands for sub-millisecond skeletal tracking.
- **⏱️ 1.2s Temporal Stability Lock:** Prevents false positives by requiring a gesture to be held steadily before triggering speech.
- **🗣️ Multi-Language TTS:** Supports `en-IN`, `hi-IN`, `ta-IN`, and `te-IN` accents via the Web Speech API.
- **📜 Editable Sentence Builder:** Users can click and remove misclassified words before speaking, ensuring 100% user control and accessibility.
- **🔒 100% Privacy-First:** All computer vision processing happens **locally in the browser**. No video data is ever sent to a server.

## 🛠️ Tech Stack
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **AI/ML:** MediaPipe Hands (WebAssembly), Heuristic Geometry (with TensorFlow.js migration path)
- **Backend/UI:** Python, Streamlit
- **Audio:** Web Speech Synthesis API

## 🚀 Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/isl-buddy.git
   cd isl-buddy
