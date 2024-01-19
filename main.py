"""https://github.com/ganna-parkhomchuk/weather_bot.git"""

import requests
import json
import time
from typing import Dict, Any

import const


def answer_user_bot(data: Dict[str, Any]) -> requests.Response:
    """
    A function that sends a message to the chatbot using the Telegram API.
    Argument: data (Dict[str, Any])
    Returns: response
    """
    data = {
        'chat_id': const.MY_ID,
        'text': data
    }
    url = const.URL.format(
        token=const.TOKEN,
        method=const.SEND_METHOD
    )
    response = requests.post(url, data=data)
    return response


def parse_weather_data(data: Dict[str, Any]) -> str:
    """
    A function that parses weather data received from the OpenWeatherMap API.
    Argument: data (Dict[str, Any])
    Returns: str data - message with weather information.
    """
    weather_state = None
    for elem in data['weather']:
        weather_state = elem['main']
    temp = round(data['main']['temp'] - 273.15, 2)
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    city = data['name']
    msg = f'The weather in {city}: temperature is {temp}°C, humidity is {humidity}%, ' \
          f'wind speed is {wind_speed} m/s, state is {weather_state}'
    return msg


def get_weather(location: str) -> str:
    """
   A function that receives weather information for the specified location from the OpenWeatherMap API.
   Argument: location (str data) The city for which weather information is requested.
   Returns: (str data) A message containing the weather information.
   """
    url = const.WEATHER_URL.format(city=location,
                                   token=const.WEATHER_TOKEN)
    response = requests.get(url)
    if response.status_code != 200:
        return 'city not found'
    data = json.loads(response.content)
    return parse_weather_data(data)


def get_message(data: Dict[str, Any]) -> str:
    """
    A function that gets the text message from the data.
    Argument:data (Dict[str, Any])
    Returns: (str data) The text message.
    """
    return data['message']['text']


def save_update_id(update: Dict[str, Any]) -> bool:
    """
    Saves the update ID to a file and updates the global constant.
    Argument: update (Dict[str, Any])
    Returns: (bool data) True if the update ID is successfully saved.
    """
    with open(const.UPDATE_ID_FILE_PATH, 'w') as file:
        file.write(str(update['update_id']))
    const.UPDATE_ID = update['update_id']
    return True


def main() -> None:
    """
    Main function to continuously check for incoming messages and respond with weather information.
    """
    while True:
        try:
            url = const.URL.format(token=const.TOKEN, method=const.UPDATE_METHOD)
            content = requests.get(url).text

            data = json.loads(content)
            result = data['result'][::-1]
            needed_part = None

            for elem in result:
                if elem['message']['chat']['id'] == const.MY_ID:
                    needed_part = elem
                    break

            if const.UPDATE_ID != needed_part['update_id']:
                message = get_message(needed_part)
                msg = get_weather(message)
                answer_user_bot(msg)
                save_update_id(needed_part)

            time.sleep(1)

        except Exception as e:
            print(f'Error: {e}')
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    main()
