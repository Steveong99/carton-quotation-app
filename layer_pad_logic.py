
import streamlit as st
import math

def calculate_layer_pad_price(length, width, grammage, costing_tonnage, selling_tonnage, quantity, adjustment_percent):
    paper_length_m = round(length / 1000, 3)
    paper_width_m = round(width / 1000, 3)
    cost_price = paper_length_m * paper_width_m * grammage * costing_tonnage
    base_price = paper_length_m * paper_width_m * grammage * selling_tonnage
    adjusted_price = base_price * (1 + adjustment_percent / 100)
    total_price = adjusted_price * quantity
    formula = f"{paper_length_m} x {paper_width_m} x {grammage} x {selling_tonnage} x (1 + {adjustment_percent / 100:.2f})"
    return round(cost_price, 2), round(adjusted_price, 2), round(total_price, 2), formula

st.set_page_config(page_title="Layer Pad Calculator", layout="wide")
st.title("🧾 Layer Pad Calculation")

length = st.number_input("Length (mm)", value=500.0)
width = st.number_input("Width (mm)", value=300.0)
grammage = st.number_input("Grammage (g/m²)", value=0.84)
costing_tonnage = st.number_input("Costing Tonnage", value=2.7)
selling_tonnage = st.number_input("Selling Tonnage", value=3.4)
quantity = st.number_input("Quantity", value=100)
adjustment_percent = st.number_input("Adjustment %", value=0.0)

if st.button("Calculate Layer Pad"):
    cp, sp, tp, formula = calculate_layer_pad_price(length, width, grammage, costing_tonnage, selling_tonnage, quantity, adjustment_percent)
    st.write(f"**Cost per Piece:** RM {cp}")
    st.write(f"**Selling Price per Piece:** RM {sp}")
    st.write(f"**Total Price:** RM {tp}")
    st.write(f"**Formula:** {formula}")
