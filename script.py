import json
import datetime
from config import supabase
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone

def get_default_horoscope():
    return {
        "Date": datetime.datetime.now().strftime("%d %b %Y | %I:%M:%S %p"),
        "Aries": {
            "desc": "Today is a great day for new beginnings. Your natural leadership abilities are heightened.",
            "cosmic_tip": "Take the initiative in important matters."
        },
        "Taurus": {
            "desc": "Focus on practical matters and financial security today.",
            "cosmic_tip": "Invest in your future stability."
        },
        "Gemini": {
            "desc": "Your communication skills are particularly strong today.",
            "cosmic_tip": "Share your ideas with confidence."
        },
        "Cancer": {
            "desc": "Trust your intuition in emotional matters today.",
            "cosmic_tip": "Listen to your inner voice."
        },
        "Leo": {
            "desc": "Your creative energy is at its peak today.",
            "cosmic_tip": "Express yourself boldly."
        },
        "Virgo": {
            "desc": "Focus on organizing and planning today.",
            "cosmic_tip": "Pay attention to details."
        },
        "Libra": {
            "desc": "Harmony in relationships is highlighted today.",
            "cosmic_tip": "Seek balance in all things."
        },
        "Scorpio": {
            "desc": "Your determination and focus are particularly strong today.",
            "cosmic_tip": "Trust your instincts."
        },
        "Sagittarius": {
            "desc": "Adventure and learning opportunities await you today.",
            "cosmic_tip": "Embrace new experiences."
        },
        "Capricorn": {
            "desc": "Professional opportunities are highlighted today.",
            "cosmic_tip": "Stay focused on your goals."
        },
        "Aquarius": {
            "desc": "Your innovative ideas can make a real difference today.",
            "cosmic_tip": "Think outside the box."
        },
        "Pisces": {
            "desc": "Your artistic and spiritual nature is enhanced today.",
            "cosmic_tip": "Follow your dreams."
        }
    }

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
