import streamlit as st
import math

# -------------------- Shared Calculation Function --------------------
def calculate_price(length, width, height, grammage, costing_tonnage, selling_tonnage, quantity, adjustment_percent):
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
        round(total_paper_length_m, 3),
        round(effective_width_per_piece_m, 3),
        round(costing_tonnage, 2),
        round(selling_tonnage, 2),
        grammage,
        pieces_per_roll,
        formula
    )

# -------------------- Streamlit UI --------------------
st.set_page_config(page_title="Carton Quotation App", layout="wide")
st.title("📦 Carton & Packaging Quotation Calculator")

menu = st.sidebar.radio("Select Calculation Type", [
    "Carton Box",
    "Pizza Box",
    "Layer Pad",
    "Nesting Fitting and Carton Design",
    "Using Sample Board",
    "Design Nesting and Layer Pad"
])

if menu == "Carton Box":
    st.header("Carton Box Calculation")
    length = st.number_input("Length (mm)", value=500.0)
    width = st.number_input("Width (mm)", value=300.0)
    height = st.number_input("Height (mm)", value=200.0)
    grammage = st.number_input("Grammage (g/m²)", value=0.84)
    costing_tonnage = st.number_input("Costing Tonnage", value=2.7)
    selling_tonnage = st.number_input("Selling Tonnage", value=3.4)
    quantity = st.number_input("Quantity", value=100)
    adjustment_percent = st.number_input("Adjustment %", value=0.0)

    if st.button("Calculate Carton Box"):
        result = calculate_price(length, width, height, grammage, costing_tonnage, selling_tonnage, quantity, adjustment_percent)
        st.write(f"**Cost per Piece:** RM {result[0]}")
        st.write(f"**Selling Price per Piece:** RM {result[1]}")
        st.write(f"**Total Price:** RM {result[2]}")
        st.write(f"**Formula:** {result[9]} = {result[1]}")

elif menu == "Pizza Box":
    st.header("Pizza Box Calculation")
    length = st.number_input("Pizza Box Length (mm)", value=300.0)
    width = st.number_input("Pizza Box Width (mm)", value=300.0)
    grammage = st.number_input("Grammage (g/m²)", value=0.84)
    costing_tonnage = st.number_input("Costing Tonnage", value=2.7)
    selling_tonnage = st.number_input("Selling Tonnage", value=3.4)
    quantity = st.number_input("Quantity", value=100)
    adjustment_percent = st.number_input("Adjustment %", value=0.0)

    if st.button("Calculate Pizza Box"):
        height = 0
        result = calculate_price(length + 20, width + 20, height, grammage, costing_tonnage, selling_tonnage, quantity, adjustment_percent)
        st.write(f"**Cost per Piece:** RM {result[0]}")
        st.write(f"**Selling Price per Piece:** RM {result[1]}")
        st.write(f"**Total Price:** RM {result[2]}")
        st.write(f"**Formula:** {result[9]} = {result[1]}")

elif menu == "Layer Pad":
    st.header("Layer Pad Calculation")
    length = st.number_input("Pad Length (mm)", value=500.0)
    width = st.number_input("Pad Width (mm)", value=300.0)
    grammage = st.number_input("Grammage (g/m²)", value=0.84)
    costing_tonnage = st.number_input("Costing Tonnage", value=2.7)
    selling_tonnage = st.number_input("Selling Tonnage", value=3.4)
    quantity = st.number_input("Quantity", value=100)
    adjustment_percent = st.number_input("Adjustment %", value=0.0)

    if st.button("Calculate Layer Pad"):
        height = 0
        result = calculate_price(length, width, height, grammage, costing_tonnage, selling_tonnage, quantity, adjustment_percent)
        st.write(f"**Cost per Piece:** RM {result[0]}")
        st.write(f"**Selling Price per Piece:** RM {result[1]}")
        st.write(f"**Total Price:** RM {result[2]}")
        st.write(f"**Formula:** {result[9]} = {result[1]}")

elif menu == "Nesting Fitting and Carton Design":
    st.header("Nesting Fitting and Carton Design")
    product_L = st.number_input("Product Length (mm)", value=800.0)
    product_W = st.number_input("Product Width (mm)", value=204.0)
    product_H = st.number_input("Product Height (mm)", value=10.0)
    include_bubble = st.checkbox("Include Bubble Wrap (10mm)?", value=True)
    thickness = st.number_input("Nesting Thickness (mm)", value=3.0)
    allowance = st.number_input("Nesting Allowance (mm)", value=40.0)
    qty_L = st.number_input("Qty in Length", value=1)
    qty_W = st.number_input("Qty in Width", value=1)
    qty_H = st.number_input("Qty in Height", value=10)
    layer_thick = st.number_input("Layer Pad Thickness (mm)", value=3.0)
    layer_qty = st.number_input("Number of Layer Pads", value=2)

    adj_L = product_L + 10 if include_bubble else product_L
    adj_W = product_W + 10 if include_bubble else product_W
    adj_H = product_H + 10 if include_bubble else product_H

    int_L = allowance + thickness + ((adj_L + thickness) * qty_L) + allowance
    int_W = allowance + thickness + ((adj_W + thickness) * qty_W) + allowance
    int_H = adj_H

    ext_L = int_L + 10
    ext_W = int_W + 10
    ext_H = int_H + 20 + (layer_thick * layer_qty)

    st.subheader("📊 Carton Size Output")
    st.write(f"Internal Size (L x W x H): {int_L:.2f} x {int_W:.2f} x {int_H:.2f} mm")
    st.write(f"External Size (L x W x H): {ext_L:.2f} x {ext_W:.2f} x {ext_H:.2f} mm")

    nesting_long_L = int_L
    nesting_long_W = int_H
    nesting_short_L = int_W
    nesting_short_W = int_H

    st.write(f"Nesting Long Size: {nesting_long_L:.2f} x {nesting_long_W:.2f} mm")
    st.write(f"Nesting Short Size: {nesting_short_L:.2f} x {nesting_short_W:.2f} mm")

if menu == "Using Sample Board":
    st.header("📦 Using Sample Board")
    board_L = st.number_input("Sample Board Length (mm)", value=2400.0)
    board_W = st.number_input("Sample Board Width (mm)", value=1322.0)
    grammage = st.number_input("Grammage", value=0.78)
    price_per_board = st.number_input("Price per Sample Board (RM)", value=5.95)
    product_L = st.number_input("Product Length (mm)", value=375.0)
    product_W = st.number_input("Product Width (mm)", value=310.0)
    order_qty = st.number_input("Customer Order Qty (pcs)", value=144)
    test_board_qty = st.number_input("Testing Quantity", value=2)
    job_cost = st.number_input("Job Setup Cost (RM)", value=60.0)
    margin_percent = st.number_input("Margin %", value=0.0)

    ups_L = int(board_L // product_L)
    ups_W = int(board_W // product_W)
    total_ups = ups_L * ups_W
    boards_needed = -(-order_qty // total_ups)  # Ceiling division
    total_boards = boards_needed + test_board_qty

    cost_per_piece = price_per_board / total_ups
    total_cost = total_boards * price_per_board + job_cost
    final_unit_price = (total_cost / order_qty) * (1 + margin_percent / 100)

    st.subheader("📊 Result")
    st.write(f"UPS (L x W): {ups_L} x {ups_W} = {total_ups} pcs/board")
    st.write(f"Boards Needed: {boards_needed} + {test_board_qty} (test) = {total_boards} boards")
    st.write(f"Cost per Piece (before margin): RM {total_cost / order_qty:.3f}")
    st.write(f"Final Unit Price (with margin): RM {final_unit_price:.3f}")

elif menu == "Design Nesting and Layer Pad":
    st.header("📦 Design Nesting and Layer Pad")
    ext_L = st.number_input("External Carton Length (mm)", value=600.0)
    ext_W = st.number_input("External Carton Width (mm)", value=500.0)
    ext_H = st.number_input("External Carton Height (mm)", value=215.0)
    pad_thickness = st.number_input("Layer Pad Thickness (mm)", value=3.0)
    pad_qty = st.number_input("Number of Layer Pads", value=3)

    prod_L = st.number_input("Product Length (mm)", value=800.0)
    prod_W = st.number_input("Product Width (mm)", value=204.0)
    prod_H = st.number_input("Product Height (mm)", value=10.0)
    use_bubble = st.checkbox("Include Bubble Wrap (10mm)?", value=False)

    adj_L = prod_L + 10 if use_bubble else prod_L
    adj_W = prod_W + 10 if use_bubble else prod_W
    adj_H = prod_H + 10 if use_bubble else prod_H

    int_L = ext_L - 10
    int_W = ext_W - 10
    int_H = ext_H - 20 - (pad_thickness * pad_qty)

    slot = 3
    bal_L = (int_L - adj_L - 2 * slot) / 2
    nest_long_L = round(bal_L + slot + adj_L + slot + bal_L)
    nest_long_W = int_H

    bal_W = (int_W - adj_W - 2 * slot) / 2
    nest_short_L = round(bal_W + slot + adj_W + slot + bal_W)
    nest_short_W = int_H

    st.subheader("📐 Calculated Sizes")
    st.write(f"Internal Carton Size: {int_L} x {int_W} x {int_H} mm")
    st.write(f"Adjusted Product Size: {adj_L} x {adj_W} x {adj_H} mm")
    st.write(f"Layer Pad Deduction: {pad_thickness} x {pad_qty} = {pad_thickness * pad_qty} mm")
    st.write(f"Nesting Long Size: {nest_long_L} x {nest_long_W} mm")
    st.write(f"Nesting Short Size: {nest_short_L} x {nest_short_W} mm")
