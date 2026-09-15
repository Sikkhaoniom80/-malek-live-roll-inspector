import streamlit as st
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Malek Live Roll Inspector", layout="centered")
st.title("MALEK LIVE ROLL INSPECTOR")

# 1. SETTINGS
st.subheader("1. Settings")
col1, col2 = st.columns(2)
with col1:
    room_type = st.selectbox("Room Type", ["Normal Room Check", "Dark Room Check"])
    light_power = st.slider("Light Power %", 0, 100, 60)
with col2:
    roll_no = st.text_input("Roll No", "Roll-001")
    factory = st.text_input("Factory", "Malek Factory")

date_str = datetime.now().strftime("%d-%m-%Y %H:%M")
st.info(f"Date: {date_str}")

# 2. 12 FAULT LIST
fault_names_12 = ["1. Hole","2. Slub","3. Thick/Thin Place","4. Oil Stain","5. Contamination","6. Crease Mark","7. Selvedge Defect","8. Reed Mark","9. Broken End","10. Double Pick","11. Weft Bar","12. Mispick"]
fault_counts = {name: 0 for name in fault_names_12}

# 3. CAMERA
st.divider()
st.subheader("3. Roll Scan")
camera_photo = st.camera_input("Click kore chobi tolo")
uploaded_photo = st.file_uploader("Othoba Gallery theke Upload koro", type=['jpg','jpeg','png'])
final_image = camera_photo or uploaded_photo
if final_image:
    st.image(final_image, use_column_width=True)

# 4. 12 FAULT DETAIL - EKHANEI HISAB
st.divider()
st.subheader("12 FAULT DETAIL HISAB - MAMA SPECIAL")
df_data = []
for name, count in fault_counts.items():
    df_data.append({"Fault Name": name, "Count": f"{count} ta", "Status": "OK" if count==0 else "FOUND"})
st.table(pd.DataFrame(df_data))

total_fault = sum(fault_counts.values())
col_a, col_b = st.columns(2)
col_a.metric("TOTAL FAULT", f"{total_fault} ta")
if total_fault == 0:
    col_b.success("RESULT: PASS (CLEAR)")
    result = "PASS"
    fault_summary = "CLEAR"
else:
    col_b.error(f"RESULT: FAIL - {total_fault} ta")
    result = "FAIL"
    fault_summary = ", ".join([f"{k}:{v}" for k,v in fault_counts.items() if v>0])

# 5. FINAL REPORT
st.divider()
st.subheader("FINAL QC REPORT")
st.write(f"**Room Type:** {room_type}")
st.write(f"**Light Power:** {light_power}%")
st.write(f"**Date:** {date_str}")
st.write(f"**Roll No:** {roll_no}")
st.write(f"**Factory:** {factory}")
st.write(f"**Total Fault:** {total_fault}")
st.write(f"**Fault Details:** {fault_summary}")
st.write(f"**Result:** {result}")

report_text = f"Date: {date_str}\nRoll: {roll_no}\nFactory: {factory}\n"
for k,v in fault_counts.items():
    report_text += f"{k}: {v} ta\n"
report_text += f"\nTOTAL: {total_fault}\nRESULT: {result}\n"
st.download_button("PRINT REPORT / DOWNLOAD", report_text, file_name=f"QC_{roll_no}.txt")
