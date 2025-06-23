import streamlit as st
import math
from dataclasses import dataclass
from enum import Enum

# ==================== CONSTANTS & ENUMS ====================
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

# ==================== DATA STRUCTURES ====================
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

# ==================== CORE CALCULATIONS ====================
def calculate_pizza_box(
    length: float, 
    width: float, 
    grammage: float, 
    costing_tonnage: float,
    selling_tonnage: float,
    quantity: int,
    adjustment_percent: float
) -> PriceResult:
    """Precise pizza box calculation according to specifications"""
    # Paper dimensions
    paper_length = length + PIZZA_FLAP_EXTENSION  # mm
    paper_width = width + PIZZA_FLAP_EXTENSION    # mm
    
    # Roll optimization
    ups = math.floor(MAX_ROLL_WIDTH / paper_width)
    if ups == 0:
        raise ValueError("Box width too large for standard rolls (max 2200mm)")
    
    total_used_width = paper_width * ups
    roll_width = math.ceil((total_used_width + 28) / 50) * 50  # 28mm trimming allowance
    paper_actual_width = roll_width / ups  # mm
    
    # Convert to meters
    paper_length_m = paper_length / 1000
    paper_actual_width_m = paper_actual_width / 1000
    
    # Pricing
    cost_price = paper_length_m * paper_actual_width_m * grammage * costing_tonnage
    selling_price = paper_length_m * paper_actual_width_m * grammage * selling_tonnage * (1 + adjustment_percent/100)
    
    return PriceResult(
        cost_price=round(cost_price, 4),
        selling_price=round(selling_price, 4),
        total_price=round(selling_price * quantity, 2),
        dimensions=f"{length} × {width} mm (box) → {paper_length} × {paper_width} mm (paper)",
        formula=(
            f"({paper_length_m:.3f}m × {paper_actual_width_m:.3f}m) × {grammage}g/m² × "
            f"RM{selling_tonnage} × {1 + adjustment_percent/100:.2f}"
        ),
        production_metrics={
            "Pieces per Roll": ups,
            "Roll Width": f"{roll_width}mm",
            "Actual Width per Piece": f"{paper_actual_width:.2f}mm",
            "Paper Length": f"{paper_length_m:.3f}m"
        }
    )

def calculate_standard_box(length, width, height, grammage, costing, selling, quantity, adjustment):
    """Universal calculation for carton boxes and layer pads"""
    total_paper = (length + width) * 2 + 30  # mm
    raw_width = width + height + 4  # mm
    
    # Roll optimization
    trim = DEFAULT_TRIM_ALLOWANCE['high'] if grammage > 0.77 else DEFAULT_TRIM_ALLOWANCE['low']
    ups = math.floor(MAX_ROLL_WIDTH / raw_width)
    roll_width = math.ceil((raw_width * ups + trim) / 50) * 50
    effective_width = roll_width / ups  # mm
    
    # Convert to meters
    paper_length_m = total_paper / 1000
    effective_width_m = effective_width / 1000
    
    # Pricing
    cost = paper_length_m * effective_width_m * grammage * costing
    price = paper_length_m * effective_width_m * grammage * selling * (1 + adjustment/100)
    
    return PriceResult(
        cost_price=round(cost, 2),
        selling_price=round(price, 2),
        total_price=round(price * quantity, 2),
        dimensions=f"{length} × {width} × {height} mm",
        formula=f"{paper_length_m:.3f}m × {effective_width_m:.3f}m × {grammage}g/m² × RM{selling} × {1+adjustment/100:.2f}",
        production_metrics={
            'Pieces per Roll': ups,
            'Roll Width': f"{roll_width}mm",
            'Effective Width': f"{effective_width:.1f}mm"
        }
    )

# ==================== UI COMPONENTS ====================
def show_price_results(result: PriceResult):
    """Standardized results display for pricing calculations"""
    st.subheader("📊 Calculation Results")
    
    cols = st.columns(3)
    cols[0].metric("Cost Price", f"RM {result.cost_price:.4f}")
    cols[1].metric("Selling Price", f"RM {result.selling_price:.4f}")
    cols[2].metric("Total Price", f"RM {result.total_price:.2f}")
    
    with st.expander("🔍 Detailed Breakdown"):
        st.write(f"**Dimensions:** {result.dimensions}")
        st.write(f"**Formula:** {result.formula}")
        st.table(result.production_metrics)

def carton_box_ui():
    st.header("📦 Carton Box Calculator")
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
            result = calculate_standard_box(length, width, height, grammage, costing, selling, quantity, adjustment)
            show_price_results(result)

def pizza_box_ui():
    st.header("🍕 Pizza Box Calculator (Precise Formula)")
    with st.form("pizza_box_form"):
        col1, col2 = st.columns(2)
        length = col1.number_input("Box Length (mm)", min_value=1.0, value=300.0)
        width = col1.number_input("Box Width (mm)", min_value=1.0, value=300.0)
        grammage = col2.number_input("Grammage (g/m²)", min_value=0.1, value=0.84)
        
        costing = col2.number_input("Costing (RM/ton)", min_value=0.1, value=2.7)
        selling = col2.number_input("Selling (RM/ton)", min_value=0.1, value=3.4)
        quantity = col2.number_input("Quantity", min_value=1, value=100)
        adjustment = col2.number_input("Adjustment %", value=0.0)
        
        if st.form_submit_button("Calculate"):
            try:
                result = calculate_pizza_box(length, width, grammage, costing, selling, quantity, adjustment)
                show_price_results(result)
            except ValueError as e:
                st.error(str(e))

def layer_pad_ui():
    st.header("📦 Layer Pad Calculator")
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
            result = calculate_standard_box(length, width, 0, grammage, costing, selling, quantity, adjustment)
            show_price_results(result)

# ==================== MAIN APP ====================
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
    elif calc_type == CalculationType.SAMPLE_BOARD.value:
        sample_board_ui()
    elif calc_type == CalculationType.NESTING_LAYER_PAD.value:
        nesting_layer_pad_ui()

if __name__ == "__main__":
    main()
