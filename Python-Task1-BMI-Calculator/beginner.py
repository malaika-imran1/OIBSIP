print("===== BMI CALCULATOR =====")

try:
    # Get input
    weight = float(input("Enter your weight in kg: "))
    height = float(input("Enter your height in metres: "))

    # Validate input
    if weight <= 0 or height <= 0:
        print("Error: Weight and height must be greater than zero.")

    else:
        # Calculate BMI
        bmi = weight / (height ** 2)

        # Classify BMI
        if bmi < 18.5:
            category = "Underweight"

        elif bmi < 25:
            category = "Normal"

        elif bmi < 30:
            category = "Overweight"

        else:
            category = "Obese"

        # Display result
        print("\n===== RESULT =====")
        print(f"BMI: {bmi:.2f}")
        print(f"Category: {category}")

except ValueError:
    print("Error: Please enter numbers only.")