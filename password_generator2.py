#!/usr/bin/env python3
import random
import time
import subprocess
import sys

def copy_to_clipboard(text):
    """Copy text to clipboard using different methods based on OS"""
    try:
        # For macOS
        if sys.platform == "darwin":
            process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
            process.communicate(input=text.encode('utf-8'))
            return True
        # For Linux
        elif sys.platform.startswith('linux'):
            process = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
            process.communicate(input=text.encode('utf-8'))
            return True
        # For Windows
        elif sys.platform == "win32":
            import pyperclip
            pyperclip.copy(text)
            return True
        else:
            print("Clipboard not supported on this platform")
            return False
    except Exception as e:
        print(f"Could not copy to clipboard: {e}")
        return False

def generate_random_string(length):
    """Generate a random string of digits"""
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

def main():
    print("=== Vibe Code Password Generator ===")
    print("Memory Erasure Technique")
    print("=" * 40)
    
    # Generate a long random string (10-15 digits)
    string_length = random.randint(10, 15)
    random_string = generate_random_string(string_length)
    
    #print(f"Generated random string: {random_string}")
    #print(f"Length: {string_length}")
    
    # Pick 4 target digits from the string
    target_indices = []
    
    # 1st digit: random position in first 2/3
    first_max = string_length - 6
    target_indices.append(random.randint(0, first_max))
    
    # 2nd digit: after 1st digit
    second_min = target_indices[0] + 1
    second_max = string_length - 4
    target_indices.append(random.randint(second_min, second_max))
    
    # 3rd digit: 2nd to last position
    target_indices.append(string_length - 2)
    
    # 4th digit: last position
    target_indices.append(string_length - 1)
    
    # Create target password
    target_password = ''.join([random_string[i] for i in target_indices])
    
    # Comment out password reveal to maintain memory erasure effect
    # print(f"Target indices: {target_indices}")
    # print(f"Target password: {target_password}")
    print("=" * 40)
    
    # Initialize state variables
    digits_on_screen = 0
    total_digits_typed = 0
    correct_digits_typed = 0
    current_digits = ""
    
    step = 1
    
    while correct_digits_typed < 4:
        
        # Check if the next digit to type is a target digit
        next_target_index = target_indices[correct_digits_typed]
        
        # Prevent entering 4th digit unless we're at the last position
        if digits_on_screen == 3 and total_digits_typed < string_length - 1:
            digits_to_type = 0  # Don't enter 4th digit unless at the end
        # If we're at a target digit position
        elif total_digits_typed == target_indices[correct_digits_typed]:
            # Check if this target digit will be placed in the correct position (rightmost)
            if correct_digits_typed == digits_on_screen:
                # Target digit will be placed in the right spot
                digits_to_type = 1
                correct_digits_typed += 1
                #print(f"✅ Found target digit {correct_digits_typed}/4!")
            else:
                # Target digit would be placed in wrong spot, skip for now
                digits_to_type = 0
        else:
            # Not at a target digit, randomly decide to insert or not
            if random.random() < 0.5:
                digits_to_type = 1
            else:
                digits_to_type = 0

        # Get the digit to type
        digit_to_enter = random_string[total_digits_typed]
        
        if digits_to_type > 0:
            print(f"\n--- Step {step} ---")
            print(f"Enter this digit: {digit_to_enter}")
            input("Press Enter after you've typed this digit into your iPhone...")
            digits_on_screen += digits_to_type
            total_digits_typed += digits_to_type
            print(f"Digits on screen: {digits_on_screen}")
            step += 1

        #print(f"Correct digits found: {correct_digits_typed}/4")

        # Deletion logic: only delete if we have non-target digits on screen
        if correct_digits_typed < digits_on_screen:
            if random.random() < 0.5:
                print(f"\n--- Step {step} ---")
                print(f"Delete 1 digit from the right")
                input("Press Enter after you've deleted this digit...")
                digits_on_screen -= 1
                print(f"Digits on screen: {digits_on_screen}")
                step += 1
        
    
    print("\n" + "=" * 40)
    print("🎉 PASSWORD COMPLETE!")
    
    # Copy the target password to clipboard automatically
    if copy_to_clipboard(target_password):
        print("✅ Password copied to clipboard!")
    else:
        print("❌ Could not copy to clipboard")
    
    print("The memory erasure process helped you forget the intermediate steps!")
    print("=" * 40)

if __name__ == "__main__":
    main() 