import streamlit as st
import cv2
import numpy as np
from PIL import Image
from mediapipe import solutions as mp
import io, os, time, csv
import pandas as pd
from datetime import datetime
from urllib.parse import quote_plus

# =================================================
# CONFIG
# =================================================
WHATSAPP_NUMBER = "256775668530"  # 0775668530
APP_URL = "https://your-app-name.streamlit.app"  # update after deploy

st.set_page_config(
    page_title="Nalybecks Afrofuturistic AI",
    page_icon="logo.png",
    layout="centered"
)

# =================================================
# BRAND COLORS (FROM LOGO)
# =================================================
PRIMARY_PINK = "#E6007E"
SECONDARY_PURPLE = "#B266FF"
DARK_BG = "#0B0B0F"
CARD_BG = "#161622"
TEXT_LIGHT = "#EDEDED"

# =================================================
# GLOBAL CSS
# =================================================
st.markdown(f"""
<style>
body {{
    background-color: {DARK_BG};
    color: {TEXT_LIGHT};
}}

.hero {{
    text-align: center;
    padding-top: 40px;
}}

.hero-title {{
    color: {PRIMARY_PINK};
    font-size: 34px;
    font-weight: 700;
}}

.hero-subtitle {{
    color: {SECONDARY_PURPLE};
    font-size: 15px;
}}

.card {{
    background: linear-gradient(180deg, {CARD_BG}, {DARK_BG});
    padding: 28px;
    border-radius: 22px;
    border: 1.5px solid {PRIMARY_PINK};
    box-shadow: 0 0 28px rgba(230, 0, 126, 0.25);
    max-width: 900px;
    margin: 28px auto;
}}

.desc {{
    font-size: 13px;
    text-align: center;
}}

button {{
    background-color: {PRIMARY_PINK} !important;
    color: white !important;
    border-radius: 14px !important;
    border: none !important;
}}

button:hover {{
    background-color: #C4006B !important;
}}

.footer {{
    text-align: center;
    color: #999;
    margin-top: 50px;
    font-size: 13px;
}}
</style>
""", unsafe_allow_html=True)

# =================================================
# SESSION STATE
# =================================================
if "user" not in st.session_state:
    st.session_state.user = None
if "selected_style" not in st.session_state:
    st.session_state.selected_style = None

# =================================================
# LOGIN (SINGLE CLEAN CARD)
# =================================================
if st.session_state.user is None:

    st.markdown("<div class='hero'>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.image("logo.png", use_container_width=True)

    st.markdown("<p class='hero-title'>Nalybecks Afrofuturistic AI</p>", unsafe_allow_html=True)
    st.markdown("<p class='hero-subtitle'>Wear Your Crown Beautifully — powered by AI</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Enter Experience")
    username = st.text_input("Your name")

    if st.button("Continue"):
        if username.strip():
            st.session_state.user = username
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div class='footer'>© 2026 Nalybecks Hairstyles</div>", unsafe_allow_html=True)
    st.stop()

# =================================================
# HEADER
# =================================================
c1, c2, c3 = st.columns([1,2,1])
with c2:
    st.image("logo.png", width=110)

st.markdown(
    f"<h2 style='text-align:center;color:{PRIMARY_PINK};'>Welcome, {st.session_state.user}</h2>",
    unsafe_allow_html=True
)

# =================================================
# SIDEBAR NAV
# =================================================
st.sidebar.title("Menu")
page = st.sidebar.selectbox(
    "Navigate",
    ["Try Hairstyle", "Gallery", "Feedback", "AI Roadmap", "Analytics"]
)

# =================================================
# FACE MODEL
# =================================================
face_mesh = mp.face_mesh.FaceMesh(static_image_mode=True)

# =================================================
# ANALYTICS LOGGER
# =================================================
def log_event(event, style=""):
    os.makedirs("data", exist_ok=True)
    with open("data/analytics.csv", "a", newline="") as f:
        csv.writer(f).writerow(
            [datetime.now(), st.session_state.user, event, style]
        )

# =================================================
# AI RECOMMENDER (FACE-SHAPE LOGIC)
# =================================================
def recommend_hairstyle(face_width, face_height):
    ratio = face_height / face_width
    if ratio > 1.3:
        return "twists.png", "Twists balance longer face shapes."
    elif ratio > 1.1:
        return "cornrows.png", "Cornrows suit balanced face shapes."
    elif ratio > 0.95:
        return "galactic_knots.png", "Galactic Knots make a bold statement."
    else:
        return "afro_crown.png", "Afro Crown enhances wider face shapes."

# =================================================
# IMAGE OVERLAY (SAFE)
# =================================================
def overlay_image(bg, overlay, x, y):
    if overlay.shape[2] == 3:
        overlay = cv2.cvtColor(overlay, cv2.COLOR_BGR2BGRA)
    h, w = overlay.shape[:2]
    alpha = overlay[:, :, 3] / 255.0
    for c in range(3):
        bg[y:y+h, x:x+w, c] = (
            (1 - alpha) * bg[y:y+h, x:x+w, c] +
            alpha * overlay[:, :, c]
        )
    return bg

# =================================================
# HAIRSTYLE CATEGORIES
# =================================================
categories = {
    "Protective Styles": {
        "cornrows.png": "Cornrows – Classic & protective",
        "twists.png": "Twists – Soft & versatile"
    },
    "Royal Styles": {
        "afro_crown.png": "Afro Crown – Regal volume",
        "galactic_knots.png": "Galactic Knots – Afrofuturistic roots"
    },
    "Futuristic Styles": {
        "futuristic_braided.png": "Galactic Braids – Sculptural future"
    }
}

# =================================================
# TRY HAIRSTYLE
# =================================================
if page == "Try Hairstyle":

    st.markdown("## 📸 Upload Your Selfie")
    uploaded = st.file_uploader("Choose an image", type=["jpg","png","jpeg"])

    if uploaded:
        img = np.array(Image.open(uploaded))
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        with st.spinner("✨ Applying Afrofuturistic AI..."):
            time.sleep(1)
            results = face_mesh.process(rgb)

        st.image(img, caption="Original Photo", width=350)

        if results.multi_face_landmarks:
            lm = results.multi_face_landmarks[0]
            top = lm.landmark[10]
            chin = lm.landmark[152]
            left = lm.landmark[234]
            right = lm.landmark[454]

            lx = int(left.x * img.shape[1])
            rx = int(right.x * img.shape[1])
            fy = int(top.y * img.shape[0])

            face_width = rx - lx
            face_height = int((chin.y - top.y) * img.shape[0])

            rec_style, rec_text = recommend_hairstyle(face_width, face_height)

            st.markdown("### 🤖 AI Recommendation")
            st.image(f"hairstyles/{rec_style}", width=140)
            st.success(rec_text)

            if st.button("Apply Recommended Style"):
                st.session_state.selected_style = rec_style
                log_event("ai_recommendation", rec_style)

            tabs = st.tabs(categories.keys())
            for tab, styles in zip(tabs, categories.values()):
                with tab:
                    cols = st.columns(2)
                    for i, (style, desc) in enumerate(styles.items()):
                        with cols[i % 2]:
                            st.image(f"hairstyles/{style}", width=140)
                            st.markdown(f"<p class='desc'>{desc}</p>", unsafe_allow_html=True)
                            if st.button(desc.split("–")[0], key=style):
                                st.session_state.selected_style = style

            if st.session_state.selected_style:
                hair = cv2.imread(
                    f"hairstyles/{st.session_state.selected_style}",
                    cv2.IMREAD_UNCHANGED
                )
                hair = cv2.resize(hair, (face_width, int(face_width * 0.8)))
                y_offset = max(0, fy - hair.shape[0] + 20)

                result = overlay_image(img.copy(), hair, lx, y_offset)
                st.image(result, caption="✨ Your Afrofuturistic Look", width=350)

                buf = io.BytesIO()
                Image.fromarray(result).save(buf, format="PNG")

                st.download_button("⬇️ Download Image", buf.getvalue(), "nalybecks_ai.png")

                # ----------- SHARE -----------
                st.markdown("### 🔁 Share Your Look")
                share_text = quote_plus(
                    "I just tried an Afrofuturistic hairstyle using Nalybecks Afrofuturistic AI 👑✨"
                )

                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    st.markdown(f"[WhatsApp](https://wa.me/?text={share_text}%20{APP_URL})")
                with c2:
                    st.markdown(f"[Facebook](https://www.facebook.com/sharer/sharer.php?u={APP_URL})")
                with c3:
                    st.markdown(f"[Twitter/X](https://twitter.com/intent/tweet?text={share_text}&url={APP_URL})")
                with c4:
                    st.markdown(f"[Instagram](https://www.instagram.com/)")

                # ----------- BOOKING -----------
                st.markdown("---")
                st.markdown(
                    f"""
                    <a href="https://wa.me/{WHATSAPP_NUMBER}?text=Hello Nalybecks! I would like to book this hairstyle."
                       target="_blank">
                       <button>📲 Book on WhatsApp</button>
                    </a>
                    """,
                    unsafe_allow_html=True
                )

# =================================================
# GALLERY
# =================================================
if page == "Gallery":
    st.markdown("## 🖼 Gallery")
    if os.path.exists("gallery"):
        imgs = os.listdir("gallery")[-9:]
        cols = st.columns(3)
        for i, f in enumerate(imgs):
            with cols[i % 3]:
                st.image(f"gallery/{f}", width=120)

# =================================================
# FEEDBACK
# =================================================
if page == "Feedback":
    st.markdown("## 📝 Feedback")
    with st.form("feedback"):
        fb = st.text_area("Your feedback")
        if st.form_submit_button("Submit"):
            st.success("Thank you for your feedback 💖")

# =================================================
# AI ROADMAP (VISUAL)
# =================================================
if page == "AI Roadmap":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("""
    ## 🚀 AI Evolution Roadmap

    **Now (MVP)**  
    - Classical computer vision  
    - Face landmarks + heuristic overlays  

    **Next (Planned Upgrade)**  
    - GANs & Diffusion models  
    - African hair–first datasets  
    - Realistic texture & volume synthesis  

    **Why it matters**  
    - Inclusive beauty-tech AI  
    - African innovation & representation  
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# =================================================
# ANALYTICS (ADMIN ONLY)
# =================================================
if page == "Analytics":
    if st.session_state.user.lower() != "rebecca":
        st.warning("Admin access only.")
    else:
        st.markdown("## 📊 Analytics Dashboard")
        path = "data/analytics.csv"
        if os.path.exists(path):
            df = pd.read_csv(path, names=["time","user","event","style"])
            st.bar_chart(df["style"].value_counts())
            st.dataframe(df.tail(10))

# =================================================
# FOOTER
# =================================================
st.markdown("""
<div class="footer">
Powered by Nalybecks Afrofuturistic AI<br>
Wear Your Crown Beautifully
</div>
""", unsafe_allow_html=True)
