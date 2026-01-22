import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return x**2 + 4*x +4

def df(x):
    return 2*x + 4

def gradient_decent(starting_point, learning_rate,iteration):
    x = starting_point
    for i in range (iteration):
        x = x - learning_rate * df(x)
        print(f"Iteration {i+1}: x = {x:.4f}, f(x) = {f(x):.4f}")
    return x

starting_point = 0
learning_rate = 0.1
iteration = 5

minimum = gradient_decent(starting_point, learning_rate,iteration)
print(f"\nLocal minimum occurs at x = {minimum:.4f}, f(x) = {f(minimum):.4f}")

x_vals = np.linspace(-10, 2, 100)
y_vals = f(x_vals)
plt.plot(x_vals, y_vals, label="f(x) = x^2 + 4x + 4")
plt.scatter(minimum, f(minimum), color='green', label="Local Minimum")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.title("Gradient Descent Visualization")
plt.legend()
plt.show()