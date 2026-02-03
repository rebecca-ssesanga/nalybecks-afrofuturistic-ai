import streamlit as st
import cv2
import numpy as np
from PIL import Image
from mediapipe import solutions as mp
import io, os, time, csv
import pandas as pd
from datetime import datetime

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Nalybecks Afrofuturistic AI",
    page_icon="logo.png",
    layout="centered"
)

# ================= CSS =================
st.markdown("""
<style>
body { background-color:#0b0b0f; }
h1,h2,h3 { color: gold; text-align:center; }
p,label { color:white; }
.desc { font-size:12px; color:#ddd; text-align:center; }
.card {
    background:#1c1c2b; padding:10px; border-radius:15px;
    border:2px solid gold; text-align:center; margin-bottom:10px;
}
.whatsapp {
    background:#25D366; color:white; padding:14px;
    border-radius:12px; text-align:center; font-weight:bold;
}
.footer { text-align:center; color:#aaa; margin-top:30px; }
</style>
""", unsafe_allow_html=True)

# ================= LOGO =================
if os.path.exists("logo.png"):
    st.image("logo.png", width=140)

st.markdown("<h1>Nalybecks Afrofuturistic AI</h1>", unsafe_allow_html=True)
st.markdown("<h3>Wear Your Crown Beautifully — powered by AI</h3>", unsafe_allow_html=True)

# ================= LOGIN =================
st.markdown("## 👤 Login")

if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    username = st.text_input("Enter your name")
    if st.button("Login"):
        if username.strip():
            st.session_state.user = username
            st.success(f"Welcome {username} 👑")
else:
    st.success(f"Logged in as {st.session_state.user}")
    if st.button("Logout"):
        st.session_state.user = None
        st.experimental_rerun()

# ================= SIDEBAR =================
st.sidebar.title("Menu")
page = st.sidebar.selectbox("Select Page", ["Try Hairstyle", "Analytics Dashboard"])

# ================= ANALYTICS LOGGER =================
def log_event(user, event, style=""):
    os.makedirs("data", exist_ok=True)
    with open("data/analytics.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), user, event, style])

# ================= AI RECOMMENDER =================
def recommend_hairstyle(face_width, face_height):
    ratio = face_height / face_width
    if ratio > 1.3:
        return "twists.png", "Twists – Best for longer face shapes."
    elif ratio > 1.1:
        return "cornrows.png", "Cornrows – Balanced and elegant."
    elif ratio > 0.9:
        return "galactic_knots.png", "Galactic Knots – Bold Afrofuturistic look."
    else:
        return "afro_crown.png", "Afro Crown – Best for wider face shapes."

# ================= FACE MODEL =================
face_mesh = mp.face_mesh.FaceMesh(static_image_mode=True)

# ================= SAFE OVERLAY =================
def overlay_image(background, overlay, x, y):
    h, w = overlay.shape[:2]

    if overlay.shape[2] == 3:
        overlay = cv2.cvtColor(overlay, cv2.COLOR_BGR2BGRA)

    alpha = overlay[:, :, 3] / 255.0

    for c in range(3):
        background[y:y+h, x:x+w, c] = (
            (1 - alpha) * background[y:y+h, x:x+w, c]
            + alpha * overlay[:, :, c]
        )
    return background

# ================= HAIRSTYLES =================
categories = {
    "Protective Styles": {
        "cornrows.png": "Cornrows – Classic protective style.",
        "twists.png": "Twists – Soft elegant twists."
    },
    "Royal Styles": {
        "afro_crown.png": "Afro Crown – Royal silhouette.",
        "galactic_knots.png": "Galactic Knots – Ancestral futuristic look."
    },
    "Futuristic Styles": {
        "futuristic_braided.png": "Galactic Braids – Bold cosmic braided design."
    }
}

# =================================================
# ================= TRY HAIRSTYLE =================
# =================================================
if page == "Try Hairstyle":

    if not st.session_state.user:
        st.info("Please login to use the app.")
        st.stop()

    uploaded_file = st.file_uploader("📸 Upload your selfie", type=["jpg","png","jpeg"])

    if "selected_style" not in st.session_state:
        st.session_state.selected_style = None

    result_image = None

    if uploaded_file:
        image = Image.open(uploaded_file)
        img = np.array(image)

        if img.shape[1] > 900:
            scale = 900 / img.shape[1]
            img = cv2.resize(img, (int(img.shape[1]*scale), int(img.shape[0]*scale)))

        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        with st.spinner("✨ Applying Afrofuturistic hairstyle..."):
            time.sleep(1)
            results = face_mesh.process(rgb)

        st.image(img, caption="Original Photo", width=350)

        if not results.multi_face_landmarks:
            st.warning("No face detected. Upload a clear selfie.")
        else:
            lm = results.multi_face_landmarks[0]

            top = lm.landmark[10]
            chin = lm.landmark[152]
            left = lm.landmark[234]
            right = lm.landmark[454]

            fy = int(top.y * img.shape[0])
            lx = int(left.x * img.shape[1])
            rx = int(right.x * img.shape[1])

            face_width = rx - lx
            face_height = int((chin.y - top.y) * img.shape[0])

            # AI Recommendation
            rec_style, rec_text = recommend_hairstyle(face_width, face_height)

            st.markdown("## 🤖 AI Recommendation")
            st.image(f"hairstyles/{rec_style}", width=150)
            st.success(rec_text)

            if st.button("Apply Recommended Style"):
                st.session_state.selected_style = rec_style
                log_event(st.session_state.user, "apply_recommendation", rec_style)

            def apply_hairstyle(style_file):
                hair_path = f"hairstyles/{style_file}"

                if not os.path.exists(hair_path):
                    st.error(f"Missing file: {hair_path}")
                    return img

                hair = cv2.imread(hair_path, cv2.IMREAD_UNCHANGED)

                if hair is None:
                    st.error("Could not load hairstyle image.")
                    return img

                if hair.shape[2] == 3:
                    hair = cv2.cvtColor(hair, cv2.COLOR_BGR2BGRA)

                hair = cv2.resize(hair, (face_width, int(face_width * 0.8)))

                x_offset = lx
                y_offset = fy - hair.shape[0] + 20
                if y_offset < 0:
                    y_offset = 0

                result = overlay_image(img.copy(), hair, x_offset, y_offset)

                st.image(result, caption="✨ Your Afrofuturistic Look", width=350)

                os.makedirs("gallery", exist_ok=True)
                filename = f"gallery/{st.session_state.user}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                Image.fromarray(result).save(filename)

                log_event(st.session_state.user, "try_style", style_file)
                return result

            # CATEGORY TABS
            tabs = st.tabs(list(categories.keys()))
            for tab, (category, styles) in zip(tabs, categories.items()):
                with tab:
                    cols = st.columns(2)
                    i = 0
                    for style, desc in styles.items():
                        with cols[i % 2]:
                            st.image(f"hairstyles/{style}", width=140)
                            st.markdown(f"<p class='desc'>{desc}</p>", unsafe_allow_html=True)
                            if st.button(desc.split("–")[0], key=style):
                                st.session_state.selected_style = style
                        i += 1

            if st.session_state.selected_style:
                result_image = apply_hairstyle(st.session_state.selected_style)

    # ================= DOWNLOAD + SHARE =================
    if result_image is not None:
        buf = io.BytesIO()
        Image.fromarray(result_image).save(buf, format="PNG")

        if st.download_button("⬇️ Download Your Look", buf.getvalue(), "nalybecks_ai.png", "image/png"):
            log_event(st.session_state.user, "download", st.session_state.selected_style)

        # Instagram
        st.markdown("## 📸 Share on Instagram")
        caption = """I just tried the Nalybecks Afrofuturistic AI hairstyle 👑✨
#NalybecksAI #AfrofuturisticHair #WearYourCrownBeautifully #GalacticBraids"""
        st.code(caption)

        st.markdown("""
<a href="https://www.instagram.com/" target="_blank">
<div style="background:#E1306C; color:white; padding:14px; border-radius:12px; text-align:center;">
📸 Open Instagram
</div>
</a>
""", unsafe_allow_html=True)

        # Facebook / WhatsApp / Twitter
        app_url = "https://your-app-link.streamlit.app"
        share_text = "I just tried Nalybecks Afrofuturistic AI hairstyle 👑✨"

        st.markdown(f"""
<a href="https://www.facebook.com/sharer/sharer.php?u={app_url}" target="_blank">📘 Share on Facebook</a><br><br>
<a href="https://wa.me/?text={share_text} {app_url}" target="_blank">📲 Share on WhatsApp</a><br><br>
<a href="https://twitter.com/intent/tweet?text={share_text}&url={app_url}" target="_blank">🐦 Share on Twitter/X</a>
""", unsafe_allow_html=True)

        # WhatsApp Booking
        phone_number = "256775668530"
        whatsapp_url = f"https://wa.me/{phone_number}?text=Hello Nalybecks! I want to book this hairstyle."
        st.markdown(f"""
<a href="{whatsapp_url}" target="_blank">
<div class="whatsapp">📲 Book This Hairstyle on WhatsApp</div>
</a>
""", unsafe_allow_html=True)

    # ================= GALLERY =================
    st.markdown("## 🖼️ Gallery")
    if os.path.exists("gallery"):
        imgs = os.listdir("gallery")
        cols = st.columns(3)
        for i, imgf in enumerate(imgs[-6:]):
            with cols[i % 3]:
                st.image(f"gallery/{imgf}", width=120)

    # ================= FEEDBACK =================
    st.markdown("## 📝 Feedback")
    with st.form("feedback_form"):
        name = st.text_input("Your Name")
        feedback = st.text_area("Your feedback")
        submitted = st.form_submit_button("Submit")
        if submitted:
            os.makedirs("data", exist_ok=True)
            with open("data/feedback.txt","a") as f:
                f.write(f"{name}: {feedback}\n")
            st.success("Thank you for your feedback 💛")

# =================================================
# ================= ANALYTICS =====================
# =================================================
if page == "Analytics Dashboard":

    admin_users = ["Rebecca"]

    if st.session_state.user not in admin_users:
        st.warning("Admin access only.")
    else:
        st.markdown("## 📊 Analytics Dashboard")

        path = "data/analytics.csv"

        if not os.path.exists(path):
            st.info("No analytics data yet.")
        else:
            df = pd.read_csv(path, names=["time","user","event","style"])

            st.metric("Total Users", df["user"].nunique())
            st.metric("Total Events", len(df))

            st.markdown("### Most Popular Hairstyles")
            st.bar_chart(df["style"].value_counts())

            st.markdown("### Event Breakdown")
            st.bar_chart(df["event"].value_counts())

            st.dataframe(df.tail(10))

# ================= FOOTER =================
st.markdown("""
<div class="footer">
Powered by Nalybecks Afrofuturistic AI<br>
© 2026 Nalybecks Hairstyles | Wear Your Crown Beautifully
</div>
""", unsafe_allow_html=True)
