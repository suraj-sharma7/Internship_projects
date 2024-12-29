import random
import string

def generate_password(length, include_uppercase, include_lowercase, include_numbers, include_special):
    if length <= 0:
        return "Password length must be greater than 0."
    
    # Character pools
    uppercase = string.ascii_uppercase if include_uppercase else ""
    lowercase = string.ascii_lowercase if include_lowercase else ""
    numbers = string.digits if include_numbers else ""
    special_characters = string.punctuation if include_special else ""
    
    # Combine pools
    all_characters = uppercase + lowercase + numbers + special_characters
    
    # Ensure at least one type of character is included
    if not all_characters:
        return "You must select at least one type of character to include in the password."
    
    # Generate password
    password = "".join(random.choice(all_characters) for _ in range(length))
    
    # Ensure password contains at least one character of each selected type
    criteria = [
        random.choice(uppercase) if include_uppercase else "",
        random.choice(lowercase) if include_lowercase else "",
        random.choice(numbers) if include_numbers else "",
        random.choice(special_characters) if include_special else ""
    ]
    criteria = [c for c in criteria if c]  # Remove empty strings
    password = list(password)
    for i in range(len(criteria)):
        password[i] = criteria[i]
    random.shuffle(password)
    return "".join(password)

def main():
    print("Random Password Generator")
    print("-" * 30)
    
    # User input
    try:
        length = int(input("Enter the desired password length: "))
    except ValueError:
        print("Invalid input. Please enter a valid number for the password length.")
        return
    
    include_uppercase = input("Include uppercase letters? (y/n): ").strip().lower() == 'y'
    include_lowercase = input("Include lowercase letters? (y/n): ").strip().lower() == 'y'
    include_numbers = input("Include numbers? (y/n): ").strip().lower() == 'y'
    include_special = input("Include special characters? (y/n): ").strip().lower() == 'y'
    
    # Generate and display password
    password = generate_password(length, include_uppercase, include_lowercase, include_numbers, include_special)
    print("\nGenerated Password:")
    print(password)

if __name__ == "__main__":
    main()
