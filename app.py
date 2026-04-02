import streamlit as st
from PIL import Image, ImageFilter
import numpy as np
import io

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="AI Image Dashboard", layout="wide")

# =========================
# 🎨 ORANGE THEME CSS
# =========================
st.markdown("""
<style>

/* 🌈 BACKGROUND */
body {
    background: #fff7ed;
}

/* ✨ TITLE */
h1 {
    color: #7c2d12;
    text-align: center;
    font-weight: 700;
}

/* 📦 SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #fff7ed, #ffe4d6);
}

/* 📤 UPLOAD BOX */
[data-testid="stFileUploader"] {
    border: 2px dashed #fb923c;
    background: #fff7ed;
    border-radius: 12px;
    padding: 10px;
}

/* 🎯 RADIO */
.stRadio > div {
    background: #ffffff;
    padding: 10px;
    border-radius: 10px;
    border: 1px solid #fed7aa;
}

/* 🎨 BUTTON */
.stButton > button {
    background: linear-gradient(135deg, #f97316, #ea580c);
    color: white;
    border-radius: 10px;
    padding: 10px 16px;
    border: none;
    font-weight: 600;
    transition: 0.3s;
}

/* 🔥 BUTTON HOVER */
.stButton > button:hover {
    background: linear-gradient(135deg, #ea580c, #c2410c);
    transform: scale(1.05);
}

/* 📸 IMAGE BOX */
.stImage {
    border-radius: 12px;
    border: 1px solid #fed7aa;
    padding: 5px;
    background: white;
}

/* 📥 DOWNLOAD */
.stDownloadButton > button {
    background: linear-gradient(135deg, #fb923c, #f97316);
    color: white;
    border-radius: 10px;
}

/* 🔻 DIVIDER */
hr {
    border: none;
    height: 1px;
    background: #fed7aa;
}

/* 🚀 FOOTER */
footer {
    color: #9a3412;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================
st.title("✨ AI Image Dashboard")

# =========================
# SIDEBAR
# =========================
st.sidebar.title("🧰 Tools")

uploaded_file = st.sidebar.file_uploader(
    "📤 Upload Image", type=["png", "jpg", "jpeg"]
)

tool = st.sidebar.radio(
    "Select Tool",
    ["🎨 Background Change", "✨ Enhance Image"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎯 Advanced Tool")
st.sidebar.markdown("👉 Use Erase Tool below")

st.sidebar.markdown("[🚀 Open Erase Tool](https://skyhostpro32-dev.github.io/erase-tool/)")
st.sidebar.markdown("[🚀 Open Blur Tool](https://skyhostpro32-dev.github.io/index./)")
st.sidebar.markdown("[🚀 Open Remove Object Tool](https://l3c2ddsnh8gkka5rnezbak.streamlit.app/)")
st.sidebar.markdown("[🚀 Open Background Tool](https://import-cus7p2zpohpwkbavzyrmpl.streamlit.app/)")

# =========================
# MAIN LAYOUT
# =========================
col1, col2 = st.columns(2)

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    image.thumbnail((600, 600))

    with col1:
        st.subheader("📸 Original Image")
        st.image(image, use_column_width=True)

    # =========================
    # 🎨 BACKGROUND CHANGE
    # =========================
    if tool == "🎨 Background Change":
        st.sidebar.subheader("🎨 Settings")

        color_hex = st.sidebar.color_picker("Pick Background Color", "#f97316")
        color = tuple(int(color_hex[i:i+2], 16) for i in (1, 3, 5))

        if st.sidebar.button("🚀 Apply Background"):
            with st.spinner("Processing..."):
                img_array = np.array(image)
                gray = np.mean(img_array, axis=2)
                mask = gray > 200
                img_array[mask] = color
                result = Image.fromarray(img_array)

            with col2:
                st.subheader("✅ Result")
                st.image(result, use_column_width=True)

            buf = io.BytesIO()
            result.save(buf, format="PNG")
            st.download_button("📥 Download", buf.getvalue(), "background.png")

    # =========================
    # ✨ ENHANCE IMAGE
    # =========================
    elif tool == "✨ Enhance Image":
        st.sidebar.subheader("✨ Settings")

        strength = st.sidebar.slider("Sharpness", 1, 5, 2)

        if st.sidebar.button("🚀 Enhance"):
            with st.spinner("Enhancing image..."):
                result = image
                for _ in range(strength):
                    result = result.filter(ImageFilter.SHARPEN)

            with col2:
                st.subheader("✅ Result")
                st.image(result, use_column_width=True)

            buf = io.BytesIO()
            result.save(buf, format="PNG")
            st.download_button("📥 Download", buf.getvalue(), "enhanced.png")

else:
    st.info("👈 Upload an image from the sidebar to begin")

st.markdown("---")
st.caption("🚀 Built with Streamlit")
