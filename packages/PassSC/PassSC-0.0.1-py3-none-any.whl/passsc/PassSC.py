import re
import math

def calculate_crack_time(password):
    charset_size = 0
    if re.search(r'[a-z]', password):
        charset_size += 26  # Lowercase letters
    if re.search(r'[A-Z]', password):
        charset_size += 26  # Uppercase letters
    if re.search(r'[0-9]', password):
        charset_size += 10  # Digits
    if re.search(r'[@$!%*?&]', password):
        charset_size += 10  # Special symbols

    # Total possible combinations
    combinations = math.pow(charset_size, len(password))

    # Assuming 1 billion guesses per second
    guesses_per_second = 1_000_000_000
    seconds_to_crack = combinations / guesses_per_second

    return seconds_to_crack

def format_time(seconds):
    years = seconds / (365 * 24 * 3600)

    if years > 1_000_000_000:
        return f"{years / 1_000_000_000:.2f} billion years"
    elif years > 1_000_000:
        return f"{years / 1_000_000:.2f} million years"
    elif years > 1:
        return f"{years:.2f} years"
    else:
        return f"{seconds:.2f} seconds"

def check_password_strength(password):
    score = 0

    if len(password) >= 8:
        score += 1
    else:
        print("Password should be at least 8 characters.")

    if re.search(r'[a-z]', password):
        score += 1
    else:
        print("Password should contain at least one lowercase letter.")

    if re.search(r'[A-Z]', password):
        score += 1
    else:
        print("Password should contain at least one uppercase letter.")

    if re.search(r'[0-9]', password):
        score += 1
    else:
        print("Password should contain at least one digit.")

    if re.search(r'[@$!%*?&]', password):
        score += 1
    else:
        print("Password should contain at least one special character.")

    crack_time = calculate_crack_time(password)
    formatted_crack_time = format_time(crack_time)

    if score == 5:
        strength = "Strong Password!"
    elif 3 <= score < 5:
        strength = "Moderate Password."
    else:
        strength = "Weak Password."

    return strength, formatted_crack_time

def main():
    password = input("Enter your password: ")
    strength, formatted_crack_time = check_password_strength(password)
    print(f"Password Strength: {strength}")
    print(f"Estimated time to crack: {formatted_crack_time}")

if __name__ == "__main__":
    main()
