import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx

# Title
st.title("Career & Wealth Navigation Tool")

# Sidebar inputs for user details
st.sidebar.header("User Inputs")
career_options = ["Finance Executive", "Manufacturing Entrepreneur", "Consulting", "Board Membership", "Lecturing"]
selected_careers = st.sidebar.multiselect("Select Career Mix", career_options)

# Customizable Weights for Decision Factors
st.sidebar.subheader("Customize Career Weights")
factor_weights = {
    "Earnings Potential": st.sidebar.slider("Earnings Potential", 1, 10, 5),
    "Flexibility": st.sidebar.slider("Flexibility", 1, 10, 5),
    "Scalability": st.sidebar.slider("Scalability", 1, 10, 5),
    "Skill Overlap": st.sidebar.slider("Skill Overlap", 1, 10, 5),
    "Moat Strength": st.sidebar.slider("Moat Strength", 1, 10, 5)
}

# Career Pivot Flowchart
def career_pivot_flowchart(careers):
    G = nx.DiGraph()
    for career in careers:
        if career == "Finance Executive":
            G.add_edge(career, "Board Membership")
            G.add_edge(career, "Consulting")
        elif career == "Manufacturing Entrepreneur":
            G.add_edge(career, "Board Membership")
            G.add_edge(career, "Consulting")
        elif career == "Consulting":
            G.add_edge(career, "Lecturing")
    
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=3000, font_size=10)
    st.pyplot(plt)

if len(selected_careers) > 0:
    st.subheader("Career Pivot Flowchart")
    career_pivot_flowchart(selected_careers)

# Pairwise Comparison Matrix with Adjusted Weights
def pairwise_comparison(earnings, factor_weights):
    careers = list(earnings.keys())
    matrix = pd.DataFrame(index=careers, columns=careers)
    for i in range(len(careers)):
        for j in range(len(careers)):
            if i == j:
                matrix.iloc[i, j] = "-"
            else:
                weight_factor = sum(factor_weights.values()) / len(factor_weights)
                matrix.iloc[i, j] = f"{(earnings[careers[i]] / max(1, earnings[careers[j]])) * weight_factor:.2f}x"
    return matrix

if len(selected_careers) > 1:
    st.subheader("Pairwise Career Comparison")
    earnings = {career: np.random.randint(50000, 200000) for career in selected_careers}
    comparison_matrix = pairwise_comparison(earnings, factor_weights)
    st.dataframe(comparison_matrix)

# Career Next Steps Checklist
def career_next_steps(selected_careers):
    steps = {
        "Finance Executive": ["Expand financial expertise", "Network with industry leaders"],
        "Manufacturing Entrepreneur": ["Optimize production", "Seek investment opportunities"],
        "Consulting": ["Develop thought leadership", "Gain certifications"],
        "Board Membership": ["Engage in nonprofit work", "Build executive presence"],
        "Lecturing": ["Develop course materials", "Engage in academic research"]
    }
    
    for career in selected_careers:
        st.subheader(f"Next Steps for {career}")
        for step in steps.get(career, []):
            st.write(f"- {step}")

if len(selected_careers) > 0:
    st.subheader("Career Next Steps")
    career_next_steps(selected_careers)

