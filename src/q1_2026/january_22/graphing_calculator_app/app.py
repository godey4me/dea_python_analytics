import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

# Helper Function
def graph(eq_str: str):
    # Default starting to end point
    start = -10
    end = 10

    # Linspace
    x = np.linspace(start=start, stop=end, num=100)

    y = eval(eq_str)

    # Matplotlib
    fig = plt.figure(figsize=(10, 10))
    plt.plot(x, y, 'r-')

    st.pyplot(fig)

# Equation as a text box
equation = st.text_area(label="Pass in a mathematical function with respect to x.", placeholder='x**2')

# button
if st.button("Graph"):
    
    try:
        st.info("Processing function")

        graph(eq_str=equation)

        st.success("Graph has been processed")
    
    except Exception as e:
        st.error(f"Error occurred: {e}")