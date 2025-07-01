def convert_length(value, from_unit, to_unit):
    meters = {
        'meters': 1,
        'kilometers': 1000,
        'centimeters': 0.01,
        'millimeters': 0.001,
        'miles': 1609.34,
        'yards': 0.9144,
        'feet': 0.3048,
        'inches': 0.0254
    }

    if from_unit not in meters or to_unit not in meters:
        raise ValueError("Unsupported length unit.")

    value_in_meters = value * meters[from_unit]
    return value_in_meters / meters[to_unit]

def convert_weight(value, from_unit, to_unit):
    grams = {
        'grams': 1,
        'kilograms': 1000,
        'milligrams': 0.001,
        'pounds': 453.592,
        'ounces': 28.3495
    }

    if from_unit not in grams or to_unit not in grams:
        raise ValueError("Unsupported weight unit.")

    value_in_grams = value * grams[from_unit]
    return value_in_grams / grams[to_unit]

def convert_temperature(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value

    if from_unit == 'celsius':
        if to_unit == 'fahrenheit':
            return (value * 9/5) + 32
        elif to_unit == 'kelvin':
            return value + 273.15

    if from_unit == 'fahrenheit':
        if to_unit == 'celsius':
            return (value - 32) * 5/9
        elif to_unit == 'kelvin':
            return (value - 32) * 5/9 + 273.15

    if from_unit == 'kelvin':
        if to_unit == 'celsius':
            return value - 273.15
        elif to_unit == 'fahrenheit':
            return (value - 273.15) * 9/5 + 32

    raise ValueError("Unsupported temperature unit.")

def convert(value, from_unit, to_unit, category):
    if category == 'length':
        return convert_length(value, from_unit, to_unit)
    elif category == 'weight':
        return convert_weight(value, from_unit, to_unit)
    elif category == 'temperature':
        return convert_temperature(value, from_unit, to_unit)
    else:
        raise ValueError("Unsupported category.")

def main():
    print("Welcome to the Unit Converter!")
    category = input("Choose category (length, weight, temperature): ").strip().lower()
    
    from_unit = input("Enter the unit you want to convert from: ").strip().lower()
    to_unit = input("Enter the unit you want to convert to: ").strip().lower()
    value = float(input("Enter the value you want to convert: "))

    try:
        result = convert(value, from_unit, to_unit, category)
        print(f"{value} {from_unit} is equal to {result} {to_unit}.")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()