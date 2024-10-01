import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def is_valid_solution(b, c):
    return (b + c > 800) and (b < 800) and (c < 800) and (566 <= b <= 799) and (566 <= c <= 799)

def find_solutions():
    solutions = []
    best_diff = float('inf')
    best_solution = None
    
    for b in range(566, 800):
        for c in range(566, 800):
            if is_valid_solution(b, c):
                diff = abs(b**2 + c**2 - 800**2)
                solutions.append((b, c, diff))
                if diff < best_diff:
                    best_diff = diff
                    best_solution = (b, c, diff)
    
    return solutions, best_solution

solutions, best_solution = find_solutions()

fig, ax = plt.subplots(figsize=(10, 8))
scatter = ax.scatter([], [], c=[], cmap='viridis', alpha=0.6)
best_point, = ax.plot([], [], 'r*', markersize=15)

ax.set_xlim(565, 800)
ax.set_ylim(565, 800)
ax.set_xlabel('B')
ax.set_ylabel('C')
ax.set_title('Dynamic Solution Process for Right Triangle (A=800)')

text = ax.text(0.02, 0.98, '', transform=ax.transAxes, va='top')

def init():
    scatter.set_offsets(np.empty((0, 2)))
    best_point.set_data([], [])
    text.set_text('')
    return scatter, best_point, text

def update(frame):
    data = solutions[:frame]
    if data:
        x, y, diff = zip(*data)
        scatter.set_offsets(np.c_[x, y])
        scatter.set_array(np.array(diff))
        
        current_best = min(data, key=lambda x: x[2])
        best_point.set_data(current_best[0], current_best[1])
        
        text.set_text(f'Current best: B={current_best[0]}, C={current_best[1]}\n'
                      f'Difference: {current_best[2]}')
    
    return scatter, best_point, text

anim = FuncAnimation(fig, update, frames=len(solutions)+1, init_func=init, blit=True, interval=50)

plt.colorbar(scatter, label='Difference from 800^2')
plt.tight_layout()
plt.show()

print(f"Best solution: B={best_solution[0]}, C={best_solution[1]}")
print(f"Sum B+C: {best_solution[0] + best_solution[1]}")
print(f"Difference from 800^2: {best_solution[2]}")
