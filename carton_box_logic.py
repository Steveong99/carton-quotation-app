
import streamlit as st
import math

def calculate_carton_box_price(length, width, height, grammage, costing_tonnage, selling_tonnage, quantity, adjustment_percent):
    total_paper_length = (length + width) * 2 + 30  # mm
    raw_width = width + height + 4  # mm
    total_paper_length_m = round(total_paper_length / 1000, 3)

    max_roll_width = 2200
    trim_allowance = 28 if grammage > 0.77 else 25
    pieces_per_roll = math.floor(max_roll_width / raw_width)
    total_used_width = raw_width * pieces_per_roll
    trimmed_total_width = total_used_width + trim_allowance
    rounded_roll_width = math.ceil(trimmed_total_width / 50) * 50
    effective_width_per_piece_m = round(rounded_roll_width / pieces_per_roll / 1000, 3)

    cost_price = total_paper_length_m * effective_width_per_piece_m * grammage * costing_tonnage
    base_unit_price = total_paper_length_m * effective_width_per_piece_m * grammage * selling_tonnage
    adjusted_unit_price = base_unit_price * (1 + adjustment_percent / 100)
    total_price = adjusted_unit_price * quantity

    formula = f"{total_paper_length_m} x {effective_width_per_piece_m} x {grammage} x {selling_tonnage} x (1 + {adjustment_percent / 100:.2f})"

    return (
        round(cost_price, 2),
        round(adjusted_unit_price, 2),
        round(total_price, 2),
        total_paper_length_m,
        effective_width_per_piece_m,
        pieces_per_roll,
        formula
    )

st.set_page_config(page_title="Carton Box Calculator", layout="wide")
st.title("📦 Carton Box Price Calculator")

st.header("Enter Carton Dimensions and Parameters")
length = st.number_input("Length (mm)", value=500.0)
width = st.number_input("Width (mm)", value=300.0)
height = st.number_input("Height (mm)", value=200.0)
grammage = st.number_input("Grammage (g/m²)", value=0.84)
costing_tonnage = st.number_input("Costing Tonnage", value=2.7)
selling_tonnage = st.number_input("Selling Tonnage", value=3.4)
quantity = st.number_input("Quantity", value=100)
adjustment_percent = st.number_input("Adjustment %", value=0.0)

if st.button("Calculate Carton Box"):
    result = calculate_carton_box_price(length, width, height, grammage, costing_tonnage, selling_tonnage, quantity, adjustment_percent)
    st.subheader("🧾 Results")
    st.write(f"**Cost per Piece:** RM {result[0]}")
    st.write(f"**Selling Price per Piece:** RM {result[1]}")
    st.write(f"**Total Price:** RM {result[2]}")
    st.write(f"**Formula:** {result[6]} = RM {result[1]}")
    st.write(f"**Paper Length (m):** {result[3]}")
    st.write(f"**Paper Actual Width (m):** {result[4]}")
    st.write(f"**UPS (pieces per roll):** {result[5]}")
