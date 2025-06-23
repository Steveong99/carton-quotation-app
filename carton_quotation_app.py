import streamlit as st
import math

# ==================== CONSTANTS ====================
TRIM_ALLOWANCE = 28
MAX_ROLL_WIDTH = 2200

# ==================== CALCULATION FUNCTIONS ====================
def calculate_standard_box(length, width, height, grammage, costing, selling, quantity, adjustment):
    paper_length = (length + width) * 2 + 30
    raw_width = width + height + 4
    total_paper_length_m = round(paper_length / 1000, 3)
    pieces_per_roll = math.floor(MAX_ROLL_WIDTH / raw_width)
    total_used_width = raw_width * pieces_per_roll
    trimmed_total_width = total_used_width + TRIM_ALLOWANCE
    rounded_roll_width = math.ceil(trimmed_total_width / 50) * 50
    effective_width_per_piece_m = round(rounded_roll_width / pieces_per_roll / 1000, 3)

    cost_price = total_paper_length_m * effective_width_per_piece_m * grammage * costing
    base_unit_price = total_paper_length_m * effective_width_per_piece_m * grammage * selling
    adjusted_unit_price = base_unit_price * (1 + adjustment / 100)
    total_price = adjusted_unit_price * quantity

    formula = f"{total_paper_length_m} x {effective_width_per_piece_m} x {grammage} x {selling} x (1 + {adjustment / 100:.2f})"

    return cost_price, adjusted_unit_price, total_price, formula

def calculate_pizza_box(length, width, grammage, costing, selling, quantity, adjustment):
    paper_length = length + 20
    paper_width = width + 20
    ups = math.floor(MAX_ROLL_WIDTH / paper_width)
    total_used = paper_width * ups
    roll_width = math.ceil((total_used + TRIM_ALLOWANCE) / 50) * 50
    actual_width = roll_width / ups

    paper_length_m = paper_length / 1000
    actual_width_m = actual_width / 1000

    cost = paper_length_m * actual_width_m * grammage * costing
    price = paper_length_m * actual_width_m * grammage * selling * (1 + adjustment/100)

    return cost, price, price * quantity, paper_length_m, actual_width_m, ups

def calculate_layer_pad(length, width, grammage, costing, selling, quantity, adjustment):
    return calculate_standard_box(length, width, 0, grammage, costing, selling, quantity, adjustment)

def calculate_nesting(product_L, product_W, product_H, bubble, thickness, allowance, qty_L, qty_W, qty_H, layer_thick, layer_qty):
    adj_L = product_L + 10 if bubble else product_L
    adj_W = product_W + 10 if bubble else product_W
    adj_H = product_H + 10 if bubble else product_H

    int_L = allowance + thickness + ((adj_L + thickness) * qty_L) + allowance
    int_W = allowance + thickness + ((adj_W + thickness) * qty_W) + allowance
    int_H = adj_H

    ext_L = int_L + 10
    ext_W = int_W + 10
    ext_H = int_H + 20 + (layer_thick * layer_qty)

    nesting_long = (int_L, int_H)
    nesting_short = (int_W, int_H)

    return int_L, int_W, int_H, ext_L, ext_W, ext_H, nesting_long, nesting_short

def calculate_sample_board(length, width, ups, grammage, costing, selling, quantity, adjustment):
    board_area = (length * width * ups) / 1000000
    cost_price = board_area * grammage * costing
    selling_price = board_area * grammage * selling * (1 + adjustment/100)
    total_price = selling_price * quantity
    return cost_price, selling_price, total_price

def calculate_design_nesting_layer_pad(ext_L, ext_W, ext_H, layer_thick, layer_qty, product_L, product_W, product_H, bubble):
    adj_L = product_L + 10 if bubble else product_L
    adj_W = product_W + 10 if bubble else product_W
    adj_H = product_H + 10 if bubble else product_H

    int_L = ext_L - 10
    int_W = ext_W - 10
    int_H = ext_H - 20 - (layer_thick * layer_qty)

    slot = 3
    bal_L = (int_L - adj_L - 2 * slot) / 2
    nesting_long_L = round(bal_L + slot + adj_L + slot + bal_L)

    bal_W = (int_W - adj_W - 2 * slot) / 2
    nesting_short_L = round(bal_W + slot + adj_W + slot + bal_W)

    return int_L, int_W, int_H, adj_L, adj_W, adj_H, nesting_long_L, int_H, nesting_short_L, int_H

# ==================== UI ====================
st.set_page_config(page_title="Carton Quotation App", layout="wide")
st.title("📦 Carton & Packaging Quotation Calculator")

menu = st.sidebar.radio("Select Calculation Type", [
    "Carton Box", "Pizza Box", "Layer Pad",
    "Nesting Fitting and Carton Design",
    "Using Sample Board", "Design Nesting and Layer Pad"
])

if menu == "Carton Box":
    st.header("Carton Box Calculation")
    L = st.number_input("Length (mm)", value=500.0)
    W = st.number_input("Width (mm)", value=300.0)
    H = st.number_input("Height (mm)", value=200.0)
    G = st.number_input("Grammage (g/m²)", value=0.84)
    C = st.number_input("Costing Tonnage", value=2.7)
    S = st.number_input("Selling Tonnage", value=3.4)
    Q = st.number_input("Quantity", value=100)
    A = st.number_input("Adjustment %", value=0.0)

    if st.button("Calculate Carton Box"):
        cp, sp, tp, f = calculate_standard_box(L, W, H, G, C, S, Q, A)
        st.write(f"Cost: RM {cp:.2f}, Price: RM {sp:.2f}, Total: RM {tp:.2f}")
        st.write(f"Formula: {f}")

elif menu == "Pizza Box":
    st.header("Pizza Box Calculation")
    L = st.number_input("Pizza Length (mm)", value=300.0)
    W = st.number_input("Pizza Width (mm)", value=300.0)
    G = st.number_input("Grammage (g/m²)", value=0.84)
    C = st.number_input("Costing Tonnage", value=2.7)
    S = st.number_input("Selling Tonnage", value=3.4)
    Q = st.number_input("Quantity", value=100)
    A = st.number_input("Adjustment %", value=0.0)

    if st.button("Calculate Pizza Box"):
        cp, sp, tp, pl, pw, ups = calculate_pizza_box(L, W, G, C, S, Q, A)
        st.write(f"Cost: RM {cp:.2f}, Price: RM {sp:.2f}, Total: RM {tp:.2f}")
        st.write(f"Paper Length: {pl:.3f}m, Actual Width: {pw:.3f}m, UPS: {ups}")

elif menu == "Layer Pad":
    st.header("Layer Pad Calculation")
    L = st.number_input("Pad Length (mm)", value=500.0)
    W = st.number_input("Pad Width (mm)", value=300.0)
    G = st.number_input("Grammage (g/m²)", value=0.84)
    C = st.number_input("Costing Tonnage", value=2.7)
    S = st.number_input("Selling Tonnage", value=3.4)
    Q = st.number_input("Quantity", value=100)
    A = st.number_input("Adjustment %", value=0.0)

    if st.button("Calculate Layer Pad"):
        cp, sp, tp, f = calculate_layer_pad(L, W, G, C, S, Q, A)
        st.write(f"Cost: RM {cp:.2f}, Price: RM {sp:.2f}, Total: RM {tp:.2f}")
        st.write(f"Formula: {f}")

elif menu == "Nesting Fitting and Carton Design":
    st.header("Nesting Fitting and Carton Design")
    PL = st.number_input("Product Length (mm)", value=800.0)
    PW = st.number_input("Product Width (mm)", value=204.0)
    PH = st.number_input("Product Height (mm)", value=10.0)
    bubble = st.checkbox("Add Bubble Wrap (10mm)?", value=True)
    thick = st.number_input("Nesting Thickness (mm)", value=3.0)
    allow = st.number_input("Nesting Allowance (mm)", value=40.0)
    qtyL = st.number_input("Qty in Length", value=1)
    qtyW = st.number_input("Qty in Width", value=1)
    qtyH = st.number_input("Qty in Height", value=10)
    layerT = st.number_input("Layer Pad Thickness (mm)", value=3.0)
    layerQty = st.number_input("Number of Layer Pads", value=2)

    if st.button("Calculate Nesting"):
        iL, iW, iH, eL, eW, eH, nL, nS = calculate_nesting(PL, PW, PH, bubble, thick, allow, qtyL, qtyW, qtyH, layerT, layerQty)
        st.write(f"Internal: {iL:.1f} x {iW:.1f} x {iH:.1f}")
        st.write(f"External: {eL:.1f} x {eW:.1f} x {eH:.1f}")
        st.write(f"Nesting Long: {nL[0]:.1f} x {nL[1]:.1f} mm")
        st.write(f"Nesting Short: {nS[0]:.1f} x {nS[1]:.1f} mm")

elif menu == "Using Sample Board":
    st.header("Sample Board Calculation")
    L = st.number_input("Board Length (mm)", value=500.0)
    W = st.number_input("Board Width (mm)", value=300.0)
    UPS = st.number_input("UPS", value=4)
    G = st.number_input("Grammage (g/m²)", value=0.84)
    C = st.number_input("Costing Tonnage", value=2.7)
    S = st.number_input("Selling Tonnage", value=3.4)
    Q = st.number_input("Quantity", value=100)
    A = st.number_input("Adjustment %", value=0.0)

    if st.button("Calculate Sample Board"):
        cp, sp, tp = calculate_sample_board(L, W, UPS, G, C, S, Q, A)
        st.write(f"Cost: RM {cp:.2f}, Price: RM {sp:.2f}, Total: RM {tp:.2f}")

elif menu == "Design Nesting and Layer Pad":
    st.header("Design Nesting and Layer Pad")
    extL = st.number_input("External Length (mm)", value=600.0)
    extW = st.number_input("External Width (mm)", value=500.0)
    extH = st.number_input("External Height (mm)", value=215.0)
    layerT = st.number_input("Layer Pad Thickness (mm)", value=3.0)
    layerQ = st.number_input("Number of Layer Pads", value=3)
    prodL = st.number_input("Product Length (mm)", value=800.0)
    prodW = st.number_input("Product Width (mm)", value=204.0)
    prodH = st.number_input("Product Height (mm)", value=10.0)
    bubble = st.checkbox("Add Bubble Wrap (10mm)?", value=False)

    if st.button("Calculate Design Nesting"):
        iL, iW, iH, aL, aW, aH, nLL, nLW, nSL, nSW = calculate_design_nesting_layer_pad(extL, extW, extH, layerT, layerQ, prodL, prodW, prodH, bubble)
        st.write(f"Internal Size: {iL} x {iW} x {iH}")
        st.write(f"Adjusted Product: {aL} x {aW} x {aH}")
        st.write(f"Nesting Long: {nLL} x {nLW} mm")
        st.write(f"Nesting Short: {nSL} x {nSW} mm")
