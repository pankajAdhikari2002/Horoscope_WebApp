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

        # Create a Beautiful Soup object
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all elements with a specific class name
        elements_with_class = soup.find_all(class_='product-block-full')

        data_f = {}
        data_f["Date"] = f"{day} {month} {year}"


        # Loop through the found elements
        # Most of the time prone to bugg is this code 👇
        for element in elements_with_class:
            symbol = element.find(class_="product-title").text.strip().split(" ")[0]
            content = element.find(class_="product-summary").find_all('p') # Splitting the desc with cosmic tip was giving problem so extracting adn displaying as a whole.
            content = [
                c.text
                for c in content
                if len(c.text) > 20
            ]
            data_f[symbol] = {"desc": content[0], "cosmic_tip": content[1][12:]} # This code might have a problem in the future!
        
        print(data_f)
        
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

