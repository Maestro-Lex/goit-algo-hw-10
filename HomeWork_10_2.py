import numpy as np
import sympy as sp
from scipy.integrate import quad
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# Функція, яку інтегруємо
def func(x):
    return -2 * x**2 + 4 * x + 5

# Границі інтегрування
a, b = -10, 10
    
x = sp.Symbol('x')
f = func(x)

# Задаємо значення для побудови графіку функції
x_values = np.linspace(a - 10, b + 10, 100)
y_values = sp.lambdify(x, f, 'numpy')(x_values)

# Розрахуємо максимальне та мінімальне значення функції на відрізку a - b 
temp_x = np.linspace(a, b, 100)
temp_y = sp.lambdify(x, f, 'numpy')(temp_x)
min_y_value = 0 if np.min(temp_y) > 0 else np.min(temp_y)
max_y_value = np.max(temp_y) if np.max(temp_y) > 0 else 0

# Площа прямокутника, утвореного відрізком a - b по осі Х та min_y_value - max_y_value по осі У
S_square = abs(b - a) * abs(max_y_value - min_y_value)

# Значення аналітичної площі фігури як чисельного інтегралу
integr_analit, error = quad(lambda x: func(x), a, b)

#------------------------------------------------------#
# Метод Монте-Карло
N = 100_000 # кількість випадкових точок
# Генерація випадкових точок
x_rand = np.random.uniform(a, b, N)
y_rand = np.random.uniform(min_y_value, max_y_value, N)

inside_pioints_pos = [
    1 for i in range(N)
    if (func(x_rand[i]) >= y_rand[i] and func(x_rand[i]) >= 0 and y_rand[i] >= 0)
]

inside_pioints_neg = [
    1 for i in range(N)
    if (func(x_rand[i]) <= y_rand[i] and func(x_rand[i]) < 0 and y_rand[i] < 0)
]

# Значення інтегралу як аналітичної площі фігури
integr_exp = (len(inside_pioints_pos) - len(inside_pioints_neg)) / N * S_square
#------------------------------------------------------#

# Створюємо область графіку та малюємо криву функції та наносимо згенеровані точки
fig, ax = plt.subplots(figsize=(15, 8))
ax.plot(x_values, y_values, 'r', linewidth = 2)
ax.plot(x_rand, y_rand, 'bo')

# Перемістимо лівий і нижній стовпчики до x = a - 10 і y = 0 відповідно.
ax.spines[["left", "bottom"]].set_position(("data", a - 0.1 * abs(a)))

# Сховати верхню та праву лінію
ax.spines[["top", "right"]].set_visible(False)

# Намалюємо стрілки (як чорні трикутники: ">k"/"^k") на кінцях осей.
# Також вимкнемо відсікання (clip_on=False) стрілок.
ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)

# Додамо проміжні лінії
ax.grid(True, linestyle='-.')

# Оформлюємо область
# Генеруємо значення x та y в області фігури
ix = np.linspace(a, b)
iy = sp.lambdify(x, f, 'numpy')(ix)

# Зафарбовуємо область
verts = [(a, 0), *zip(ix, iy), (b, 0)]
poly = Polygon(verts, facecolor='0.9', edgecolor='0.5')
ax.add_patch(poly)

# малюємо графік функції та горизонталні межі обрахунку
if max_y_value:
    ax.axhline(y = max_y_value, color='green', linestyle='--')
    ax.text(b +  0.1 * abs(b), max_y_value, f"{max_y_value:.2f}", color="green",
        horizontalalignment='left', fontsize=15)
if min_y_value:
    ax.axhline(y = min_y_value, color='green', linestyle='--')
    ax.text(b +  0.1 * abs(b), min_y_value, f"{min_y_value:.2f}", color="green",
        horizontalalignment='left', fontsize=15)

# Задаємо характеристики площини відображення
ax.text(b +  0.1 * abs(b) + 0.1, 0, "x", color="black",
        horizontalalignment='left', fontsize=15)
ax.set_ylabel('f(x)', fontsize=15)
ax.set_xlim(a - 0.1 * abs(a), b + 0.1 * abs(b))
ax.set_ylim(min_y_value * 1.1, max_y_value * 1.1)
ax.axvline(x=a, color='gray', linestyle='--')
ax.axvline(x=b, color='gray', linestyle='--')

# Виводимо рішення у титулній строчці
title = r"$Графік\ функції\ f(x)\ =\ " + sp.latex(f) + r"\ на\ відрізку\ '{%d}'\ -\ '{%d}'$" % (a, b) + "\n"
title += r"$\int_{%d}^{%d} (" % (a, b) + sp.latex(f) + r")\mathrm{d}x\ =\ %.3f$" % integr_analit + "\n"
title += r"$Значення\ за\ методом\ Монте-Карло\ =\ %.3f$" % integr_exp + r"$\ (при\ кількості\ точок\ -\ {%d})$" % (N)
ax.set_title(title)

plt.show()