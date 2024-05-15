from bs4 import BeautifulSoup
import datetime
import json
import requests


def runScript():
    try:
        today = datetime.date.today()
        day, month, year = today.strftime("%d %B %Y").split(" ")
        url = f"https://www.vogue.in/horoscope/collection/horoscope-today-{month.lower()}-{int(day)}-{year}/"
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad response status codes

        html_content = response.text

        # Create a Beautiful Soup object
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all elements with a specific class name
        elements_with_class = soup.find_all(class_='product-block-full')

        data_f = {}
        data_f["Date"] = f"{day} {month} {year}"

        # Loop through the found elements
        for element in elements_with_class:
            symbol = element.h2.text.split(" ")[0]
            content = element.find(class_="product-summary").text
            desc, cosmic_tip = content.split("Cosmic tip: ")
            data_f[symbol] = {"desc": desc, "cosmic_tip": cosmic_tip}

        # Serializing json
        json_object = json.dumps(data_f, indent=4, ensure_ascii=False)

        # Writing to sample.json
        with open(file="horoscope.json", mode="w", encoding="utf-8") as outfile:
            outfile.write(json_object)
        return {"Message": "Script ran successfully!"}

    except requests.exceptions.RequestException as e:
        return {"Message for Request Error" : str(e)}

    except Exception as e:
        return {"Message for Script Error" : str(e)}
