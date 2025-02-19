import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Title
st.title("Career & Wealth Navigation Tool")

# Step 1: Career Goals
st.header("Step 1: Define Your Career Goals")
career_goals = st.multiselect("Select Your Career Goals", ["High Earnings", "Work-Life Balance", "Career Growth", "Low Risk", "Flexibility", "Scalability"])
st.write("Your selected goals will influence career suggestions and risk analysis.")

# Step 2: Career Selection
st.header("Step 2: Select & Customize Your Career Mix")
career_options = ["Finance Executive", "Manufacturing Entrepreneur", "Consulting", "Board Membership", "Lecturing"]
selected_careers = st.multiselect("Select Careers", career_options)

st.sidebar.header("Career Weights & Risk Factors")

factor_weights = {
    "Earnings Potential": st.sidebar.slider("Earnings Potential", 1, 10, 5),
    "Flexibility": st.sidebar.slider("Flexibility", 1, 10, 5),
    "Scalability": st.sidebar.slider("Scalability", 1, 10, 5),
    "Skill Overlap": st.sidebar.slider("Skill Overlap", 1, 10, 5),
    "Moat Strength": st.sidebar.slider("Moat Strength", 1, 10, 5)
}

earnings = {}
risk_factors = {}
for career in selected_careers:
    earnings[career] = st.number_input(f"Expected Annual Earnings ($) - {career}", min_value=0, step=1000)
    risk_factors[career] = st.slider(f"Risk Level (1-10) - {career}", min_value=1, max_value=10, value=5)

# Step 3: Career Risk & Stability Analysis
def calculate_stability_score(risk_factors):
    return {career: 10 - risk for career, risk in risk_factors.items()}

def diversification_score(earnings):
    total_income = sum(earnings.values()) if sum(earnings.values()) > 0 else 1  # Avoid division by zero
    return {career: (income / total_income) * 100 for career, income in earnings.items()}

if len(earnings) > 1:
    st.header("Step 3: Career Risk & Stability Analysis")
    stability_scores = calculate_stability_score(risk_factors)
    diversification_scores = diversification_score(earnings)
    stability_df = pd.DataFrame({
        "Career": stability_scores.keys(),
        "Stability Score": stability_scores.values(),
        "Diversification Score (%)": diversification_scores.values()
    })
    st.dataframe(stability_df)

# Step 4: Career Pivot & Decision Support
def suggest_career_pivots(earnings, risk_factors, factor_weights):
    suggestions = []
    for career in earnings.keys():
        if risk_factors[career] > 7:
            suggestions.append(f"Consider shifting from {career} to a lower-risk option with similar skill overlap.")
        if factor_weights["Flexibility"] > 7 and career in ["Finance Executive", "Manufacturing Entrepreneur"]:
            suggestions.append(f"{career} has lower flexibility; consider adding Consulting or Lecturing.")
        if factor_weights["Scalability"] > 7 and career not in ["Entrepreneur", "Consulting"]:
            suggestions.append(f"{career} has limited scalability; consider adding an entrepreneurial path.")
    return suggestions

if len(earnings) > 1:
    st.header("Step 4: Suggested Career Pivots")
    pivots = suggest_career_pivots(earnings, risk_factors, factor_weights)
    for pivot in pivots:
        st.write("- ", pivot)

# Improved Radar Chart for Career Factors
def radar_chart(factor_weights):
    labels = list(factor_weights.keys())
    values = list(factor_weights.values())
    values += values[:1]  # Close the circle
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='blue', alpha=0.3)
    ax.plot(angles, values, color='blue', linewidth=2)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_yticklabels([])
    st.pyplot(fig)

st.header("Career Factor Radar Chart")
radar_chart(factor_weights)

st.write("This visualization helps you understand the weight distribution of key decision factors in your career choices.")
