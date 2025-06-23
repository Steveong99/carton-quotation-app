import streamlit as st
import math
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

# -------------------- Enums & Constants --------------------
class CalculationType(Enum):
    CARTON_BOX = "Carton Box"
    PIZZA_BOX = "Pizza Box"
    LAYER_PAD = "Layer Pad"
    NESTING_DESIGN = "Nesting Design"
    SAMPLE_BOARD = "Sample Board"
    NESTING_LAYER_PAD = "Nesting & Layer Pad"

DEFAULT_TRIM_ALLOWANCE = {'low': 25, 'high': 28}
MAX_ROLL_WIDTH = 2200  # mm
PIZZA_FLAP_EXTENSION = 20  # mm

# -------------------- Data Structures --------------------
@dataclass
class PriceResult:
    cost_price: float
    selling_price: float
    total_price: float
    dimensions: str
    formula: str
    production_metrics: dict

@dataclass
class DesignResult:
    internal_size: str
    external_size: str
    nesting_sizes: dict
    material_usage: dict

# -------------------- Core Calculations --------------------
def calculate_box_price(length, width, height, grammage, costing, selling, quantity, adjustment):
    """Universal box pricing calculation"""
    total_paper = (length + width) * 2 + 30
    raw_width = width + height + 4
    paper_length_m = round(total_paper / 1000, 3)

    trim = DEFAULT_TRIM_ALLOWANCE['high'] if grammage > 0.77 else DEFAULT_TRIM_ALLOWANCE['low']
    pieces_per_roll = math.floor(MAX_ROLL_WIDTH / raw_width)
    roll_width = math.ceil((raw_width * pieces_per_roll + trim) / 50) * 50
    effective_width = round(roll_width / pieces_per_roll / 1000, 3)

    cost = paper_length_m * effective_width * grammage * costing
    price = paper_length_m * effective_width * grammage * selling * (1 + adjustment/100)

    return PriceResult(
        cost_price=round(cost, 2),
        selling_price=round(price, 2),
        total_price=round(price * quantity, 2),
        dimensions=f"{length} × {width} × {height} mm",
        formula=f"{paper_length_m}m × {effective_width}m × {grammage}g/m² × RM{selling} × {1+adjustment/100:.2f}",
        production_metrics={
            'Pieces per Roll': pieces_per_roll,
            'Roll Width': f"{roll_width}mm",
            'Paper Length': f"{paper_length_m}m"
        }
    )

# -------------------- UI Components --------------------
def show_price_results(result: PriceResult):
    """Display standardized price results"""
    st.subheader("💰 Pricing Results")
    col1, col2, col3 = st.columns(3)
    col1.metric("Cost per Unit", f"RM {result.cost_price:.2f}")
    col2.metric("Selling Price", f"RM {result.selling_price:.2f}")
    col3.metric("Total Price", f"RM {result.total_price:.2f}")
    
    with st.expander("📊 Detailed Breakdown"):
        st.write(f"**Formula:** {result.formula}")
        st.write(f"**Dimensions:** {result.dimensions}")
        st.table(result.production_metrics)

def carton_box_ui():
    st.header("📦 Carton Box Calculation")
    with st.form("carton_box_form"):
        col1, col2 = st.columns(2)
        length = col1.number_input("Length (mm)", min_value=1.0, value=500.0)
        width = col1.number_input("Width (mm)", min_value=1.0, value=300.0)
        height = col1.number_input("Height (mm)", min_value=1.0, value=200.0)
        
        grammage = col2.number_input("Grammage (g/m²)", min_value=0.1, value=0.84)
        costing = col2.number_input("Costing (RM/ton)", min_value=0.1, value=2.7)
        selling = col2.number_input("Selling (RM/ton)", min_value=0.1, value=3.4)
        quantity = col2.number_input("Quantity", min_value=1, value=100)
        adjustment = col2.number_input("Adjustment %", value=0.0)
        
        if st.form_submit_button("Calculate"):
            result = calculate_box_price(length, width, height, grammage, costing, selling, quantity, adjustment)
            show_price_results(result)

def pizza_box_ui():
    st.header("🍕 Pizza Box Calculation")
    with st.form("pizza_box_form"):
        col1, col2 = st.columns(2)
        length = col1.number_input("Length (mm)", min_value=1.0, value=300.0)
        width = col1.number_input("Width (mm)", min_value=1.0, value=300.0)
        
        grammage = col2.number_input("Grammage (g/m²)", min_value=0.1, value=0.84)
        costing = col2.number_input("Costing (RM/ton)", min_value=0.1, value=2.7)
        selling = col2.number_input("Selling (RM/ton)", min_value=0.1, value=3.4)
        quantity = col2.number_input("Quantity", min_value=1, value=100)
        adjustment = col2.number_input("Adjustment %", value=0.0)
        
        if st.form_submit_button("Calculate"):
            # Pizza boxes use length+20, width+20, height=0
            result = calculate_box_price(
                length + PIZZA_FLAP_EXTENSION, 
                width + PIZZA_FLAP_EXTENSION, 
                0, grammage, costing, selling, quantity, adjustment
            )
            show_price_results(result)

def layer_pad_ui():
    st.header("📦 Layer Pad Calculation")
    with st.form("layer_pad_form"):
        col1, col2 = st.columns(2)
        length = col1.number_input("Length (mm)", min_value=1.0, value=500.0)
        width = col1.number_input("Width (mm)", min_value=1.0, value=300.0)
        
        grammage = col2.number_input("Grammage (g/m²)", min_value=0.1, value=0.84)
        costing = col2.number_input("Costing (RM/ton)", min_value=0.1, value=2.7)
        selling = col2.number_input("Selling (RM/ton)", min_value=0.1, value=3.4)
        quantity = col2.number_input("Quantity", min_value=1, value=100)
        adjustment = col2.number_input("Adjustment %", value=0.0)
        
        if st.form_submit_button("Calculate"):
            # Layer pads have no height
            result = calculate_box_price(length, width, 0, grammage, costing, selling, quantity, adjustment)
            show_price_results(result)

def nesting_design_ui():
    st.header("🧩 Nesting Design Calculator")
    with st.form("nesting_form"):
        st.subheader("Product Dimensions")
        col1, col2 = st.columns(2)
        prod_L = col1.number_input("Length (mm)", min_value=1.0, value=800.0)
        prod_W = col1.number_input("Width (mm)", min_value=1.0, value=204.0)
        prod_H = col1.number_input("Height (mm)", min_value=1.0, value=10.0)
        use_bubble = col1.checkbox("Include Bubble Wrap (10mm)")
        
        thickness = col2.number_input("Nesting Thickness (mm)", min_value=0.1, value=3.0)
        allowance = col2.number_input("Allowance (mm)", min_value=0.0, value=40.0)
        qty_L = col2.number_input("Qty in Length", min_value=1, value=1)
        qty_W = col2.number_input("Qty in Width", min_value=1, value=1)
        
        if st.form_submit_button("Calculate"):
            adj_L = prod_L + 10 if use_bubble else prod_L
            adj_W = prod_W + 10 if use_bubble else prod_W
            
            int_L = allowance + thickness + ((adj_L + thickness) * qty_L) + allowance
            int_W = allowance + thickness + ((adj_W + thickness) * qty_W) + allowance
            
            result = DesignResult(
                internal_size=f"{int_L:.1f} × {int_W:.1f} × {prod_H:.1f} mm",
                external_size=f"{int_L + 10:.1f} × {int_W + 10:.1f} × {prod_H + 20:.1f} mm",
                nesting_sizes={
                    "Long Side": f"{int_L:.1f} × {prod_H:.1f} mm",
                    "Short Side": f"{int_W:.1f} × {prod_H:.1f} mm"
                },
                material_usage={
                    "Product Size": f"{prod_L} × {prod_W} × {prod_H} mm",
                    "Adjusted Size": f"{adj_L} × {adj_W} mm",
                    "Allowance": f"{allowance} mm per side"
                }
            )
            
            st.subheader("Design Results")
            col1, col2 = st.columns(2)
            col1.metric("Internal Size", result.internal_size)
            col2.metric("External Size", result.external_size)
            
            with st.expander("Nesting Details"):
                st.table(result.nesting_sizes)
                st.table(result.material_usage)

# -------------------- Main App --------------------
def main():
    st.set_page_config(
        page_title="Packaging Calculator Pro",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("📦 Packaging Calculator Pro")
    
    # Sidebar navigation
    with st.sidebar:
        st.header("Calculation Types")
        calc_type = st.radio(
            "Select Calculator",
            options=[ct.value for ct in CalculationType]
        )
    
    # Show selected calculator
    if calc_type == CalculationType.CARTON_BOX.value:
        carton_box_ui()
    elif calc_type == CalculationType.PIZZA_BOX.value:
        pizza_box_ui()
    elif calc_type == CalculationType.LAYER_PAD.value:
        layer_pad_ui()
    elif calc_type == CalculationType.NESTING_DESIGN.value:
        nesting_design_ui()
    # Add other calculation types here...

if __name__ == "__main__":
    main()
