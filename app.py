import streamlit as st
import cv2
import numpy as np
from PIL import Image
from datetime import datetime

st.set_page_config(page_title="Malek Live Roll Inspector", layout="centered")
st.markdown("<style>@media print{header,footer,.stCameraInput,.stRadio,.stToggle,.stSlider,button{display:none!important;}}</style>", unsafe_allow_html=True)

st.title("🏭 Malek Live Roll Inspector")
st.caption("Fault | Print | Room | Light Room - All in One")

st.markdown("### 🏠 1. Room Selection")
room_type = st.radio("কোথায় চেক করবা?", ["🏠 Normal Room Check", "💡 Light Room Check"], horizontal=True)

if "Light Room" in room_type:
    st.success("💡 Light Room ON - Factory Standard!")
    light_power = st.slider("💡 Light Power", 0, 100, 85)
    threshold_val = 20
    st.markdown(f'<div style="background:black; padding:12px; border-radius:8px; text-align:center; border:2px solid yellow;"><span style="color:yellow; font-weight:bold;">💡 LIGHT ROOM: {light_power}% | 🔴 LIVE</span></div>', unsafe_allow_html=True)
else:
    light_power = st.slider("🔦 Room Light", 0, 100, 60)
    threshold_val = 30
    st.markdown(f'<div style="background:#444; padding:12px; border-radius:8px; text-align:center;"><span style="color:white;">🏠 NORMAL ROOM: {light_power}%</span></div>', unsafe_allow_html=True)

st.markdown("### ⚠️ 2. Factory 12 Fault List")
st.info("Hole/ফুটা, Slub/গুটি, Oil Stain, Contamination, Thick/Thin, Crease, Selvedge, Broken End, Weft Bar, Stain, Missing Yarn, Temple Mark")

machine_on = st.toggle("⚙️ 3. MACHINE START")
if not machine_on:
    st.warning("Machine ON করো মামা!")
    st.stop()

st.success("🔴 MACHINE চলছে...")

cam = st.camera_input("📸 4. ROLL SCAN")

if cam:
    img = Image.open(cam)
    frame = np.array(img)
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (21,21), 0)
    diff = cv2.absdiff(gray, blur)
    _, thresh = cv2.threshold(diff, threshold_val, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    faults_found = []
    for c in contours:
        area = cv2.contourArea(c)
        if area > 700:
            x,y,w,h = cv2.boundingRect(c)
            if area > 6000: name = "Hole/ফুটা"
            elif area > 3500: name = "Oil Stain"
            elif area > 2000: name = "Slub/গুটি"
            elif area > 1200: name = "Contamination"
            else: name = "Thick/Thin"
            faults_found.append(name)
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 3)
            cv2.putText(frame, name, (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
    st.image(frame, use_container_width=True)
    if faults_found:
        st.error(f"⚠️ {len(faults_found)} টা FAULT!")
    else:
        st.success("✅ ROLL CLEAR - PASS")

    st.divider()
    st.markdown("### 🖨️ 5. Print Report")
    roll_no = st.text_input("Roll No:", "Roll-001")
    buyer = st.text_input("Factory/Buyer:", "Malek Factory")
    now = datetime.now().strftime("%d-%m-%Y %H:%M")
    fault_str = ", ".join(faults_found) if faults_found else "CLEAR"
    result = "FAIL" if faults_found else "PASS"
    report = f'<div style="border:2px solid black; padding:20px; background:white; color:black;"><h2 style="text-align:center;">🏭 Malek Fabrics - Inspection Report</h2><p><b>Room Type:</b> {room_type}</p><p><b>Light Power:</b> {light_power}%</p><p><b>Date:</b> {now}</p><p><b>Roll No:</b> {roll_no}</p><p><b>Factory:</b> {buyer}</p><hr><p><b>12 Fault:</b> Hole, Slub, Oil, Contamination, Thick/Thin, Crease, Selvedge, Broken End, Weft Bar, Stain, Missing Yarn, Temple Mark</p><p><b>Total:</b> {len(faults_found)}</p><p><b>Fault Names:</b> {fault_str}</p><p><b>Result:</b> <b style="font-size:18px;">{result}</b></p><br><p>QC Sign: ___________ Manager: ___________</p></div>'
    st.markdown(report, unsafe_allow_html=True)
    st.markdown('<button onclick="window.print()" style="background:red; color:white; padding:15px; width:100%; font-size:20px; border:none; border-radius:10px; font-weight:bold; margin-top:10px;">🖨️ PRINT REPORT</button>', unsafe_allow_html=True)
else:
    st.info("📸 Camera তে Roll ধরো মামা")
