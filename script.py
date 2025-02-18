import json
import datetime

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
        # Use default horoscope data
        obj = get_default_horoscope()
        
        # Save to JSON file
        json_obj = json.dumps(obj, indent=4)
        with open("horoscope.json", "w", encoding="utf-8") as outfile:
            outfile.write(json_obj)
        
        return {"status": "success", "message": "Horoscope updated successfully!"}
    
    except Exception as e:
        return {"status": "error", "message": f"Error: {str(e)}"}

# Initialize horoscope.json when the script is imported
runScript()
