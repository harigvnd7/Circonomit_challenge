# Simulation Model with Feedback Loops and Plotting

import matplotlib.pyplot as plt

# Parameters 

initial_budget = 100000
energy_cost = 10
material_cost = 5
production_efficiency = 0.5
initial_price_per_unit = 120
initial_demand = 1000
time_steps = 10
threshold_revenue = 1000
min_budget_to_operate = 100

# Tracking for future reference to model situation

history = {
    "time": [],
    "budget": [],
    "energy_input": [],
    "material_input": [],
    "production": [],
    "sales": [],
    "revenue": [],
    "price_per_unit": []
}

# Initial State of Model

budget = initial_budget
price_per_unit = initial_price_per_unit
demand = initial_demand

for t in range(time_steps):
    history["time"].append(t)
    history["budget"].append(budget)
    history["price_per_unit"].append(price_per_unit)

    # Feedback: Adjust reinvestment ratio based on revenue 

    if t > 0 and history["revenue"][-1] < threshold_revenue:
        reinvestment_ratio = 0.6
    else:
        reinvestment_ratio = 0.85

    investable_budget = reinvestment_ratio * budget
    energy_budget = 0.4 * investable_budget
    material_budget = 0.6 * investable_budget

    energy_input = energy_budget / energy_cost
    material_input = material_budget / material_cost
    effective_input = min(energy_input, material_input)
    production = production_efficiency * effective_input

    # Feedback: Adjust price based on sales vs demand 
    if t > 0:
        if history["sales"][-1] < 0.5 * demand:
            price_per_unit *= 0.95  # discount to boost demand
        elif history["sales"][-1] > 0.9 * demand:
            price_per_unit *= 1.10  # raise price due to high demand

    sales = min(production, demand)
    revenue = sales * price_per_unit

    #  Update Budget for next time step
    budget = max((1 - reinvestment_ratio) * budget + revenue, min_budget_to_operate)

    #  Saving the information for reference
    history["energy_input"].append(energy_input)
    history["material_input"].append(material_input)
    history["production"].append(production)
    history["sales"].append(sales)
    history["revenue"].append(revenue)

#  Print final summary 
for i in range(time_steps):
    print(f"Time {i}: Budget={history['budget'][i]:.2f}, Production={history['production'][i]:.2f}, "
          f"Sales={history['sales'][i]:.2f}, Revenue={history['revenue'][i]:.2f}, "
          f"Price={history['price_per_unit'][i]:.2f}")

#  Plotting Section 
plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
plt.plot(history["time"], history["budget"], marker='o')
plt.title("Budget over Time")
plt.xlabel("Time")
plt.ylabel("Budget")

plt.subplot(2, 2, 2)
plt.plot(history["time"], history["production"], label='Production', marker='s')
plt.plot(history["time"], history["sales"], label='Sales', marker='x')
plt.title("Production & Sales")
plt.xlabel("Time")
plt.ylabel("Units")
plt.legend()

plt.subplot(2, 2, 3)
plt.plot(history["time"], history["revenue"], marker='^')
plt.title("Revenue over Time")
plt.xlabel("Time")
plt.ylabel("Revenue")

plt.subplot(2, 2, 4)
plt.plot(history["time"], history["price_per_unit"], marker='d')
plt.title("Price per Unit")
plt.xlabel("Time")
plt.ylabel("Price")

plt.tight_layout()
plt.show()

