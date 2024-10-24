"""

MIT License

Copyright (c) 2021 Dev Kumar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use("Agg")

# === Documentation of graphing.py ===


def viewBudget(data):
    sorted_data = {}
    sorted_data = {k: v for k, v in sorted(data.items(), key=lambda item: item[1])}
    values = []
    labels = []
    for k, v in sorted_data.items():
        values.append(v)
        labels.append(k)
    plt.pie(values, labels=values, counterclock=False, shadow=True)
    plt.title("Category Wise Budget")
    plt.legend(labels, loc="center")
    plt.savefig("budget.png", bbox_inches="tight")
    plt.close()


def addlabels(x, y):
    """
    addlabels(x, y): This function is used to add the labels to the graph.
    It takes the expense values and adds the values inside the bar graph for each expense type
    """
    for i in range(len(x)):
        plt.text(i, y[i] // 2, y[i], ha="center")


def visualize(total_text, monthly_budget):
    """
    visualize(total_text): This is the main function used to implement the graphing
    part of display feature. This file is called from display.py, and takes the user
    expense as a string and creates a dictionary which in turn is fed as input matplotlib to create the graph
    """
    n1 = len(monthly_budget)
    r1 = np.arange(n1)
    width = 0.45
    total_text_split = [line for line in total_text.split("\n") if line.strip() != ""]
    monthly_budget_str = ""
    for key, value in monthly_budget.items():
        monthly_budget_str += str(key) + " $" + str(value) + "\n"
    monthly_budget_split = [
        line for line in monthly_budget_str.split("\n") if line.strip() != ""
    ]

    monthly_budget_categ_val = {}
    for j in monthly_budget_split:
        x = j.split(" ")
        x[1] = x[1].replace("$", "")
        monthly_budget_categ_val[x[0]] = float(x[1])

    categ_val = {key: 0 for key in monthly_budget_categ_val}
    for i in total_text_split:
        a = i.split(" ")
        a[1] = a[1].replace("$", "")
        categ_val[a[0]] = float(a[1])

    x = list(categ_val.keys())
    y = list(categ_val.values())
    n2 = len(x)
    r2 = np.arange(n2)
    plt.bar(r2, categ_val.values(), width=width, label="your spendings")
    plt.bar(
        r1 + width, monthly_budget_categ_val.values(), width=width, label="your budget"
    )
    addlabels(x, y)

    plt.ylabel("Expenditure")
    plt.xlabel("Categories")
    plt.xticks(r1 + width / 2, monthly_budget_categ_val.keys(), rotation=90)
    plt.legend()
    plt.savefig("expenditure.png", bbox_inches="tight")
    plt.close()
