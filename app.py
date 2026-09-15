import streamlit as st
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Malek Roll Inspector", layout="centered")
st.title("MALEK LIVE ROLL INSPECTOR")

# 1. Settings
st.subheader("1. Settings")
room_type = st.selectbox("Room Type", ["Normal Room Check", "Dark Room Check"])
light_power = st.slider("Light Power %", 0, 100, 60)
roll_no = st.text_input("Roll No", "Roll-001")
factory = st.text_input("Factory", "Malek Factory")
date_str = datetime.now().strftime("%d-%m-%Y %H:%M")
st.info(f"Date: {date_str}")

# 2. Scan
st.divider()
st.subheader("3. Roll Scan")
st.write("Click kore chobi tolo")
camera_photo = st.camera_input("Camera", label_visibility="collapsed")

st.write("Othoba Gallery theke Upload koro")
uploaded_photo = st.file_uploader("Upload", type=['jpg','jpeg','png'], label_visibility="collapsed")

final_image = camera_photo if camera_photo is not None else uploaded_photo
if final_image is not None:
    st.image(final_image, caption="Roll Image")

# 3. 12 Fault Input
st.divider()
st.subheader("12 FAULT DETAIL HISAB - MAMA")

c1, c2 = st.columns(2)
with c1:
    hole = st.number_input("1. Hole", 0, 100, 0)
    slub = st.number_input("2. Slub", 0, 100, 0)
    thick = st.number_input("3. Thick Place", 0, 100, 0)
    oil = st.number_input("4. Oil Stain", 0, 100, 0)
    cont = st.number_input("5. Contamination", 0, 100, 0)
    crease = st.number_input("6. Crease", 0, 100, 0)
with c2:
    selvedge = st.number_input("7. Selvedge", 0, 100, 0)
    reed = st.number_input("8. Reed Mark", 0, 100, 0)
    broken = st.number_input("9. Broken End", 0, 100, 0)
    double = st.number_input("10. Double Pick", 0, 100, 0)
    weft = st.number_input("11. Weft Bar", 0, 100, 0)
    mispick = st.number_input("12. Mispick", 0, 100, 0)

fault_list = [
    ["1. Hole", hole],
    ["2. Slub", slub],
    ["3. Thick Place", thick],
    ["4. Oil Stain", oil],
    ["5. Contamination", cont],
    ["6. Crease", crease],
    ["7. Selvedge", selvedge],
    ["8. Reed Mark", reed],
    ["9. Broken End", broken],
    ["10. Double Pick", double],
    ["11. Weft Bar", weft],
    ["12. Mispick", mispick],
]

df = pd.DataFrame(fault_list, columns=["Fault Name", "Count"])
st.table(df)

total = hole+slub+thick+oil+cont+crease+selvedge+reed+broken+double+weft+mispick
st.metric("TOTAL FAULT", f"{total} ta")

if total == 0:
    st.success("RESULT: PASS (CLEAR)")
    result = "PASS"
else:
    st.error(f"RESULT: FAIL - {total} ta Fault")
    result = "FAIL"

# 4. Final Report
st.divider()
st.subheader("FINAL QC REPORT")
st.write(f"Room: {room_type} | Light: {light_power}%")
st.write(f"Roll: {roll_no} | Factory: {factory}")
st.write(f"Total: {total} | Result: {result}")

report = f"""MALEK FACTORY QC REPORT
Date: {date_str}
Roll No: {roll_no}
Factory: {factory}
Room Type: {room_type}
Light: {light_power}%

12 FAULT DETAILS:
1. Hole: {hole}
2. Slub: {slub}
3. Thick: {thick}
4. Oil: {oil}
5. Contamination: {cont}
6. Crease: {crease}
7. Selvedge: {selvedge}
8. Reed: {reed}
9. Broken End: {broken}
10. Double Pick: {double}
11. Weft Bar: {weft}
12. Mispick: {mispick}

TOTAL: {total}
RESULT: {result}
"""
st.download_button("PRINT / DOWNLOAD REPORT", report, file_name=f"QC_{roll_no}.txt")
