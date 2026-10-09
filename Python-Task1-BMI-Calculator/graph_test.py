import matplotlib.pyplot as plt

dates = ["Oct 1", "Oct 5", "Oct 10", "Oct 15"]

bmi_values = [27.5, 26.8, 26.1, 25.7]

plt.plot(dates, bmi_values, marker="o")

plt.xlabel("Date")
plt.ylabel("BMI")

plt.title("BMI Trend")

plt.show()