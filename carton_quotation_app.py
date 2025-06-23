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
SAMPLE_BOARD_TRIM = 28  # mm

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

@dataclass
class SampleBoardResult:
    cost_per_piece: float
    final_unit_price: float
    ups: int
    boards_needed: int
    total_boards: int

# ==================== CORE CALCULATIONS ====================
def calculate_pizza_box(length, width, grammage, costing, selling, quantity, adjustment):
    """Precise pizza box calculation with 20mm flap extension"""
    paper_length = length + PIZZA_FLAP_EXTENSION
    paper_width = width + PIZZA_FLAP_EXTENSION
    
    ups = math.floor(MAX_ROLL_WIDTH / paper_width)
    total_used = paper_width * ups
    roll_width = math.ceil((total_used + 28) / 50) * 50
    actual_width = roll_width / ups
    
    paper_length_m = paper_length / 1000
    actual_width_m = actual_width / 1000
    
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

def calculate_standard_box(length, width, height, grammage, costing, selling, quantity, adjustment):
    """Universal calculation for cartons and layer pads"""
    total_paper = (length + width) * 2 + 30
    raw_width = width + height + 4
    
    trim = DEFAULT_TRIM_ALLOWANCE['high'] if grammage > 0.77 else DEFAULT_TRIM_ALLOWANCE['low']
    ups = math.floor(MAX_ROLL_WIDTH / raw_width)
    roll_width = math.ceil((raw_width * ups + trim) / 50) * 50
    effective_width = roll_width / ups
    
    paper_length_m = total_paper / 1000
    effective_width_m = effective_width / 1000
    
    cost = paper_length_m * effective_width_m * grammage * costing
    price = paper_length_m * effective_width_m * grammage * selling * (1 + adjustment/100)
    
    return PriceResult(
        cost_price=round(cost, 2),
        selling_price=round(price, 2),
        total_price=round(price * quantity, 2),
        dimensions=f"{length}x{width}x{height}mm",
        formula=f"{paper_length_m:.3f}m × {effective_width_m:.3f}m × {grammage}g/m² × RM{selling} × {1+adjustment/100:.2f}",
        production_metrics={
            'Pieces/Roll': ups,
            'Roll Width': f"{roll_width}mm",
            'Effective Width': f"{effective_width:.1f}mm"
        }
    )

def calculate_sample_board(board_L, board_W, product_L, product_W, price_per_board, order_qty, test_qty, job_cost, margin):
    """Sample board optimization calculation"""
    ups_L = int(board_L // product_L)
    ups_W = int(board_W // product_W)
    total_ups = ups_L * ups_W
    
    if total_ups == 0:
        raise ValueError("Product too large for board")
    
    boards_needed = -(-order_qty // total_ups)  # Ceiling division
    total_boards = boards_needed + test_qty
    
    cost_per_piece = (total_boards * price_per_board + job_cost) / order_qty
    final_price = cost_per_piece * (1 + margin/100)
    
    return SampleBoardResult(
        cost_per_piece=round(cost_per_piece, 3),
        final_unit_price=round(final_price, 3),
        ups=total_ups,
        boards_needed=boards_needed,
        total_boards=total_boards
    )

# ==================== UI COMPONENTS ====================
def show_price_results(result: PriceResult):
    """Standard pricing results display"""
    st.subheader("📊 Results")
    col1, col2, col3 = st.columns(3)
    col1.metric("Cost/Unit", f"RM {result.cost_price:.4f}")
    col2.metric("Price/Unit", f"RM {result.selling_price:.4f}")
    col3.metric("Total", f"RM {result.total_price:.2f}")
    
    with st.expander("🔍 Details"):
        st.write(f"**Dimensions:** {result.dimensions}")
        st.write(f"**Formula:** {result.formula}")
        st.table(result.production_metrics)

def carton_box_ui():
    st.header("📦 Carton Box")
    with st.form("carton_box_form"):
        col1, col2 = st.columns(2)
        length = col1.number_input("Length (mm)", value=500.0)
        width = col1.number_input("Width (mm)", value=300.0)
        height = col1.number_input("Height (mm)", value=200.0)
        
        grammage = col2.number_input("Grammage (g/m²)", value=0.84)
        costing = col2.number_input("Cost (RM/ton)", value=2.7)
        selling = col2.number_input("Sell (RM/ton)", value=3.4)
        quantity = col2.number_input("Quantity", value=100)
        adjustment = col2.number_input("Adjustment %", value=0.0)
        
        if st.form_submit_button("Calculate"):
            result = calculate_standard_box(length, width, height, grammage, costing, selling, quantity, adjustment)
            show_price_results(result)

def pizza_box_ui():
    st.header("🍕 Pizza Box")
    with st.form("pizza_box_form"):
        col1, col2 = st.columns(2)
        length = col1.number_input("Length (mm)", value=300.0)
        width = col1.number_input("Width (mm)", value=300.0)
        grammage = col2.number_input("Grammage (g/m²)", value=0.84)
        
        costing = col2.number_input("Cost (RM/ton)", value=2.7)
        selling = col2.number_input("Sell (RM/ton)", value=3.4)
        quantity = col2.number_input("Quantity", value=100)
        adjustment = col2.number_input("Adjustment %", value=0.0)
        
        if st.form_submit_button("Calculate"):
            try:
                result = calculate_pizza_box(length, width, grammage, costing, selling, quantity, adjustment)
                show_price_results(result)
            except ValueError as e:
                st.error(str(e))

def sample_board_ui():
    st.header("📋 Sample Board")
    with st.form("sample_board_form"):
        st.subheader("Board Specs")
        col1, col2 = st.columns(2)
        board_L = col1.number_input("Board Length (mm)", value=2400.0)
        board_W = col1.number_input("Board Width (mm)", value=1322.0)
        price_per_board = col2.number_input("Price/Board (RM)", value=5.95)
        test_qty = col2.number_input("Test Qty", value=2)
        
        st.subheader("Product Specs")
        col1, col2 = st.columns(2)
        product_L = col1.number_input("Product Length (mm)", value=375.0)
        product_W = col1.number_input("Product Width (mm)", value=310.0)
        order_qty = col2.number_input("Order Qty", value=144)
        job_cost = col2.number_input("Job Cost (RM)", value=60.0)
        margin = st.number_input("Margin %", value=0.0)
        
        if st.form_submit_button("Calculate"):
            try:
                result = calculate_sample_board(
                    board_L, board_W, product_L, product_W,
                    price_per_board, order_qty, test_qty,
                    job_cost, margin
                )
                
                st.subheader("📊 Results")
                col1, col2 = st.columns(2)
                col1.metric("Cost/Piece", f"RM {result.cost_per_piece:.3f}")
                col2.metric("Sell Price", f"RM {result.final_unit_price:.3f}")
                
                with st.expander("🔍 Details"):
                    st.write(f"**UPS:** {result.ups} pieces/board")
                    st.write(f"**Boards Needed:** {result.boards_needed} + {test_qty} test = {result.total_boards}")
                    st.write(f"**Margin:** {margin}%")
                    
            except ValueError as e:
                st.error(str(e))

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
    elif calc_type == CalculationType.SAMPLE_BOARD.value:
        sample_board_ui()
    # Additional calculators can be added here...

if __name__ == "__main__":
    main()
