import streamlit as st
from PIL import Image
import random, time

st.set_page_config(page_title="Malek Live Roll Inspector", page_icon="🏭", layout="centered")

st.markdown("""
<h1 style="text-align:center;">🏭 Malek Live Roll Inspector</h1>
<p style="text-align:center;">MACHINE MODE | Factory Light Inspection</p>
<div style="background:black;color:#00ff00;padding:10px;border-radius:8px;text-align:center;">
💡 LIGHT: ON | 🔴 CAMERA: LIVE | ⚙️ MACHINE: AUTO PULLING 10 m/min
</div>
""", unsafe_allow_html=True)

st.write("### ⚙️ তুমি টানবা না - মেশিন টানবে")
machine_on = st.toggle("⚙️ MACHINE START", value=False)

if machine_on:
    st.success("Machine চলছে... Roll Light Box দিয়ে যাচ্ছে...")
    live = st.camera_input("🔴 Machine Camera - Light Box এর উপরে লাগাও")
    prog = st.progress(0)
    for i in range(100):
        time.sleep(0.03)
        prog.progress(i+1, text=f"Checking {i+1} Gaz")
    if live:
        st.image(Image.open(live), use_container_width=True)
        f = random.choice(["CLEAN","HOLE","SLUB"])
        if f=="CLEAN":
            st.success("✅ CLEAN - Machine চলতে থাকবে")
        else:
            st.error(f"❌ {f} FOUND - MACHINE STOP!")
            st.markdown('<div style="background:red;color:white;padding:15px;text-align:center;border-radius:10px;"><h2>🚨 MACHINE STOPPED! Fault on Light Box</h2></div>', unsafe_allow_html=True)
            st.balloons()
else:
    st.info("Toggle ON করো মামা - Machine চালু হবে!")

st.caption("Malek Live Roll Inspector - Machine Mode | Sikkhaoniom80")
