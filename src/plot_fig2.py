import matplotlib.pyplot as plt
import numpy as np

# Data for the chart
categories = ['Daily', 'Weekly', 'Monthly', 'Rarely or Never']
high_anxiety = [15, 25, 40, 60]
moderate_anxiety = [45, 50, 45, 30]
low_anxiety = [40, 25, 15, 10]

# Bar width and x positions
barWidth = 0.85
r = np.arange(len(categories))

# Creating the stacked bar chart with adjusted style to match previous examples
plt.figure(figsize=(10, 6))
plt.bar(r, high_anxiety, color='#2b6cb0', edgecolor='white',
       width=barWidth, label='High Anxiety')
plt.bar(r, moderate_anxiety, bottom=high_anxiety, color='#c53030',
       edgecolor='white', width=barWidth, label='Moderate Anxiety')
plt.bar(r, low_anxiety, bottom=np.array(high_anxiety) + np.array(moderate_anxiety),
       color='#2f855a', edgecolor='white', width=barWidth, label='Low Anxiety')

# Adding labels and title with standard black font
plt.xlabel('Frequency of Reflection', fontsize=12, color='black')
plt.ylabel('Percentage (%)', fontsize=12, color='black')
plt.title('Relationship between Frequency of Reflection and Levels of Academic Anxiety',
         fontsize=14, color='black')
plt.xticks(r, categories, fontsize=10, color='black')

# Adding a legend outside the chart
plt.legend(loc='upper left', bbox_to_anchor=(1, 1), frameon=False)

# Display the chart
plt.tight_layout()
plt.show()
