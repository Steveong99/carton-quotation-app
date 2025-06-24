
import streamlit as st
import math

def calculate_pizza_box_price(length, width, grammage, costing_tonnage, selling_tonnage, quantity, adjustment_percent):
    paper_length_mm = length + 20
    paper_width_mm = width + 20
    trimming_allowance = 28
    ups = math.floor(2200 / paper_width_mm)
    total_width_used = paper_width_mm * ups
    roll_width_with_trim = total_width_used + trimming_allowance
    rounded_roll_width = math.ceil(roll_width_with_trim / 50) * 50
    paper_actual_width = rounded_roll_width / ups
    paper_length_m = round(paper_length_mm / 1000, 3)
    paper_width_m = round(paper_actual_width / 1000, 3)
    cost_price = paper_length_m * paper_width_m * grammage * costing_tonnage
    base_unit_price = paper_length_m * paper_width_m * grammage * selling_tonnage
    adjusted_unit_price = base_unit_price * (1 + adjustment_percent / 100)
    total_price = adjusted_unit_price * quantity
    formula = f"{paper_length_m} x {paper_width_m} x {grammage} x {selling_tonnage} x (1 + {adjustment_percent / 100:.2f})"
    return (
        round(cost_price, 2),
        round(adjusted_unit_price, 2),
        round(total_price, 2),
        round(paper_length_m, 3),
        round(paper_width_m, 3),
        ups,
        formula
    )

st.set_page_config(page_title="Pizza Box Calculation", layout="wide")
st.title("📦 Pizza Box Calculator")

length = st.number_input("Pizza Box Length (mm)", value=300.0)
width = st.number_input("Pizza Box Width (mm)", value=300.0)
grammage = st.number_input("Grammage (g/m²)", value=0.84)
costing_tonnage = st.number_input("Costing Tonnage", value=2.7)
selling_tonnage = st.number_input("Selling Tonnage", value=3.4)
quantity = st.number_input("Quantity", value=100)
adjustment_percent = st.number_input("Adjustment %", value=0.0)

if st.button("Calculate Pizza Box"):
    result = calculate_pizza_box_price(length, width, grammage, costing_tonnage, selling_tonnage, quantity, adjustment_percent)
    st.write(f"**Cost per Piece:** RM {result[0]}")
    st.write(f"**Selling Price per Piece:** RM {result[1]}")
    st.write(f"**Total Price:** RM {result[2]}")
    st.write(f"**Formula:** {result[6]} = {result[1]}")
    st.write(f"**Paper Length (m):** {result[3]} | **Paper Actual Width (m):** {result[4]} | **UPS:** {result[5]}")
