import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title("Career & Wealth Navigation Tool")

# Sidebar inputs for user details
st.sidebar.header("User Inputs")
career_options = ["Finance Executive", "Manufacturing Entrepreneur", "Consulting", "Board Membership", "Lecturing"]
selected_careers = st.sidebar.multiselect("Select Career Mix", career_options)

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
    total_income = sum(earnings.values())
    return {career: (income / total_income) * 100 for career, income in earnings.items()}


if len(earnings) > 1:
    stability_scores = calculate_stability_score(risk_factors)
    diversification_scores = diversification_score(earnings)

    st.subheader("Career Stability & Diversification Scores")
    stability_df = pd.DataFrame({"Career": stability_scores.keys(), "Stability Score": stability_scores.values(),
                                 "Diversification Score (%)": diversification_scores.values()})
    st.dataframe(stability_df)


# Pairwise Comparison Matrix
def pairwise_comparison(earnings):
    careers = list(earnings.keys())
    matrix = pd.DataFrame(index=careers, columns=careers)
    for i in range(len(careers)):
        for j in range(len(careers)):
            if i == j:
                matrix.iloc[i, j] = "-"
            else:
                matrix.iloc[i, j] = f"{earnings[careers[i]] / max(1, earnings[careers[j]]):.2f}x"
    return matrix


if len(earnings) > 1:
    st.subheader("Pairwise Career Comparison")
    st.write("This compares the relative earning potential of selected careers.")
    comparison_matrix = pairwise_comparison(earnings)
    st.dataframe(comparison_matrix)
