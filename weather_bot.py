from aiogram import Bot, Dispatcher, types, executor
from config import telegram_token, open_weather_token
import requests
import datetime

bot = Bot(token=telegram_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(messege: types.Message):
    await messege.reply("Привет напиши мне название города на латинском: ")

@dp.message_handler()
async def get_weather(messege: types.Message):
    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={messege.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        code_to_smile = {
            "Clear": "Ясно \U00002600",
            "Clouds": "Облачно \U00002601",
            "Rain": "Дождь \U00002614",
            "Drizzle": "Дождь \U00002614",
            "Thunderstorm": "Гроза \U000026A1",
            "Snow": "Снег \U0001F328",
            "Mist": "Туман \U0001F32B"
        }

        city = data['name']
        cur_weather = data['main']['temp']

        weather_description = data['weather'][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = 'Посмотри в окно сам!'

        humidity = data['main']['humidity']
        temp_max = data['main']['temp_max']
        temp_min = data['main']['temp_min']
        pressure = data['main']['pressure']
        speed_wind = data['wind']['speed']
        sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])

        await messege.reply(f"На {datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}\n"
              f"Температура в городе: {city}\nТемпература: {cur_weather}°С {wd}"
              f"\nВлажность: {humidity}\nМаксимальная температура: {temp_max}°С"
              f"\nМинимальная температура: {temp_min}°С\nДавление: {pressure}мм рт.ст."
              f"\nСкорость ветра: {speed_wind}м\\с\nВремя рассвета: {sunrise}"
              f"\nВремя заката: {sunset}\nСветовой день: {sunset-sunrise}"
                            f"\nОтличного дня!")

    except:

        await messege.reply("\U00002620 Проверьте название города! \U00002620")


if __name__ == "__main__":
    executor.start_polling(dp)

