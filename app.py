import streamlit as st
from datetime import datetime
import pandas as pd
import time

st.set_page_config(page_title="Malek Auto Roll Machine", layout="centered")
st.title("MALEK 100 GAJ AUTO MACHINE - V6")
st.error("🤖 FULL AUTO MODE - Roll Cholbe, Fault Pelei Auto Chobi!")

# Memory
if 'auto_start' not in st.session_state:
    st.session_state.auto_start = False
    st.session_state.faults = {"Hole":0,"Slub":0,"Oil":0,"Contamination":0,"Crease":0,"Others":0}
    st.session_state.total = 0
    st.session_state.captured_images = []
    st.session_state.roll_length = 0

roll_no = st.text_input("Roll No (100 Gaj)", "Roll-100G-001")
st.divider()

# MACHINE CONTROL
st.subheader("🏭 ROLL MACHINE CONTROL")
c1, c2 = st.columns(2)
with c1:
    if st.button("▶️ START ROLL - 100 GAJ", use_container_width=True):
        st.session_state.auto_start = True
        st.session_state.total = 0
        st.session_state.captured_images = []
        st.session_state.roll_length = 0
        st.session_state.faults = {k:0 for k in st.session_state.faults}
        st.rerun()
with c2:
    if st.button("⏹️ STOP ROLL", use_container_width=True):
        st.session_state.auto_start = False
        st.rerun()

# CAMERA ON/OFF - TUMAR DABI THAKBEI
st.subheader("📷 CAMERA ON/OFF")
cam_on = st.toggle("Camera ON/OFF", value=st.session_state.auto_start)

if cam_on and st.session_state.auto_start:
    st.success(f"🟢 MACHINE RUNNING... Roll Cholche: {st.session_state.roll_length} Gaj")
    
    # Progress bar - 100 gaj
    progress = st.progress(st.session_state.roll_length / 100)

    # LIVE CAMERA - Roll cholar somoy
    photo = st.camera_input("LIVE ROLL CAM - Auto Capture Cholche", label_visibility="collapsed")

    if photo is not None:
        # === AUTO DETECTION LOGIC ===
        # Ekhane AI model bosbe. Ekhon demo auto capture
        st.session_state.captured_images.append(photo)
        st.session_state.total += 1
        st.session_state.roll_length += 5 # proti capture e 5 gaj dhorlam
        st.session_state.faults["Hole"] += 1 # demo

        st.success(f"⚡ AUTO FAULT DETECTED! Photo #{st.session_state.total} Captured!")
        st.image(photo, caption=f"Fault #{st.session_state.total} - {roll_no}")

        if st.session_state.roll_length >= 100:
            st.session_state.auto_start = False
            st.balloons()
            st.success("✅ 100 GAJ COMPLETE!")
            st.rerun()
        else:
            time.sleep(0.5)
            st.rerun()

elif not cam_on:
    st.warning("🔴 Camera OFF - Machine Standby")
else:
    st.info("START ROLL Button chaple Machine cholbe")

# AUTO GALLERY + REPORT
st.divider()
st.subheader(f"📸 AUTO CAPTURED GALLERY - Total: {st.session_state.total} ta Fault")

if st.session_state.captured_images:
    cols = st.columns(3)
    for i, img in enumerate(st.session_state.captured_images[-6:]): # last 6 ta dekhabo
        with cols[i % 3]:
            st.image(img, caption=f"Fault {i+1}")

st.metric("100 Gaj e Total Fault", f"{st.session_state.total} ta")
st.table(pd.DataFrame(list(st.session_state.faults.items()), columns=["Fault", "Count"]))

if st.session_state.total == 0:
    st.success("RESULT: PASS - 100 Gaj Clear")
else:
    st.error(f"RESULT: FAIL - 100 Gaj e {st.session_state.total} ta Fault Auto Captured")

# FINAL REPORT
report = f"""MALEK 100 GAJ AUTO REPORT
Date: {datetime.now()}
Roll No: {roll_no}
Roll Length: 100 Gaj
Total Auto Captured Fault: {st.session_state.total}
Fault Details: {st.session_state.faults}
Total Photo Captured: {len(st.session_state.captured_images)}
Result: {'PASS' if st.session_state.total==0 else 'FAIL'}
"""
st.download_button("📥 DOWNLOAD 100 GAJ AUTO REPORT", report, file_name=f"AUTO_100GAJ_{roll_no}.txt", use_container_width=True)
