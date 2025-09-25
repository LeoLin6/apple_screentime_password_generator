#!/usr/bin/env python3
from flask import Flask, render_template, jsonify, send_file, request
import random
import subprocess
import os
import tempfile
import json
from PIL import Image, ImageDraw, ImageFont
import uuid

app = Flask(__name__)

def generate_random_string(length):
    """Generate a random string of digits"""
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

def create_text_image(text, width=800, height=600, font_size=48):
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
    y_offset = 100
    line_height = font_size + 20
    
    for line in lines:
        if line.strip():  # Only draw non-empty lines
            # Center the text horizontally
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            
            draw.text((x, y_offset), line, fill='white', font=font)
            y_offset += line_height
    
    return img

def generate_password_steps():
    """Generate password steps and return the data"""
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
    
    # Generate steps
    steps = []
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
            step_text = f"--- Step {step} ---\n"
            step_text += f"Enter this digit: {digit_to_enter}\n"
            digits_on_screen += digits_to_type
            total_digits_typed += digits_to_type
            step_text += f"Digits on screen: {digits_on_screen}"
            steps.append(step_text)
            step += 1

        # Deletion logic: only delete if we have non-target digits on screen
        if correct_digits_typed < digits_on_screen:
            if random.random() < 0.5:
                step_text = f"--- Step {step} ---\n"
                step_text += "Delete 1 digit from the right\n"
                digits_on_screen -= 1
                step_text += f"Digits on screen: {digits_on_screen}"
                steps.append(step_text)
                step += 1
    
    steps.append("=" * 40 + "\n🎉 PASSWORD COMPLETE!")
    
    return {
        'target_password': target_password,
        'steps': steps,
        'random_string': random_string,
        'target_indices': target_indices
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_password():
    """Generate password and create video"""
    try:
        # Generate password data
        data = generate_password_steps()
        
        # Create temporary directory for this session
        session_id = str(uuid.uuid4())
        temp_dir = tempfile.mkdtemp(prefix=f"password_gen_{session_id}_")
        
        # Create images for each step
        image_files = []
        for i, step_text in enumerate(data['steps']):
            img = create_text_image(step_text)
            filename = os.path.join(temp_dir, f"frame_{i:03d}.png")
            img.save(filename)
            image_files.append(filename)
        
        # Create video using ffmpeg
        video_filename = os.path.join(temp_dir, "password_demo.mp4")
        try:
            cmd = [
                'ffmpeg', '-y',  # -y to overwrite output file
                '-framerate', '1/10',  # 1 frame per 10 seconds
                '-i', os.path.join(temp_dir, 'frame_%03d.png'),  # Input pattern
                '-c:v', 'libx264',  # Video codec
                '-pix_fmt', 'yuv420p',  # Pixel format for compatibility
                video_filename  # Output file
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            
            # Move video to static directory for serving
            static_video_path = os.path.join('static', f'password_demo_{session_id}.mp4')
            os.makedirs('static', exist_ok=True)
            os.rename(video_filename, static_video_path)
            
            # Clean up temporary directory
            for filename in image_files:
                os.remove(filename)
            os.rmdir(temp_dir)
            
            return jsonify({
                'success': True,
                'password': data['target_password'],
                'video_url': f'/static/password_demo_{session_id}.mp4'
            })
            
        except subprocess.CalledProcessError as e:
            # Clean up on error
            for filename in image_files:
                if os.path.exists(filename):
                    os.remove(filename)
            if os.path.exists(temp_dir):
                os.rmdir(temp_dir)
            
            return jsonify({
                'success': False,
                'error': 'Failed to create video. Make sure ffmpeg is installed.'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8080))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug, host='0.0.0.0', port=port)
