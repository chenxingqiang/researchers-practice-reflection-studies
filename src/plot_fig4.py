import matplotlib.pyplot as plt

# Data for Table 4
disciplines = ['Humanities', 'Social Sciences',
              'Natural Sciences', 'Engineering']
high_adoption = [65, 60, 40, 35]
moderate_adoption = [25, 30, 35, 40]
low_adoption = [10, 10, 25, 25]

# Plotting the 100% stacked bar chart
fig, ax = plt.subplots(figsize=(8, 6))

# Stacking the bars
ax.barh(disciplines, low_adoption, color='#f56565', label='Low Adoption')
ax.barh(disciplines, moderate_adoption, left=low_adoption,
       color='#f6ad55', label='Moderate Adoption')
ax.barh(disciplines, high_adoption, left=[
        i + j for i, j in zip(low_adoption, moderate_adoption)], color='#68d391', label='High Adoption')

# Labels and title
ax.set_xlabel('Percentage (%)')
ax.set_title('Adoption Rates of Reflective Practice by Discipline')

# Customizing legend placement to not overlap the chart
ax.legend(loc='best')

# Display the chart
plt.tight_layout()
plt.show()
