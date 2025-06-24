import streamlit as st
import math

def calculate_nesting_design(product_L, product_W, product_H, include_bubble, nesting_thickness, allowance, qty_per_box, carton_ext_L, carton_ext_W, carton_ext_H, product_weight):
    # Adjust product dimensions with bubble wrap
    adj_L = product_L + 10 if include_bubble else product_L
    adj_W = product_W + 10 if include_bubble else product_W
    adj_H = product_H + 10 if include_bubble else product_H

    # Keep original orientation
    packed_L = adj_L
    packed_W = adj_W
    packed_H = adj_H

    # Convert carton external to internal dimensions
    carton_int_L = carton_ext_L - 10
    carton_int_W = carton_ext_W - 10
    carton_int_H = carton_ext_H - 20

    # Calculate how many units fit
    fit_L = math.floor(carton_int_L / packed_L)
    fit_W = math.floor(carton_int_W / packed_W)
    fit_H = math.floor(carton_int_H / packed_H)
    total_fit = fit_L * fit_W * fit_H

    # Nesting Long Calculation
    balance_L = (carton_int_L - packed_L - 2 * nesting_thickness) / 2
    nesting_long_length = balance_L + nesting_thickness + packed_L + nesting_thickness + balance_L

    if fit_H > 0:
        nesting_each_height = (carton_int_H - (fit_H + 1) * nesting_thickness) / fit_H
        nesting_long_width = nesting_each_height
        layer_pad_quantity = fit_H + 1
    else:
        nesting_long_width = packed_H
        nesting_each_height = 0
        layer_pad_quantity = 2

    long_formula = f"{balance_L:.1f} + {nesting_thickness} + {packed_L} + {nesting_thickness} + {balance_L:.1f} = {nesting_long_length:.1f}"

    # Nesting Short Calculation
    nesting_short_length = carton_int_W
    nesting_short_width = nesting_long_width
    short_formula = f"Same width as long nesting: {nesting_short_width:.1f}"

    # Layer pad size
    layer_pad_length = carton_int_L
    layer_pad_width = carton_int_W

    total_carton_weight = total_fit * product_weight

    return (
        round(nesting_long_length, 2),
        round(nesting_long_width, 2),
        round(nesting_short_length, 2),
        round(nesting_short_width, 2),
        round(layer_pad_length, 2),
        round(layer_pad_width, 2),
        round(nesting_each_height, 2),
        layer_pad_quantity,
        fit_L, fit_W, fit_H, total_fit,
        carton_int_L, carton_int_W, carton_int_H,
        long_formula, short_formula,
        round(total_carton_weight, 2)
    )

# -------------------- Streamlit UI --------------------
st.set_page_config(page_title="Nesting Design Calculator", layout="wide")
st.title("📦 Nesting Design Calculator")

st.header("Input Customer Product Dimensions")
product_L = st.number_input("Product Length (mm)", value=800.0)
product_W = st.number_input("Product Width (mm)", value=204.0)
product_H = st.number_input("Product Height (mm)", value=10.0)
include_bubble = st.checkbox("Include Bubble Wrap (Add 10mm to each side)", value=True)

st.header("Input Carton External Dimensions")
carton_ext_L = st.number_input("Carton External Length (mm)", value=600.0)
carton_ext_W = st.number_input("Carton External Width (mm)", value=500.0)
carton_ext_H = st.number_input("Carton External Height (mm)", value=300.0)

st.header("Design Parameters")
nesting_thickness = st.number_input("Nesting Thickness (mm)", value=3.0)
allowance = st.number_input("Balance Allowance (mm)", value=30.0)
qty_per_box = st.number_input("Product Quantity in One Box", value=10)
product_weight = st.number_input("Product Weight (kg)", value=1.0)

if st.button("Calculate Nesting Design"):
    long_L, long_W, short_L, short_W, pad_L, pad_W, nest_H, pad_qty, fit_L, fit_W, fit_H, total_fit, int_L, int_W, int_H, long_formula, short_formula, total_carton_weight = calculate_nesting_design(
        product_L, product_W, product_H,
        include_bubble, nesting_thickness,
        allowance, qty_per_box,
        carton_ext_L, carton_ext_W, carton_ext_H,
        product_weight
    )

    st.subheader("📏 Nesting Output")
    st.write(f"Nesting Long Size: {long_L} x {long_W} mm")
    st.write(f"Formula: {long_formula}")
    st.write(f"Nesting Short Size: {short_L} x {short_W} mm")
    st.write(f"Formula: {short_formula}")

    st.subheader("🧱 Layer Pad Design")
    st.write(f"Layer Pad Size: {pad_L} x {pad_W} mm")
    st.write(f"Layer Pad Quantity: {pad_qty}")
    st.write(f"Nesting Height Per Layer: {nest_H} mm")

    st.subheader("📦 Fitment Info")
    st.write(f"Internal Carton Size: {int_L} x {int_W} x {int_H} mm")
    st.write(f"Units that fit (L×W×H): {fit_L} × {fit_W} × {fit_H} = {total_fit} units")
    st.write(f"Total Carton Weight: {total_carton_weight:.2f} kg")
