
import streamlit as st
import math

def calculate_sample_board(L, W, UPS, G, C, S, Q, A):
    length_m = L / 1000
    width_m = W / 1000
    cost_per_piece = length_m * width_m * G * C
    selling_price = length_m * width_m * G * S * (1 + A / 100)
    total_price = selling_price * Q
    board_area = 1.05 * 0.75  # Fixed board size
    piece_area = length_m * width_m
    ups_per_board = math.floor(board_area / piece_area)
    boards_needed = math.ceil(Q / ups_per_board)
    return cost_per_piece, selling_price, total_price, ups_per_board, boards_needed

st.title("Sample Board Calculator")

L = st.number_input("Product Length (mm)", value=500.0)
W = st.number_input("Product Width (mm)", value=300.0)
UPS = st.number_input("UPS per board (fixed)", value=1)
G = st.number_input("Grammage", value=0.84)
C = st.number_input("Costing Tonnage", value=2.7)
S = st.number_input("Selling Tonnage", value=3.4)
Q = st.number_input("Quantity", value=100)
A = st.number_input("Adjustment %", value=0.0)

if st.button("Calculate Sample Board"):
    cp, sp, tp, ups_calc, boards_needed = calculate_sample_board(L, W, UPS, G, C, S, Q, A)
    st.write(f"Cost per Piece: RM {cp:.4f}")
    st.write(f"Selling Price per Piece: RM {sp:.4f}")
    st.write(f"Total Price: RM {tp:.2f}")
    st.write(f"UPS per Board: {ups_calc}")
    st.write(f"Boards Needed: {boards_needed}")
