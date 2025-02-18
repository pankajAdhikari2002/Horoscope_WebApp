from flask import Flask, render_template, request, url_for, redirect
import json
import datetime
import logging
from config import supabase

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def find_sign(dob):
    try:
        x = datetime.datetime.strptime(dob, '%Y-%m-%d')
    except ValueError:
        raise ValueError('Invalid date format. Please use YYYY-MM-DD format.')
    date_f = x.strftime('%d %B %Y').split(" ")
    day = int(date_f[0])
    month = date_f[1].lower()
    if month == 'december':  
        sun_sign = 'Sagittarius' if (day < 22) else 'Capricorn'  
    elif month == 'january':  
        sun_sign = 'Capricorn' if (day < 20) else 'Aquarius'  
    elif month == 'february':  
        sun_sign = 'Aquarius' if (day < 19) else 'Pisces'  
    elif month == 'march':  
        sun_sign = 'Pisces' if (day < 21) else 'Aries'  
    elif month == 'april':  
        sun_sign = 'Aries' if (day < 20) else 'Taurus'  
    elif month == 'may':  
        sun_sign = 'Taurus' if (day < 21) else 'Gemini'  
    elif month == 'june':  
        sun_sign = 'Gemini' if (day < 21) else 'Cancer'  
    elif month == 'july':  
        sun_sign = 'Cancer' if (day < 23) else 'Leo'  
    elif month == 'august':  
        sun_sign = 'Leo' if (day < 23) else 'Virgo'  
    elif month == 'september':  
        sun_sign = 'Virgo' if (day < 23) else 'Libra'  
    elif month == 'october':  
        sun_sign = 'Libra' if (day < 23) else 'Scorpio'  
    elif month == 'november':  
        sun_sign = 'Scorpio' if (day < 22) else 'Sagittarius'  
    return sun_sign.lower()

def get_horoscope_data():
    try:
        logger.info("Attempting to fetch data from Supabase")
        # Get latest horoscope data from Supabase
        response = supabase.table('horoscopes').select('data').order('created_at', desc=True).limit(1).execute()
        logger.debug(f"Supabase response: {response}")
        
        if not response.data:
            logger.info("No data in Supabase, falling back to JSON file")
            # Fallback to JSON file if no data in Supabase
            with open("horoscope.json", "r", encoding="utf-8") as outfile:
                data = json.load(outfile)
                logger.debug(f"Loaded data from JSON file: {data}")
                return data
        
        logger.info("Successfully retrieved data from Supabase")
        return response.data[0]['data']
    except Exception as e:
        logger.error(f"Error fetching from Supabase: {str(e)}")
        logger.info("Falling back to JSON file")
        # Fallback to JSON file if Supabase fails
        with open("horoscope.json", "r", encoding="utf-8") as outfile:
            data = json.load(outfile)
            logger.debug(f"Loaded data from JSON file: {data}")
            return data

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        user_name = request.form['name']
        user_dob = request.form['dob']
        astro_sign = find_sign(user_dob)
        logger.info(f"Redirecting to info page with astro_sign={astro_sign}, name={user_name}")
        return redirect(url_for("info", astro_sign=astro_sign, name=user_name.split(" ")[0]))
    
    return render_template("homepage.html")

@app.route("/info/<astro_sign>/<name>")
def info(astro_sign, name):
    try:
        logger.info(f"Fetching horoscope for sign: {astro_sign}, name: {name}")
        today_data = get_horoscope_data()
        logger.debug(f"Retrieved horoscope data: {today_data}")
        
        if not isinstance(today_data, dict):
            logger.error(f"Invalid data format. Expected dict, got {type(today_data)}")
            return render_template('error.html', err='Invalid data format received from database.'), 500
            
        data = today_data.get(astro_sign.title())
        if data is None:
            logger.error(f"Zodiac sign not found: {astro_sign.title()}")
            return render_template('error.html', err=f'Invalid zodiac sign: {astro_sign}'), 400
            
        logger.info("Successfully retrieved horoscope data")
        return render_template("infopage.html", astro_sign=astro_sign, data=data, name=name)
    except FileNotFoundError as e:
        logger.error(f"File not found error: {str(e)}")
        return render_template('error.html', err='Horoscope data not available. Please try again later.'), 500
    except KeyError as e:
        logger.error(f"Key error: {str(e)}")
        return render_template('error.html', err='Invalid zodiac sign provided.'), 400
    except Exception as e:
        logger.error(f"Unexpected error in info route: {str(e)}")
        return render_template('error.html', err=f'Error reading horoscope data: {str(e)}'), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', err=e), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('error.html', err=e), 500

if __name__ == "__main__":
    # Only bind to localhost in development
    app.run(host="127.0.0.1", port=5001, debug=True)
