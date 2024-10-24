from code import graphing
import numpy as np

dummy_total_text_none = ""
dummy_total_text_data = """Food $10.0
Transport $50.0
Shopping $148.0
Miscellaneous $47.93
Utilities $200.0
Groceries $55.21\n"""

dummy_x = ["Food", "Transport", "Shopping", "Miscellaneous", "Utilities", "Groceries"]
dummy_y = [10.0, 50.0, 148.0, 47.93, 200.0, 55.21]
dummy_categ_val = {
    "Food": 10.0,
    "Transport": 50.0,
    "Shopping": 148.0,
    "Miscellaneous": 47.93,
    "Miscellaneous": 47.93,
    "Utilities": 200.0,
    "Groceries": 55.21,
}
dummy_color = [
    (1.00, 0, 0, 0.6),
    (0.2, 0.4, 0.6, 0.6),
    (0, 1.00, 0, 0.6),
    (1.00, 1.00, 0, 1.00),
]
dummy_edgecolor = "blue"
dummy_monthly_budget = {
    "Food": 100.0,
    "Transport": 150.0,
    "Shopping": 150.0,
    "Miscellaneous": 50,
    "Utilities": 200.0,
    "Groceries": 100,
}

n2 = len(dummy_x)
r2 = np.arange(n2)
width = 0.45


def test_visualize(mocker):
    mocker.patch.object(graphing, "plt")
    graphing.plt.bar.return_value = True
    graphing.visualize(dummy_total_text_data, dummy_monthly_budget)
    # graphing.plt.bar.assert_called_with(r2,
    # ANY, width=width, label='your spendings')
