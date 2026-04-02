import streamlit as st
from PIL import Image, ImageFilter
import numpy as np
import io

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="AI Image Dashboard", layout="wide")

# =========================
# 🎨 PRO CSS (Photoshop Style)
# =========================
st.markdown("""
<style>

/* 🌈 BACKGROUND */
body {
    background: #fff7ed;
}

/* ✨ TITLE */
.main-title {
    text-align: center;
    font-size: 38px;
    font-weight: 700;
    color: #7c2d12;
}

/* 🧰 LEFT TOOLBAR */
.toolbar {
    background: white;
    padding: 10px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

/* 🔲 TOOL BUTTON */
.tool-btn button {
    width: 100%;
    margin-bottom: 10px;
    border-radius: 10px;
    background: #fff7ed;
    border: 1px solid #fed7aa;
}

/* 🎨 ACTIVE TOOL */
.active-tool {
    background: linear-gradient(135deg, #f97316, #ea580c) !important;
    color: white !important;
}

/* 🎨 BUTTON */
.stButton > button {
    background: linear-gradient(135deg, #f97316, #ea580c);
    color: white;
    border-radius: 10px;
    padding: 10px;
    border: none;
    font-weight: 600;
}

/* 📸 IMAGE */
.stImage {
    border-radius: 12px;
    border: 1px solid #fed7aa;
    background: white;
}

/* 🔻 FOOTER */
footer {
    text-align: center;
    color: #9a3412;
}

</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================
st.markdown('<div class="main-title">✨ AI Image Dashboard</div>', unsafe_allow_html=True)

# =========================
# SIDEBAR (UPLOAD ONLY)
# =========================
st.sidebar.header("📤 Upload")
uploaded_file = st.sidebar.file_uploader("", type=["png", "jpg", "jpeg"])

# =========================
# MAIN LAYOUT
# =========================
left, right = st.columns([1, 5])

# =========================
# 🧰 LEFT TOOLBAR
# =========================
with left:
    st.markdown("### 🧰 Tools")

    if st.button("🎨 BG"):
        st.session_state.tool = "bg"

    if st.button("✨ Enhance"):
        st.session_state.tool = "enhance"

    if st.button("🧽 Erase"):
        st.session_state.tool = "erase"

    if st.button("🌫 Blur"):
        st.session_state.tool = "blur"

    if st.button("❌ Remove"):
        st.session_state.tool = "remove"

    if st.button("🖼 BG Tool"):
        st.session_state.tool = "bg_tool"

# =========================
# 🖼 RIGHT PANEL
# =========================
with right:

    # TOOL CARDS (shown when no tool selected)
    if "tool" not in st.session_state:
        st.subheader("🧰 Choose a Tool")

        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("🎨 Background Change"):
                st.session_state.tool = "bg"

        with c2:
            if st.button("✨ Enhance Image"):
                st.session_state.tool = "enhance"

        with c3:
            if st.button("🧽 Erase Tool"):
                st.session_state.tool = "erase"

        c4, c5, c6 = st.columns(3)
        with c4:
            if st.button("🌫 Blur Tool"):
                st.session_state.tool = "blur"

        with c5:
            if st.button("❌ Remove Object"):
                st.session_state.tool = "remove"

        with c6:
            if st.button("🖼 Background Tool"):
                st.session_state.tool = "bg_tool"

    # =========================
    # IMAGE AREA
    # =========================
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        image.thumbnail((600, 600))

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📸 Original")
            st.image(image)

        tool = st.session_state.get("tool", None)

        # 🎨 BACKGROUND CHANGE
        if tool == "bg":
            color_hex = st.color_picker("Pick Color", "#f97316")
            color = tuple(int(color_hex[i:i+2], 16) for i in (1, 3, 5))

            if st.button("🚀 Apply"):
                img_array = np.array(image)
                gray = np.mean(img_array, axis=2)
                mask = gray > 200
                img_array[mask] = color
                result = Image.fromarray(img_array)

                with col2:
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

                with col2:
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
