import numpy as np 
np.random.seed(20)
num_months = 12
free_production_per_month = 15
min_possible_demand = 1
max_possible_demand = 30
demand_per_month = np.random.randint(min_possible_demand, max_possible_demand, num_months)



def c(x):
    # 3 cost per machine produced over m 
    return x*5

def h(x):
    #6 cost per machine held in inventory at end of month
    return x*6

def fill_dp_matrix(num_months, free_production_quantity, demand_per_month_array):
    big_d = sum(demand_per_month_array)
    dp = np.full((num_months + 1, big_d + 1), np.inf)  # Initialize all to inf
    production_table = np.zeros((num_months + 1, big_d + 1))
    dp[num_months, 0] = 0  # Base case: no cost for ending with 0 inventory

    # Handle zero demand case
    if big_d == 0:
        return (production_table, 0)  # No cost if there's no demand to meet

    m = free_production_quantity
    for inventory in range(big_d + 1):
        for month in range(num_months - 1, -1, -1):
            if demand_per_month_array[month] == (inventory + m):
                dp[month, inventory] = dp[month + 1, 0]
                production_table[month, inventory] = (demand_per_month_array[month] - inventory)
            elif demand_per_month_array[month] > (m + inventory):
                dp[month, inventory] = dp[month + 1, 0] + c(demand_per_month_array[month] - (inventory + m))
                production_table[month, inventory] = (demand_per_month_array[month] - inventory)
            else:
                min_cost = float('inf')
                for potential_production in range(min(m + 1, big_d + 1)):  # Avoid out-of-bounds access
                    if dp[month + 1, potential_production] < min_cost:
                        min_cost = dp[month + 1, potential_production] + h(potential_production)
                production_table[month, inventory] = abs(inventory - demand_per_month_array[month])
                dp[month, inventory] = min_cost
    best_cost = dp[0, 0]
    return (production_table, best_cost)





def print_results(results):
    production_table, best_cost = results
    best_cost = int(best_cost)
    num_months = production_table.shape[0]
    for i in range(num_months - 1):  # Exclude the last row if it's just a base case
        production_quantity = np.argmin(production_table[i, :])  # Production quantity based on the minimum cost
        print(f"In month {i + 1}, produce {production_quantity} machines.")
    print(f"For a total cost of: {best_cost}")


print_results(fill_dp_matrix(num_months,free_production_per_month,demand_per_month))