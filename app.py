def parse_frequency_input(frequency_input):
    """
    Parse user input to extract the frequency value in Hz.

    :param frequency_input: The frequency input as a string (e.g., "72MHz", "72M", "1kHz")
    :return: The frequency in Hz as a float
    """
    units = {
        'hz': 1,
        'khz': 1e3,
        'mhz': 1e6,
        'ghz': 1e9,
        'k': 1e3,
        'm': 1e6,
        'g': 1e9
    }

    # Extract numeric value and optional unit
    import re
    match = re.match(r"([\d\.]+)\s*([a-zA-Z]*)", frequency_input.strip())
    if not match:
        raise ValueError("Invalid frequency input format. Use formats like '72MHz', '1k', '1kHz', etc.")

    value, unit = match.groups()
    value = float(value)
    unit = unit.lower() or 'hz'  # Default to 'hz' if no unit is provided

    if unit not in units:
        raise ValueError(f"Unsupported unit '{unit}'. Supported units are: Hz, kHz, MHz, GHz, k, m, g.")

    return value * units[unit]

def calculate_pwm_configurations(target_frequency, timer_clock):
    """
    Calculate all possible prescaler and counter period (ARR) combinations for a given PWM frequency.

    :param target_frequency: The desired PWM frequency (Hz)
    :param timer_clock: The clock frequency of the timer (Hz)
    :return: A list of (Prescaler, Counter Period) tuples
    """
    results = []

    # Loop through all possible prescaler values (1 to 65536)
    for prescaler in range(1, 65537):
        # Calculate the counter period (ARR) for the current prescaler
        counter_period = timer_clock / (prescaler * target_frequency)

        # Check if the counter period is a valid integer and within the 16-bit range
        if 1 <= counter_period <= 65535 and counter_period.is_integer():
            results.append((prescaler, int(counter_period)))

    return results

# Example usage
if __name__ == "__main__":
    try:
        # Input parameters
        target_frequency_input = input("Enter target PWM frequency (e.g., 1kHz, 72MHz): ")
        timer_clock_input = input("Enter timer clock frequency (e.g., 72MHz): ")

        # Parse inputs
        target_frequency = parse_frequency_input(target_frequency_input)
        timer_clock = parse_frequency_input(timer_clock_input)

        # Calculate configurations
        configurations = calculate_pwm_configurations(target_frequency, timer_clock)

        # Print results
        if configurations:
            print(f"\nPossible Prescaler and Counter Period combinations for {target_frequency} Hz:")
            for prescaler, counter_period in configurations:
                print(f"Prescaler: {prescaler}, Counter Period (ARR): {counter_period}")
        else:
            print("\nNo valid configurations found for the given frequency and timer clock.")

    except ValueError as e:
        print(f"Error: {e}")
