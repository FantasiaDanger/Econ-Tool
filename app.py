import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Function to plot the simulation
def plot_supply_demand(
    demand_intercept, demand_slope, supply_intercept, supply_slope,
    tax, subsidy, externality, substitute_price, market_flexibility
):
    # Define the price range
    price = np.linspace(1, 100, 500)

    # Adjust slopes based on market flexibility
    adjusted_demand_slope = demand_slope / market_flexibility
    adjusted_supply_slope = supply_slope / market_flexibility

    # Demand curve: Qd = demand_intercept - adjusted_demand_slope * P + sensitivity * (substitute_price - base_substitute_price)
    base_substitute_price = 50  # Reference price for substitutes
    sensitivity = 1.5  # Sensitivity of demand to substitute price changes
    demand = demand_intercept - adjusted_demand_slope * price + sensitivity * (substitute_price - base_substitute_price)
    demand[demand < 0] = 0  # No negative demand

    # Supply curve: Qs = supply_intercept + adjusted_supply_slope * P + externality - tax + subsidy
    supply = supply_intercept + adjusted_supply_slope * price + externality / 10 - tax + subsidy
    supply[supply < 0] = 0  # No negative supply

    # Find equilibrium: Where Qd = Qs
    equilibrium_price_index = np.abs(demand - supply).argmin()
    equilibrium_price = price[equilibrium_price_index]
    equilibrium_quantity = supply[equilibrium_price_index]

    # Plot the supply and demand curves
    plt.figure(figsize=(10, 6))
    plt.plot(price, demand, label="Demand Curve (Qd)", color="blue")
    plt.plot(price, supply, label="Supply Curve (Qs)", color="green")
    plt.scatter(equilibrium_price, equilibrium_quantity, color="red", label="Equilibrium")
    plt.axvline(equilibrium_price, color="gray", linestyle="--", label=f'Price: {equilibrium_price:.2f}')
    plt.axhline(equilibrium_quantity, color="gray", linestyle="--", label=f'Quantity: {equilibrium_quantity:.2f}')
    plt.title("Microeconomic Simulation: Market Flexibility")
    plt.xlabel("Price")
    plt.ylabel("Quantity")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

# Streamlit App Layout
st.title("Interactive Microeconomic Simulation: Market Flexibility")

st.sidebar.header("Adjust Supply and Demand Curves")

# Demand Curve Parameters
st.sidebar.subheader("Demand Curve")
demand_intercept = st.sidebar.slider("Demand Intercept (Base Quantity)", 50, 150, 100)
demand_slope = st.sidebar.slider("Demand Slope (Elasticity)", 1, 5, 2)

# Supply Curve Parameters
st.sidebar.subheader("Supply Curve")
supply_intercept = st.sidebar.slider("Supply Intercept (Base Quantity)", 0, 50, 20)
supply_slope = st.sidebar.slider("Supply Slope (Elasticity)", 1, 5, 2)

# Additional Modifiers
st.sidebar.header("Market Modifiers")
tax = st.sidebar.slider("Tax", 0, 20, 0)
subsidy = st.sidebar.slider("Subsidy", 0, 20, 0)
externality = st.sidebar.slider("Externality", -20, 20, 0)

# Substitute Effects
st.sidebar.header("Substitute Product")
substitute_price = st.sidebar.slider("Substitute Price", 10, 100, 50)

# Market Flexibility
st.sidebar.header("Market Flexibility")
market_flexibility = st.sidebar.slider(
    "Market Flexibility (Higher = More Flexible)", 0.5, 2.0, 1.0, step=0.1
)

st.sidebar.write(
    """
    **Instructions**:
    - Use the sliders to adjust supply and demand parameters, substitute product price, market modifiers, and market flexibility.
    - Observe how the curves and equilibrium point change dynamically.
    """
)

# Plot the simulation with the selected parameters
plot_supply_demand(
    demand_intercept,
    demand_slope,
    supply_intercept,
    supply_slope,
    tax,
    subsidy,
    externality,
    substitute_price,
    market_flexibility,
)
