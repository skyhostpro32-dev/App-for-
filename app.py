import streamlit as st
from PIL import Image, ImageFilter
import numpy as np
import io

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="AI Image Dashboard", layout="wide")

# =========================
# 💜 GLOBAL CSS (HIDE STREAMLIT + LAVENDER UI)
# =========================
st.markdown("""
<style>

/* ❌ HIDE STREAMLIT HEADER & MENU */
header {visibility: hidden;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* ❌ HIDE MANAGE APP BUTTON */
[data-testid="stStatusWidget"] {
    display: none !important;
}

/* 🌈 FULL BACKGROUND */
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f5f3ff, #ede9fe) !important;
}

/* REMOVE WHITE BLOCK */
[data-testid="stAppViewContainer"] > .main {
    background: transparent;
}
.block-container {
    background: transparent;
    padding-top: 1rem;
}

/* ✨ TITLE */
.main-title {
    text-align: center;
    font-size: 38px;
    font-weight: 700;
    color: #5b21b6;
    margin-bottom: 10px;
}

/* 📦 SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f5f3ff, #ddd6fe);
}

/* 📤 UPLOAD BOX */
[data-testid="stFileUploader"] {
    border: 2px dashed #c4b5fd;
    background: #f5f3ff;
    border-radius: 14px;
    padding: 12px;
}

/* 🔲 TOOL CARD */
.tool-card {
    background: white;
    padding: 18px;
    border-radius: 18px;
    border: 1px solid #e9d5ff;
    transition: 0.25s;
    height: 140px;
}

/* ✨ HOVER */
.tool-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(139,92,246,0.15);
    border-color: #8b5cf6;
}

/* 🎨 TITLE */
.tool-title {
    font-size: 18px;
    font-weight: 600;
    color: #5b21b6;
}

/* 📝 DESC */
.tool-desc {
    font-size: 13px;
    color: #6d28d9;
    margin-top: 6px;
}

/* 👻 INVISIBLE BUTTON */
.stButton > button {
    width: 100%;
    height: 140px;
    opacity: 0;
    position: absolute;
}

/* 📸 IMAGE */
.stImage {
    border-radius: 12px;
    border: 1px solid #ddd6fe;
    background: white;
}

/* 📥 DOWNLOAD BUTTON */
.stDownloadButton > button {
    background: linear-gradient(135deg, #a78bfa, #8b5cf6);
    color: white;
    border-radius: 10px;
}

/* 🔻 FOOTER TEXT */
footer {
    text-align: center;
    color: #6d28d9;
}

</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================
st.markdown('<div class="main-title">✨ AI Image Dashboard</div>', unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
st.sidebar.header("📤 Upload Image")
uploaded_file = st.sidebar.file_uploader("", type=["png", "jpg", "jpeg"])

# =========================
# TOOL CARDS
# =========================
st.subheader("🧰 Choose a Tool")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button(" ", key="bg"):
        st.session_state.tool = "bg"
    st.markdown("""
    <div class="tool-card">
        <div class="tool-title">🎨 Background Change</div>
        <div class="tool-desc">Change the background color</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if st.button(" ", key="enhance"):
        st.session_state.tool = "enhance"
    st.markdown("""
    <div class="tool-card">
        <div class="tool-title">✨ Enhance Image</div>
        <div class="tool-desc">Sharpen and enhance photo</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    if st.button(" ", key="erase"):
        st.session_state.tool = "erase"
    st.markdown("""
    <div class="tool-card">
        <div class="tool-title">🧽 Erase Tool</div>
        <div class="tool-desc">Erase unwanted parts</div>
    </div>
    """, unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)

with col4:
    if st.button(" ", key="blur"):
        st.session_state.tool = "blur"
    st.markdown("""
    <div class="tool-card">
        <div class="tool-title">🌫 Blur Tool</div>
        <div class="tool-desc">Blur out parts of an image</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    if st.button(" ", key="remove"):
        st.session_state.tool = "remove"
    st.markdown("""
    <div class="tool-card">
        <div class="tool-title">❌ Remove Object</div>
        <div class="tool-desc">Remove objects from photo</div>
    </div>
    """, unsafe_allow_html=True)

with col6:
    if st.button(" ", key="bg_tool"):
        st.session_state.tool = "bg_tool"
    st.markdown("""
    <div class="tool-card">
        <div class="tool-title">🖼 Background Tool</div>
        <div class="tool-desc">Auto remove background</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# IMAGE PROCESSING
# =========================
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    image.thumbnail((600, 600))

    colA, colB = st.columns(2)

    with colA:
        st.subheader("📸 Original")
        st.image(image)

    tool = st.session_state.get("tool")

    # 🎨 BACKGROUND CHANGE
    if tool == "bg":
        color_hex = st.color_picker("Pick Color", "#8b5cf6")
        color = tuple(int(color_hex[i:i+2], 16) for i in (1, 3, 5))

        if st.button("Apply"):
            img_array = np.array(image)
            gray = np.mean(img_array, axis=2)
            mask = gray > 200
            img_array[mask] = color
            result = Image.fromarray(img_array)

            with colB:
                st.subheader("✅ Result")
                st.image(result)

            buf = io.BytesIO()
            result.save(buf, format="PNG")
            st.download_button("Download", buf.getvalue(), "bg.png")

    # ✨ ENHANCE
    elif tool == "enhance":
        strength = st.slider("Sharpness", 1, 5, 2)

        if st.button("Enhance"):
            result = image
            for _ in range(strength):
                result = result.filter(ImageFilter.SHARPEN)

            with colB:
                st.subheader("✅ Result")
                st.image(result)

            buf = io.BytesIO()
            result.save(buf, format="PNG")
            st.download_button("Download", buf.getvalue(), "enhanced.png")

    # 🔗 EXTERNAL TOOLS
    elif tool == "erase":
        st.link_button("Open Erase Tool", "https://skyhostpro32-dev.github.io/erase-tool/")

    elif tool == "blur":
        st.link_button("Open Blur Tool", "https://skyhostpro32-dev.github.io/index./")

    elif tool == "remove":
        st.link_button("Open Remove Tool", "https://l3c2ddsnh8gkka5rnezbak.streamlit.app/")

    elif tool == "bg_tool":
        st.link_button("Open Background Tool", "https://import-cus7p2zpohpwkbavzyrmpl.streamlit.app/")

else:
    st.info("👈 Upload an image to start")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("🚀 Built with Streamlit")
