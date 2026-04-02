import streamlit as st
from PIL import Image, ImageFilter
import numpy as np
import io

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="AI Image Dashboard", layout="wide")

# =========================
# CSS (CARD UI)
# =========================
st.markdown("""
<style>
.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 20px;
}
.tool-card {
    padding: 20px;
    border-radius: 15px;
    background: #f5f7fa;
    text-align: center;
    transition: 0.3s;
    border: 1px solid #eee;
}
.tool-card:hover {
    background: #e6f0ff;
    transform: scale(1.03);
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">✨ AI Image Dashboard</div>', unsafe_allow_html=True)

# =========================
# SIDEBAR (ONLY UPLOAD)
# =========================
st.sidebar.header("📤 Upload Image")
uploaded_file = st.sidebar.file_uploader("", type=["png", "jpg", "jpeg"])

# =========================
# TOOL CARDS (MAIN SCREEN)
# =========================
st.subheader("🧰 Choose a Tool")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🎨 Background Change", use_container_width=True):
        st.session_state.tool = "bg"

with col2:
    if st.button("✨ Enhance Image", use_container_width=True):
        st.session_state.tool = "enhance"

with col3:
    if st.button("🧽 Erase Tool", use_container_width=True):
        st.session_state.tool = "erase"

col4, col5, col6 = st.columns(3)

with col4:
    if st.button("🌫 Blur Tool", use_container_width=True):
        st.session_state.tool = "blur"

with col5:
    if st.button("❌ Remove Object", use_container_width=True):
        st.session_state.tool = "remove"

with col6:
    if st.button("🖼 Background Tool", use_container_width=True):
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
        st.image(image, use_column_width=True)

    # =========================
    # TOOL LOGIC
    # =========================
    tool = st.session_state.get("tool", None)

    # 🎨 Background Change
    if tool == "bg":
        color_hex = st.color_picker("Pick Color", "#00ffaa")
        color = tuple(int(color_hex[i:i+2], 16) for i in (1, 3, 5))

        if st.button("🚀 Apply"):
            img_array = np.array(image)
            gray = np.mean(img_array, axis=2)
            mask = gray > 200
            img_array[mask] = color
            result = Image.fromarray(img_array)

            with colB:
                st.subheader("✅ Result")
                st.image(result, use_column_width=True)

            buf = io.BytesIO()
            result.save(buf, format="PNG")
            st.download_button("📥 Download", buf.getvalue(), "bg.png")

    # ✨ Enhance
    elif tool == "enhance":
        strength = st.slider("Sharpness", 1, 5, 2)

        if st.button("🚀 Enhance"):
            result = image
            for _ in range(strength):
                result = result.filter(ImageFilter.SHARPEN)

            with colB:
                st.subheader("✅ Result")
                st.image(result, use_column_width=True)

            buf = io.BytesIO()
            result.save(buf, format="PNG")
            st.download_button("📥 Download", buf.getvalue(), "enhanced.png")

    # 🔗 External Tools
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

st.markdown("---")
st.caption("🚀 Built with Streamlit")
