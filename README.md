"# Daily Horoscope Web Application

A Flask-based web application that provides daily horoscope readings and cosmic tips for all zodiac signs. The application can work with both static horoscope data and AI-generated content using Google's Gemini API.

## Features

- Daily horoscope readings for all 12 zodiac signs
- Personalized cosmic tips
- Automatic zodiac sign detection based on birth date
- Clean and intuitive user interface
- Support for both static and AI-generated content

## Prerequisites

- Python 3.10 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/pankajAdhikari2002/Horoscope_WebApp.git
   cd Horoscope_WebApp
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### Basic Setup (Static Content)
- No additional configuration needed
- The app will use pre-defined horoscope content

### AI-Generated Content (Optional)
1. Get a Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Set the API key as an environment variable:
   ```bash
   export GEMINI_API_KEY=your_api_key_here
   ```

## Running the Application

1. Start the Flask development server:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## Usage

1. Enter your name and date of birth on the homepage
2. Click 'Get Horoscope' to view your daily horoscope
3. Receive personalized predictions and cosmic tips

## Project Structure

- `app.py`: Main Flask application file
- `script.py`: Horoscope generation logic
- `horoscope.json`: Daily horoscope data
- `templates/`: HTML templates
- `static/`: CSS, JavaScript, and other static files

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Flask web framework
- Google Gemini API (for AI-generated content)
- Bootstrap for UI components" 
