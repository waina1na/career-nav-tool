import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

earnings = {}
risk_factors = {}
for career in selected_careers:
    earnings[career] = st.sidebar.number_input(f"Expected Annual Earnings ($) - {career}", min_value=0, step=1000)
    risk_factors[career] = st.sidebar.slider(f"Risk Level (1-10) - {career}", min_value=1, max_value=10, value=5)

# Monte Carlo Simulation - Earnings Projection
def monte_carlo_simulation(earnings, risk_factors, simulations=1000, years=10):
    results = {}
    for career, base_earning in earnings.items():
        growth_rate = np.random.normal(0.05, 0.02, simulations)  # 5% avg growth with 2% std dev
        risk_adjustment = 1 - (risk_factors[career] / 10)  # Adjust growth based on risk level
        projections = base_earning * np.cumprod(1 + (growth_rate * risk_adjustment))
        results[career] = projections
    return results

if st.sidebar.button("Run Projection"):
    projections = monte_carlo_simulation(earnings, risk_factors)
    st.subheader("Projected Earnings Over 10 Years")
    
    for career, values in projections.items():
        st.write(f"{career}: Median Earnings after 10 years: ${np.median(values):,.2f}")
        fig, ax = plt.subplots()
        ax.hist(values, bins=30, alpha=0.7)
        ax.set_title(f"Monte Carlo Simulation - {career}")
        ax.set_xlabel("Earnings ($)")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

# Feature Engineering - Career Stability & Diversification Score
def calculate_stability_score(risk_factors):
    return {career: 10 - risk for career, risk in risk_factors.items()}

def diversification_score(earnings):
    total_income = sum(earnings.values()) if sum(earnings.values()) > 0 else 1  # Avoid division by zero
    return {career: (income / total_income) * 100 for career, income in earnings.items()}

if len(earnings) > 1:
    stability_scores = calculate_stability_score(risk_factors)
    diversification_scores = diversification_score(earnings)
    
    st.subheader("Career Stability & Diversification Scores")
    stability_df = pd.DataFrame({
        "Career": stability_scores.keys(),
        "Stability Score": stability_scores.values(),
        "Diversification Score (%)": diversification_scores.values()
    })
    st.dataframe(stability_df)

# Pairwise Comparison Matrix with Adjusted Weights
def pairwise_comparison(earnings, factor_weights):
    careers = list(earnings.keys())
    matrix = pd.DataFrame(index=careers, columns=careers)
    for i in range(len(careers)):
        for j in range(len(careers)):
            if i == j:
                matrix.iloc[i, j] = "-"
            else:
                weight_factor = sum(factor_weights.values()) / len(factor_weights)  # Normalize weights
                matrix.iloc[i, j] = f"{(earnings[careers[i]] / max(1, earnings[careers[j]])) * weight_factor:.2f}x"
    return matrix

if len(earnings) > 1:
    st.subheader("Pairwise Career Comparison with Weights")
    comparison_matrix = pairwise_comparison(earnings, factor_weights)
    st.dataframe(comparison_matrix)

# Suggested Career Pivots Algorithm
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
    st.subheader("Suggested Career Pivots")
    pivots = suggest_career_pivots(earnings, risk_factors, factor_weights)
    for pivot in pivots:
        st.write("- ", pivot)

# Visualization: Radar Chart for Career Factors
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

st.subheader("Career Factor Radar Chart")
radar_chart(factor_weights)

st.write("This visualization helps you understand the weight distribution of key decision factors in your career choices.")

