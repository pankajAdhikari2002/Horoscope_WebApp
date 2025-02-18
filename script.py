import google.generativeai as genai
import os
import json
import datetime
from config import supabase
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone

def get_default_horoscope():
    # Get API key
    apikey = os.getenv("GEMINI_API_KEY")

    # Ensure API key is not None
    if not apikey:
        raise ValueError("GEMINI_API_KEY is not set. Please check your environment variables.")

    # Configure the API
    genai.configure(api_key=apikey)

    # Create a model instance
    model = genai.GenerativeModel('gemini-pro')

    # Get current timestamp
    x = datetime.datetime.now().strftime("%d %b %Y | %I:%M:%S %p")

    # Prompt for horoscope generation
    prompt = """
    You are an astrologer generating unique daily horoscopes. Each execution should yield fresh insights, ensuring variety while aligning with each zodiac sign's characteristics. Generate a JSON response containing:  

    - A brief daily horoscope (max 110 words) tailored to each zodiac sign's personality, strengths, and challenges.  
    - A cosmic tip (max 15 words) offering guidance, motivation, or reflection.  

    Format:
    {
      "Aries": {
        "desc": "...",
        "cosmic_tip": "..."
      },
      "Taurus": {
        "desc": "...",
        "cosmic_tip": "..."
      },
      "...": {
        "desc": "...",
        "cosmic_tip": "..."
      }
    }
    Ensure horoscopes feel natural, insightful, and unique each time by incorporating dynamic themes, celestial influences, and emotional depth. Avoid repetition and clichés.
    """

    # Generate response
    response = model.generate_content(prompt)

    if not response.text:
        raise ValueError("API response is empty.")

    # Process JSON output
    output = response.text.replace("```", "").replace("json", "").strip()
    obj = json.loads(output)
    obj["Date"] = x  # Add timestamp
    
    return obj

def runScript():
    try:
        print("Starting horoscope update...")
        # Use default horoscope data
        obj = get_default_horoscope()
        print("Generated horoscope data")
        
        try:
            # Insert new data (no need to delete as we'll just have multiple versions)
            insert_response = supabase.table('horoscopes').insert({
                'data': obj,
                'created_at': datetime.datetime.now(timezone('UTC')).isoformat()
            }).execute()
            print(f"Inserted new data: {insert_response}")
        except Exception as db_error:
            print(f"Supabase error: {str(db_error)}")
            raise db_error
        
        # Also save to JSON file as backup
        json_obj = json.dumps(obj, indent=4)
        with open("horoscope.json", "w", encoding="utf-8") as outfile:
            outfile.write(json_obj)
        print("Saved backup to JSON file")
        
        return {"status": "success", "message": "Horoscope updated successfully!"}
    
    except Exception as e:
        print(f"Error in runScript: {str(e)}")
        return {"status": "error", "message": f"Error: {str(e)}"}

# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(
    runScript,
    trigger=CronTrigger(hour=6, minute=0, timezone=timezone('Asia/Kolkata')),
    id='update_horoscope',
    name='Update horoscope data daily at 6 AM IST',
    replace_existing=True
)

# Start the scheduler
scheduler.start()

# Initialize horoscope data when the script is imported
runScript()
