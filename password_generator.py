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
    
    # Generate a long random string (20-30 digits)
    string_length = random.randint(10, 15)
    random_string = generate_random_string(string_length)
    
    print(f"Generated random string: {random_string}")
    print(f"Length: {string_length}")
    
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
    
    print(f"Target indices: {target_indices}")
    print(f"Target password: {target_password}")
    print("=" * 40)
    
    # Initialize state variables
    digits_on_screen = 0
    total_digits_typed = 0
    correct_digits_typed = 0
    current_digits = ""
    
    step = 1
    
    while correct_digits_typed < 4:    # maybe ? <3 perhaps
        print(f"\n")
        
        # Calculate digits to type in (never exceed 3 digits on screen and never push a target digit out)


        next_target_index = target_indices[correct_digits_typed]  
        max_insertable = next_target_index - total_digits_typed + 1 #digits in between that can be put in before the next target digit
        
        if correct_digits_typed < 4:
            max_digits_to_type = min(3 - digits_on_screen, string_length - total_digits_typed, max_insertable)
        else:
            max_digits_to_type = min(3 - digits_on_screen, string_length - total_digits_typed)

        if(total_digits_typed == string_length-1):    # type in last 2 digits at the end regardless
            digits_to_type = 1
        elif(max_insertable == 1 and correct_digits_typed != digits_on_screen): #next one is the right digit but if we insert it now it wont be in right spot
            digits_to_type = 0
        elif max_digits_to_type > 0:
            digits_to_type = random.randint(1, max_digits_to_type) # type in random number of digits for first 2 digits
        else:
            digits_to_type = 0

        # Get the digits to type
        start_idx = total_digits_typed
        end_idx = total_digits_typed + digits_to_type
        digits_to_enter = random_string[start_idx:end_idx]
        
        if digits_to_type > 0:
            print(f"Enter these {digits_to_type} digit(s): {digits_to_enter}")
            input("Press Enter after you've typed these digits into your iPhone...")
            current_digits += digits_to_enter
            digits_on_screen += digits_to_type
            total_digits_typed += digits_to_type
            print(f"Digits on screen: {digits_on_screen}")

        # Check if we reached a target digit in the ones we entered
        if digits_to_type > 0 and total_digits_typed > 0:
            for i in range(digits_to_type):
                if (total_digits_typed - digits_to_type + i) == target_indices[correct_digits_typed]:
                    correct_digits_typed += 1
                    print(f"✅ Found target digit {correct_digits_typed}/4!")
                    break
        print(f"Correct digits found: {correct_digits_typed}/4")

        # Deletion logic: never delete a target digit already found and on screen
        if total_digits_typed != string_length - 2:
            max_safe_delete = digits_on_screen - correct_digits_typed
            if max_safe_delete > 0:
                digits_to_delete = random.randint(1, max_safe_delete)
                print(f"\nDelete {digits_to_delete} digit(s) from the right")
                input("Press Enter after you've deleted these digits...")
                current_digits = current_digits[:-digits_to_delete]
                digits_on_screen -= digits_to_delete
                print(f"Digits on screen: {digits_on_screen}")
        
        step += 1
    
    print("\n" + "=" * 40)
    print("🎉 PASSWORD COMPLETE!")
    print(f"Final password: {target_password}")
    print("The memory erasure process helped you forget the intermediate steps!")
    
    # Copy to clipboard
    if copy_to_clipboard(target_password):
        print("✅ Password copied to clipboard!")
    else:
        print("❌ Could not copy to clipboard")
    
    print("=" * 40)

if __name__ == "__main__":
    main() 