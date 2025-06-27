import pulp


def my_model() -> dict:
    # Створюємо модель
    model = pulp.LpProblem("Drinkins", pulp.LpMaximize)

    x = pulp.LpVariable('lemonade', lowBound=0, cat='integer')
    y = pulp.LpVariable('juice', lowBound=0, cat='integer')

    model += x + y, "Maximum value"

    # Визначаємо обмеження
    model += 2 * x + 1 * y <= 100, "water limit"
    model += 1 * x <= 50, "sugar limit"
    model += 1 * x <= 30, "lemon juice limit"
    model += 2 * y <= 40, "fruit jam limit"

    model.solve()

    return {
        "lemonade": x.varValue,
        "fruit_juice": y.varValue,
        "max_value": pulp.value(model.objective)
    }


def main():
    model = my_model()
    print(f"Необхідна кількість лимонаду: {model["lemonade"]}")
    print(f"Необхідна кількість фруктового соку: {model["fruit_juice"]}")
    print(f"Максимальна можлива кількість продукту: {model["max_value"]}")


if __name__ == "__main__":
    main()