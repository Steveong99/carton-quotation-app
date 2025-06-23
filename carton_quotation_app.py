import streamlit as st
import math
from dataclasses import dataclass
from enum import Enum
from typing import Tuple

# ==================== CONSTANTS & ENUMS ====================
class CalculationType(Enum):
    CARTON_BOX = "Carton Box"
    PIZZA_BOX = "Pizza Box"
    LAYER_PAD = "Layer Pad"
    NESTING_DESIGN = "Nesting Design"
    SAMPLE_BOARD = "Sample Board"
    NESTING_LAYER_PAD = "Nesting & Layer Pad"

DEFAULT_TRIM_ALLOWANCE = {'low': 25, 'high': 28}  # For grammage <=0.77 and >0.77
MAX_ROLL_WIDTH = 2200  # mm
PIZZA_FLAP_EXTENSION = 20  # mm
STANDARD_SLOT_SIZE = 3  # mm for nesting designs

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
    internal_dimensions: Tuple[float, float, float]
    external_dimensions: Tuple[float, float, float]
    nesting_long: Tuple[float, float]
    nesting_short: Tuple[float, float]
    layer_pad_thickness: float

@dataclass
class SampleBoardResult:
    ups: int
    boards_needed: int
    cost_per_piece: float
    final_price: float

# ==================== CORE CALCULATIONS ====================
def calculate_pizza_box(length: float, width: float, grammage: float, 
                       costing: float, selling: float, quantity: int, 
                       adjustment: float) -> PriceResult:
    """Precise pizza box calculation with 20mm flap extension"""
    paper_length = length + PIZZA_FLAP_EXTENSION  # mm
    paper_width = width + PIZZA_FLAP_EXTENSION    # mm
    
    # Roll optimization
    ups = math.floor(MAX_ROLL_WIDTH / paper_width)
    if ups == 0:
        raise ValueError("Box width exceeds maximum roll width (2200mm)")
    
    total_used = paper_width * ups
    roll_width = math.ceil((total_used + 28) / 50) * 50  # 28mm trimming allowance
    actual_width = roll_width / ups  # mm
    
    # Convert to meters for pricing
    paper_length_m = paper_length / 1000
    actual_width_m = actual_width / 1000
    
    # Pricing calculation
    cost = paper_length_m * actual_width_m * grammage * costing
    price = paper_length_m * actual_width_m * grammage * selling * (1 + adjustment/100)
    
    return PriceResult(
        cost_price=round(cost, 4),
        selling_price=round(price, 4),
        total_price=round(price * quantity, 2),
        dimensions=f"{length}x{width}mm → {paper_length}x{paper_width}mm (paper)",
        formula=f"({paper_length_m:.3f}m × {actual_width_m:.3f}m) × {grammage}g/m² × RM{selling} × {1+adjustment/100:.2f}",
        production_metrics={
            "Pieces/Roll": ups,
            "Roll Width": f"{roll_width}mm",
            "Actual Width": f"{actual_width:.2f}mm"
        }
    )

def calculate_nesting_design(product_L: float, product_W: float, product_H: float,
                           include_bubble: bool, thickness: float, allowance: float,
                           qty_L: int, qty_W: int, layer_thick: float) -> DesignResult:
    """Calculate nested packaging design with layer pads"""
    # Adjust for bubble wrap
    adj_L = product_L + 10 if include_bubble else product_L
    adj_W = product_W + 10 if include_bubble else product_W
    
    # Internal dimensions
    int_L = allowance + thickness + ((adj_L + thickness) * qty_L) + allowance
    int_W = allowance + thickness + ((adj_W + thickness) * qty_W) + allowance
    int_H = product_H  # Height doesn't nest
    
    # External dimensions
    ext_L = int_L + 10  # 10mm wall thickness
    ext_W = int_W + 10
    ext_H = int_H + 20 + layer_thick  # 20mm top/bottom + layer pad
    
    # Nesting pieces
    nesting_long = (int_L, product_H)  # Length-wise nesting
    nesting_short = (int_W, product_H)  # Width-wise nesting
    
    return DesignResult(
        internal_dimensions=(int_L, int_W, int_H),
        external_dimensions=(ext_L, ext_W, ext_H),
        nesting_long=nesting_long,
        nesting_short=nesting_short,
        layer_pad_thickness=layer_thick
    )

# ==================== UI COMPONENTS ====================
def show_price_results(result: PriceResult):
    """Standardized price results display"""
    st.subheader("💰 Pricing Results")
    cols = st.columns(3)
    cols[0].metric("Cost/Unit", f"RM {result.cost_price:.4f}")
    cols[1].metric("Price/Unit", f"RM {result.selling_price:.4f}")
    cols[2].metric("Total Price", f"RM {result.total_price:.2f}")
    
    with st.expander("📊 Production Details"):
        st.write(f"**Formula:** {result.formula}")
        st.write(f"**Dimensions:** {result.dimensions}")
        st.table(result.production_metrics)

def show_design_results(result: DesignResult):
    """Display nesting design results"""
    st.subheader("📐 Design Specifications")
    
    col1, col2 = st.columns(2)
    col1.metric("Internal Size", f"{result.internal_dimensions[0]:.1f} × {result.internal_dimensions[1]:.1f} × {result.internal_dimensions[2]:.1f} mm")
    col2.metric("External Size", f"{result.external_dimensions[0]:.1f} × {result.external_dimensions[1]:.1f} × {result.external_dimensions[2]:.1f} mm")
    
    with st.expander("🧩 Nesting Components"):
        st.write(f"**Long Nesting:** {result.nesting_long[0]:.1f} × {result.nesting_long[1]:.1f} mm")
        st.write(f"**Short Nesting:** {result.nesting_short[0]:.1f} × {result.nesting_short[1]:.1f} mm")
        st.write(f"**Layer Pad Thickness:** {result.layer_pad_thickness}mm")

# ==================== CALCULATOR PAGES ====================
def carton_box_ui():
    st.header("📦 Carton Box Calculator")
    with st.form("carton_box_form"):
        col1, col2 = st.columns(2)
        length = col1.number_input("Length (mm)", min_value=1.0, value=500.0)
        width = col1.number_input("Width (mm)", min_value=1.0, value=300.0)
        height = col1.number_input("Height (mm)", min_value=1.0, value=200.0)
        
        grammage = col2.number_input("Grammage (g/m²)", min_value=0.1, value=0.84)
        costing = col2.number_input("Cost (RM/ton)", min_value=0.1, value=2.7)
        selling = col2.number_input("Sell (RM/ton)", min_value=0.1, value=3.4)
        quantity = col2.number_input("Quantity", min_value=1, value=100)
        adjustment = col2.number_input("Adjustment %", value=0.0)
        
        if st.form_submit_button("Calculate"):
            result = calculate_standard_box(length, width, height, grammage, costing, selling, quantity, adjustment)
            show_price_results(result)

def nesting_design_ui():
    st.header("🧩 Nesting Design Calculator")
    with st.form("nesting_form"):
        st.subheader("Product Dimensions")
        col1, col2 = st.columns(2)
        product_L = col1.number_input("Length (mm)", min_value=1.0, value=800.0)
        product_W = col1.number_input("Width (mm)", min_value=1.0, value=204.0)
        product_H = col1.number_input("Height (mm)", min_value=1.0, value=10.0)
        include_bubble = col1.checkbox("Include Bubble Wrap (+10mm)")
        
        st.subheader("Design Parameters")
        thickness = col2.number_input("Nesting Thickness (mm)", min_value=0.1, value=3.0)
        allowance = col2.number_input("Allowance (mm)", min_value=0.0, value=40.0)
        qty_L = col2.number_input("Qty in Length", min_value=1, value=1)
        qty_W = col2.number_input("Qty in Width", min_value=1, value=1)
        layer_thick = col2.number_input("Layer Pad Thickness (mm)", min_value=0.0, value=3.0)
        
        if st.form_submit_button("Calculate"):
            result = calculate_nesting_design(
                product_L, product_W, product_H,
                include_bubble, thickness, allowance,
                qty_L, qty_W, layer_thick
            )
            show_design_results(result)

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
    
    # Router
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
