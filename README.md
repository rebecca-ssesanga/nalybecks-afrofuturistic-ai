# 👑 Nalybecks Afrofuturistic AI (WIP)

**Wear Your Crown Beautifully — powered by AI**

Nalybecks Afrofuturistic AI is a **work-in-progress beauty-tech AI project** exploring how **computer vision and machine learning** can support **African-centered hairstyle try-on experiences**.

This repository contains an **early MVP**, focused on validating the technical pipeline and learning constraints before moving into generative models.

---

## 🚧 Project Status

⚠️ **Work in Progress (MVP stage)**
This is **not a final product**. The current implementation prioritizes:

* Learning
* Technical validation
* Iterative experimentation

---

## 🌍 Why this project?

Most beauty-tech AI systems struggle with:

* African hair textures
* Braids, twists, knots, and volume
* Cultural and aesthetic representation

This project asks:

> *What would hair try-on AI look like if African hair was the starting point, not an edge case?*

---

## ✨ Current Features (MVP)

* Web-based app deployed on **Streamlit**
* Accessible on **Android & iOS via the browser**
* User selfie upload
* Face landmark detection using **MediaPipe Face Mesh**
* Basic face-shape estimation (width, height, aspect ratio)
* Heuristic-based hairstyle recommendations
* 2D hairstyle try-on using transparent PNG overlays
* Image download & social sharing links
* WhatsApp booking call-to-action
* Basic analytics logging (admin-only)
* Dark, Afrofuturistic UI inspired by brand identity

---

## 🧠 Technical Overview

**Tech stack:**

* Python
* Streamlit
* OpenCV
* MediaPipe
* NumPy / PIL

**Pipeline (simplified):**

1. User uploads a selfie
2. Facial landmarks are detected
3. Face geometry is estimated
4. Rule-based logic recommends hairstyles
5. Hairstyle overlays are resized and composited using alpha blending

---

## ⚠️ Known Limitations (By Design)

The current MVP:

* Uses **classical computer vision**, not generative AI
* Applies **2D overlays** (no volumetric modeling)
* Does **not** model:

  * Hair texture dynamics
  * Lighting adaptation
  * Occlusion
  * Identity-preserving synthesis

These limitations are **intentional** and help define the next research phase.

---

## 🚀 Roadmap (Planned)

**Next phase:**

* Explore **GANs and Diffusion models**
* Focus on:

  * African hair texture synthesis
  * Volume & structure realism
  * Identity preservation
* Build or curate **African hair–focused datasets**
* Transition from overlays → generative try-on

---

## 📁 Repository Structure

```text
.
├── app.py                # Main Streamlit app
├── requirements.txt      # Python dependencies
├── hairstyles/           # Hairstyle PNG assets
├── data/                 # Analytics logs (CSV)
├── gallery/              # Saved results (optional)
├── logo.png              # Brand logo
└── README.md             # Project documentation
```

---

## 🛠 Running Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 🤝 Contributions & Feedback

This project is currently **research-driven and experimental**.
Feedback, discussions, and idea exchanges are welcome — especially around:

* Computer vision
* Generative models
* African-centered AI design

---

## 📌 Disclaimer

This project is an **exploratory MVP**.
It should not be considered production-ready or representative of final model performance.

---

## 👩🏽‍💻 Author

**Rebecca Ssesanga**
Machine Learning Engineer (Research-Oriented)
Computer Vision · Applied AI · African Innovation


