# Screentime Password Generator

A web application that generates secure passwords using the "Memory Erasure Technique" - a method that helps you forget the intermediate steps while creating a memorable password.

## Features

- **Memory Erasure Technique**: Generates passwords by walking through steps that you'll naturally forget
- **Video Generation**: Creates instructional videos showing the password generation process
- **Web Interface**: Clean, terminal-style web interface
- **Password Copy**: One-click password copying to clipboard
- **Video Download**: Download the generated instructional video

## How It Works

1. **Generate Random String**: Creates a 10-15 digit random number
2. **Select Target Digits**: Picks 4 specific digits to form the final password
3. **Step-by-Step Process**: Guides you through entering digits and deletions
4. **Memory Erasure**: The process is designed so you forget the intermediate steps
5. **Final Password**: Only the 4 target digits remain as your password

## Local Development

### Prerequisites
- Python 3.9+
- ffmpeg (for video generation)

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/screentime_pw_generator.git
cd screentime_pw_generator

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The app will be available at `http://localhost:8080`

## Deployment

### Azure App Service
1. Create an Azure App Service with Python runtime
2. Deploy from GitHub
3. Configure startup command: `startup.sh`
4. Your app will be live at `https://your-app-name.azurewebsites.net`

### Railway
1. Connect your GitHub repository
2. Railway will auto-detect Python and deploy
3. Add `nixpacks.toml` for ffmpeg support

## Files Structure

```
screentime_pw_generator/
├── app.py                    # Flask web server
├── templates/
│   └── index.html           # Web interface
├── static/                  # Generated videos
├── requirements.txt         # Python dependencies
├── web.config              # Azure configuration
├── startup.sh              # Linux startup script
├── .deployment             # Azure deployment config
└── .gitignore             # Git ignore rules
```

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **Video Generation**: ffmpeg + PIL
- **WSGI Server**: Gunicorn
- **Deployment**: Azure App Service / Railway

## License

MIT License - feel free to use and modify as needed.