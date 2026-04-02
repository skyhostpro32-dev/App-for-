import streamlit as st
from PIL import Image, ImageFilter
import numpy as np
import io

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="AI Image Dashboard", layout="wide")

# =========================
# 💜 LAVENDER CSS
# =========================
st.markdown("""
<style>

/* 🌈 BACKGROUND */
body {
    background: linear-gradient(135deg, #f5f3ff, #ede9fe);
}

/* ✨ TITLE */
.main-title {
    text-align: center;
    font-size: 40px;
    font-weight: 700;
    color: #5b21b6;
}

/* 📦 SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f5f3ff, #ddd6fe);
    padding: 10px;
}

/* 📤 UPLOAD BOX */
[data-testid="stFileUploader"] {
    border: 2px dashed #a78bfa;
    background: #f5f3ff;
    border-radius: 12px;
    padding: 10px;
}

/* 🔲 TOOL CARD */
.tool-card {
    background: white;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #ddd6fe;
    transition: 0.3s;
    text-align: center;
}

.tool-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 10px 25px rgba(139,92,246,0.2);
    border-color: #8b5cf6;
}

/* 🧰 BUTTON */
.stButton > button {
    background: linear-gradient(135deg, #8b5cf6, #7c3aed);
    color: white;
    border-radius: 10px;
    padding: 10px;
    border: none;
    font-weight: 600;
}

/* 🔥 HOVER */
.stButton > button:hover {
    background: linear-gradient(135deg, #7c3aed, #6d28d9);
    transform: scale(1.05);
}

/* 📸 IMAGE */
.stImage {
    border-radius: 12px;
    border: 1px solid #ddd6fe;
    background: white;
}

/* 📥 DOWNLOAD */
.stDownloadButton > button {
    background: linear-gradient(135deg, #a78bfa, #8b5cf6);
    color: white;
    border-radius: 10px;
}

/* 🔻 FOOTER */
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
    if st.button("🎨 Background Change"):
        st.session_state.tool = "bg"

with col2:
    if st.button("✨ Enhance Image"):
        st.session_state.tool = "enhance"

with col3:
    if st.button("🧽 Erase Tool"):
        st.session_state.tool = "erase"

col4, col5, col6 = st.columns(3)

with col4:
    if st.button("🌫 Blur Tool"):
        st.session_state.tool = "blur"

with col5:
    if st.button("❌ Remove Object"):
        st.session_state.tool = "remove"

with col6:
    if st.button("🖼 Background Tool"):
        st.session_state.tool = "bg_tool"

# =========================
# MAIN IMAGE AREA
# =========================
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    image.thumbnail((600, 600))

    colA, colB = st.columns(2)

    with colA:
        st.subheader("📸 Original")
        st.image(image)

    tool = st.session_state.get("tool", None)

    # 🎨 BACKGROUND CHANGE
    if tool == "bg":
        color_hex = st.color_picker("Pick Color", "#8b5cf6")
        color = tuple(int(color_hex[i:i+2], 16) for i in (1, 3, 5))

        if st.button("🚀 Apply"):
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
            st.download_button("📥 Download", buf.getvalue(), "bg.png")

    # ✨ ENHANCE
    elif tool == "enhance":
        strength = st.slider("Sharpness", 1, 5, 2)

        if st.button("🚀 Enhance"):
            result = image
            for _ in range(strength):
                result = result.filter(ImageFilter.SHARPEN)

            with colB:
                st.subheader("✅ Result")
                st.image(result)

            buf = io.BytesIO()
            result.save(buf, format="PNG")
            st.download_button("📥 Download", buf.getvalue(), "enhanced.png")

    # 🔗 EXTERNAL TOOLS
    elif tool == "erase":
        st.link_button("🚀 Open Erase Tool", "https://skyhostpro32-dev.github.io/erase-tool/")

    elif tool == "blur":
        st.link_button("🚀 Open Blur Tool", "https://skyhostpro32-dev.github.io/index./")

    elif tool == "remove":
        st.link_button("🚀 Open Remove Tool", "https://l3c2ddsnh8gkka5rnezbak.streamlit.app/")

    elif tool == "bg_tool":
        st.link_button("🚀 Open Background Tool", "https://import-cus7p2zpohpwkbavzyrmpl.streamlit.app/")

else:
    st.info("👈 Upload an image to start")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("🚀 Built with Streamlit")
