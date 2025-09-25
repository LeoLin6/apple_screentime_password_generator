#!/usr/bin/env python3
import random
import time
import subprocess
import sys
from PIL import Image, ImageDraw, ImageFont
import os

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
            return False
    except Exception as e:
        return False

def generate_random_string(length):
    """Generate a random string of digits"""
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

def create_text_image(text, width=800, height=600, font_size=34):
    """Create an image with text"""
    # Create a black background
    img = Image.new('RGB', (width, height), color='black')
    draw = ImageDraw.Draw(img)
    
    # Try to use a default font, fallback to basic if not available
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Monaco.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", font_size)
        except:
            font = ImageFont.load_default()
    
    # Split text into lines and draw them
    lines = text.split('\n')
    y_offset = 50
    
    for line in lines:
        # Center the text horizontally
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        
        draw.text((x, y_offset), line, fill='white', font=font)
        y_offset += font_size + 10
    
    return img

def output_password(target_indices, random_string, string_length, outputs):
    """Modified output_password that saves to outputs list instead of printing"""
    # Initialize state variables
    digits_on_screen = 0
    total_digits_typed = 0
    correct_digits_typed = 0
    
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
            # Combine all step outputs into one frame
            step_output = f"--- Step {step} ---\n"
            step_output += f"Enter this digit: {digit_to_enter}\n"
            #step_output += "Press Enter after you've typed this digit into your iPhone...\n"
            digits_on_screen += digits_to_type
            total_digits_typed += digits_to_type
            step_output += f"Digits on screen: {digits_on_screen}"
            outputs.append(step_output)
            step += 1

        # Deletion logic: only delete if we have non-target digits on screen
        if correct_digits_typed < digits_on_screen:
            if random.random() < 0.5:
                # Combine all deletion step outputs into one frame
                step_output = f"--- Step {step} ---\n"
                step_output += "Delete 1 digit from the right\n"
                #step_output += "Press Enter after you've deleted this digit...\n"
                digits_on_screen -= 1
                step_output += f"Digits on screen: {digits_on_screen}"
                outputs.append(step_output)
                step += 1
    
    outputs.append("=" * 40 + "\n🎉 PASSWORD COMPLETE!")

def main():
    outputs = []
    
    # Initial setup - combine into one frame
    initial_output = "= Screentime Password Generator =\n"
    initial_output += "Memory Erasure Technique\n"
    initial_output += "=" * 40
    outputs.append(initial_output)
    
    # Generate a long random string (10-15 digits)
    string_length = random.randint(10, 15)
    random_string = generate_random_string(string_length)
    
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
    
    # First password generation
    output_password(target_indices, random_string, string_length, outputs)
    
    # Reenter password section - combine into one frame
    reenter_output = "\n\n" + "=" * 40 + "\n"
    reenter_output += "Reenter the password:\n"
    reenter_output += "=" * 40
    outputs.append(reenter_output)
    
    output_password(target_indices, random_string, string_length, outputs)
    
    # Final messages - combine into one frame
    final_output = "✅ Password copied to clipboard!\n"
    final_output += "The memory erasure process helped you forget the intermediate steps!\n"
    final_output += "=" * 40
    outputs.append(final_output)
    
    # Create images for each output
    print("Creating images...")
    image_files = []
    
    for i, output in enumerate(outputs):
        img = create_text_image(output)
        filename = f"frame_{i:03d}.png"
        img.save(filename)
        image_files.append(filename)
        print(f"Created frame {i+1}/{len(outputs)}: {output[:50]}...")
    
    # Create video using ffmpeg
    print("Creating video...")
    try:
        # Create video with 10 seconds per frame
        cmd = [
            'ffmpeg', '-y',  # -y to overwrite output file
            '-framerate', '1/10',  # 1 frame per 10 seconds
            '-i', 'frame_%03d.png',  # Input pattern
            '-c:v', 'libx264',  # Video codec
            '-pix_fmt', 'yuv420p',  # Pixel format for compatibility
            'password_generator_demo.mp4'  # Output file
        ]
        
        subprocess.run(cmd, check=True)
        print("✅ Video created: password_generator_demo.mp4")
        
        # Clean up image files
        for filename in image_files:
            os.remove(filename)
        print("✅ Cleaned up temporary image files")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating video: {e}")
        print("Make sure ffmpeg is installed: brew install ffmpeg")
    except FileNotFoundError:
        print("❌ ffmpeg not found. Please install it:")
        print("  macOS: brew install ffmpeg")
        print("  Ubuntu: sudo apt install ffmpeg")
        print("  Windows: Download from https://ffmpeg.org/")

if __name__ == "__main__":
    main()
