import matplotlib.pyplot as plt
import numpy as np

# Data for the horizontal bar chart
challenge_areas = ['Time Management', 'Research Productivity',
                  'Teaching Quality', 'Work-Life Balance', 'Institutional Politics']
highly_effective = [65, 55, 70, 50, 30]
moderately_effective = [25, 30, 20, 35, 45]
not_effective = [10, 15, 10, 15, 25]

# Define the color scheme to match previous charts
colors = ['#2b6cb0', '#c53030', '#2f855a']  # Blue, red, green

# Create the figure and axes
fig, ax = plt.subplots(figsize=(8, 5))

# Create horizontal bar chart with stacking
ax.barh(challenge_areas, highly_effective,
       color=colors[0], edgecolor='white', label='Highly Effective')
ax.barh(challenge_areas, moderately_effective, left=highly_effective,
       color=colors[1], edgecolor='white', label='Moderately Effective')
ax.barh(challenge_areas, not_effective, left=np.add(highly_effective,
       moderately_effective), color=colors[2], edgecolor='white', label='Not Effective')

# Add labels, title, and custom formatting
ax.set_xlabel('Percentage (%)')
ax.set_title(
    'Perceived Effectiveness of Reflective Practice on Academic Challenges')
ax.invert_yaxis()  # Reverse the y-axis to have the top category first

# Add the legend
plt.legend(loc='upper right', frameon=True)

# Display the chart
plt.tight_layout()

# Save the figure as requested
plt.savefig("Effectiveness_Reflective_Practice_Academic_Challenges.png")

plt.show()
