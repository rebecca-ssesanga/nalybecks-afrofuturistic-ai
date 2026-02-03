# Nalybecks Afrofuturistic AI 👑

**Wear Your Crown Beautifully — powered by AI**

Nalybecks Afrofuturistic AI is a **work-in-progress web application** that blends African heritage, Afrofuturistic design, and artificial intelligence to allow users to virtually try on unique natural hairstyles.

Users can upload a selfie, preview Afrofuturistic hairstyles, receive AI-based recommendations, and share or book their preferred look via WhatsApp.

⚠️ This project is currently under active development and experimentation.

---

## 🌟 Features (Current MVP)

- 👤 User login (session-based)
- 📸 Upload a selfie image
- 💇🏾 Virtual hairstyle try-on (overlay)
- 🤖 AI hairstyle recommendation (face-shape logic)
- 🖼 Hairstyle categories:
  - Afro Crown  
  - Galactic Knots (Bantu Knots)  
  - Cornrows  
  - Twists  
  - Galactic Braids  
- ⬇️ Download generated hairstyle image
- 📤 Share to:
  - Instagram (manual upload flow)
  - Facebook
  - WhatsApp
  - Twitter/X
- 📲 WhatsApp booking button
- 🖼 User gallery (saved results)
- 📝 Feedback form
- 📊 Analytics dashboard (admin only)
- 🎨 Afrofuturistic dark & gold UI theme
- 📱 Mobile-friendly layout

---

## 🧠 Tech Stack

- **Frontend / App Framework:** Streamlit  
- **Computer Vision:** OpenCV  
- **Face Detection & Landmarks:** MediaPipe  
- **Image Processing:** Pillow, NumPy  
- **Data & Analytics:** Pandas, CSV storage  
- **Deployment:** Streamlit Cloud (planned/active)

---

## 📁 Project Structure

```text
nalybecks_afrofuturistic_ai/
│
├── app.py
├── requirements.txt
├── logo.png
├── hairstyles/
│   ├── afro_crown.png
│   ├── galactic_knots.png
│   ├── cornrows.png
│   ├── twists.png
│   └── futuristic_braided.png   # Galactic Braids
├── gallery/
└── data/
