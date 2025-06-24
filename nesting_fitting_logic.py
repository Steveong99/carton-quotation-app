
import streamlit as st

def calculate_nesting_fitting(product_L, product_W, product_H, include_bubble, thickness, allowance,
                              qty_L, qty_W, qty_H, layer_thick, layer_qty):
    adj_L = product_L + 10 if include_bubble else product_L
    adj_W = product_W + 10 if include_bubble else product_W
    adj_H = product_H + 10 if include_bubble else product_H

    int_L = allowance + thickness + ((adj_L + thickness) * qty_L) + allowance
    int_W = allowance + thickness + ((adj_W + thickness) * qty_W) + allowance
    int_H = adj_H

    ext_L = int_L + 10
    ext_W = int_W + 10
    ext_H = int_H + 20 + (layer_thick * layer_qty)

    nesting_long = (int_L, int_H)
    nesting_short = (int_W, int_H)

    return {
        "Internal Size": (int_L, int_W, int_H),
        "External Size": (ext_L, ext_W, ext_H),
        "Nesting Long": nesting_long,
        "Nesting Short": nesting_short
    }

st.set_page_config(page_title="Nesting Fitting & Carton Design", layout="wide")
st.title("📏 Nesting Fitting and Carton Design")

with st.form("nesting_fitting_form"):
    st.subheader("Product Info")
    product_L = st.number_input("Product Length (mm)", value=800.0)
    product_W = st.number_input("Product Width (mm)", value=204.0)
    product_H = st.number_input("Product Height (mm)", value=10.0)
    include_bubble = st.checkbox("Include Bubble Wrap (10mm)?", value=True)

    st.subheader("Nesting & Carton Parameters")
    thickness = st.number_input("Slot Thickness (mm)", value=3.0)
    allowance = st.number_input("Allowance (mm)", value=40.0)
    qty_L = st.number_input("Qty in Length", value=1)
    qty_W = st.number_input("Qty in Width", value=1)
    qty_H = st.number_input("Qty in Height", value=10)
    layer_thick = st.number_input("Layer Pad Thickness (mm)", value=3.0)
    layer_qty = st.number_input("Number of Layer Pads", value=2)

    submitted = st.form_submit_button("Calculate")

if submitted:
    result = calculate_nesting_fitting(
        product_L, product_W, product_H, include_bubble,
        thickness, allowance, qty_L, qty_W, qty_H, layer_thick, layer_qty
    )

    st.subheader("📐 Internal Dimensions")
    st.write(f"L x W x H: {result['Internal Size'][0]:.1f} x {result['Internal Size'][1]:.1f} x {result['Internal Size'][2]:.1f} mm")

    st.subheader("📦 External Dimensions")
    st.write(f"L x W x H: {result['External Size'][0]:.1f} x {result['External Size'][1]:.1f} x {result['External Size'][2]:.1f} mm")

    st.subheader("🧩 Nesting Components")
    st.write(f"Nesting Long: {result['Nesting Long'][0]:.1f} x {result['Nesting Long'][1]:.1f} mm")
    st.write(f"Nesting Short: {result['Nesting Short'][0]:.1f} x {result['Nesting Short'][1]:.1f} mm")
