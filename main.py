import datetime
import requests
import pandas as pd
import warnings
from calendar import monthrange
#from pprint import pprint

# Поточна погода
def current_weather(latitude, longitude):
    try:
        r0 = requests.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&"
            f"hourly=temperature_2m,relativehumidity_2m,apparent_temperature,precipitation,surface_pressure,cloudcover,"
            f"windspeed_10m,windgusts_10m,winddirection_10m&"
            f"windspeed_unit=ms&"
            f"timezone=Europe%2FKiev&"
            f"start_date={datetime.datetime.now().strftime('%Y-%m-%d')}&"
            f"end_date={datetime.datetime.now().strftime('%Y-%m-%d')}")
        data_d0 = r0.json()
        #pprint(data_d0)

        time_idx = int()
        current_time = datetime.datetime.now().strftime('%Y-%m-%dT%H:00')
        for t in range(len(data_d0["hourly"]["time"])):
            if data_d0["hourly"]["time"][t] == current_time:
                if int(datetime.datetime.now().strftime('%M')) >= 30:
                    time_idx = t+1
                else:
                    time_idx = t

        temp = data_d0["hourly"]["temperature_2m"][time_idx]
        apparent_temp = data_d0["hourly"]["apparent_temperature"][time_idx]
        humidity = data_d0["hourly"]["relativehumidity_2m"][time_idx]
        precipitation = data_d0["hourly"]["precipitation"][time_idx]
        cloudcover = data_d0["hourly"]["cloudcover"][time_idx]
        pressure_hPa = data_d0["hourly"]["surface_pressure"][time_idx]
        windspeed = data_d0["hourly"]["windspeed_10m"][time_idx]
        windgusts = data_d0["hourly"]["windgusts_10m"][time_idx]
        winddirection = data_d0["hourly"]["winddirection_10m"][time_idx]

        # Перевод тиску з hPa (Гектопаскаль) до мм.рт.ст (міліметрів ртутного стовпа)
        pressure = round(pressure_hPa * 0.75006375541921, 2)

        print(f"Дата: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
              f"Температура: {temp}°C (Відчувається як: {apparent_temp}°C)\nВологість: {humidity}%\n"
              f"Кількість опадів: {precipitation}мм\nХмарність: {cloudcover}%\n"
              f"Тиск: {pressure}мм.рт.ст.\nШвидкість вітру: {windspeed}м/c\nПориви вітру: {windgusts}м/c\n"
              f"Напрям вітру: {winddirection}°\n")

    except Exception as ex:
        print(ex)
        print("Перевірте правильність введених координатів!")

# Погода кожні 3 години в обраний день
def hourly_weather(latitude, longitude, date):
    try:
        r = requests.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&"
            f"hourly=temperature_2m,relativehumidity_2m,apparent_temperature,precipitation,surface_pressure,cloudcover,"
            f"windspeed_10m,windgusts_10m,winddirection_10m&"
            f"windspeed_unit=ms&"
            f"timezone=Europe%2FKiev&"
            f"start_date={date}&"
            f"end_date={date}")
        data = r.json()
        #pprint(data)

        temp = data["hourly"]["temperature_2m"]
        apparent_temp = data["hourly"]["apparent_temperature"]
        humidity = data["hourly"]["relativehumidity_2m"]
        precipitation = data["hourly"]["precipitation"]
        cloudcover = data["hourly"]["cloudcover"]
        pressure_hPa = data["hourly"]["surface_pressure"]
        windspeed = data["hourly"]["windspeed_10m"]
        windgusts = data["hourly"]["windgusts_10m"]
        winddirection = data["hourly"]["winddirection_10m"]

        pressure = list()
        for i in range(len(pressure_hPa)):
            pressure.append(round(pressure_hPa[i]*0.75006375541921, 2))

        print(f"Дата: {date}")
        for hour in range(len(data["hourly"]["time"])):
            if hour%3==0:
                print(f"Час: {data['hourly']['time'][hour].split('T')[1]}\n"
                      f"Температура: {temp[hour]}°C (Відчувається як: {apparent_temp[hour]}°C)\nВологість: {humidity[hour]}%\n"
                      f"Кількість опадів: {precipitation[hour]}мм\nХмарність: {cloudcover[hour]}%\n"
                      f"Тиск: {pressure[hour]}мм.рт.ст.\nШвидкість вітру: {windspeed[hour]}м/c\nПорив вітру: {windgusts[hour]}м/c\n"
                      f"Напрям вітру: {winddirection[hour]}°\n")

    except Exception as ex:
        print(ex)
        print("Перевірте правильність введених данних!")

# Погода на протязі неділі (з пн до вс), в якій присутня введена дата
def week_weather(latitude, longitude, date):
    # Наступний шматок коду визначає дати понеділка та неділі, в межах яких знаходиться вхідна дата
    try:
        format_date = datetime.datetime(int(date.split('-')[0]), int(date.split('-')[1]), int(date.split('-')[2]))
        if int(format_date.day) >= datetime.datetime.weekday(format_date):
            diff = str(int(format_date.day)-datetime.datetime.weekday(format_date))
            monday = f"{format_date.year}-{format_date.month}-{diff}"
        else:
            if format_date.month != 1:
                diff = str(int(format_date.day)-datetime.datetime.weekday(format_date)+monthrange(format_date.year, format_date.month-1)[1])
                monday = f"{format_date.year}-{format_date.month-1}-{diff}"
            else:
                diff = str(int(format_date.day)-datetime.datetime.weekday(format_date)+monthrange(format_date.year-1, 12)[1])
                monday = f"{format_date.year-1}-12-{diff}"
        days_to_sunday = 6 - datetime.datetime.weekday(format_date)
        if int(format_date.day)+days_to_sunday <= monthrange(format_date.year, format_date.month)[1]:
            sunday = f"{format_date.year}-{format_date.month}-{int(format_date.day)+days_to_sunday}"
        else:
            if format_date.month != 12:
                sunday = f"{format_date.year}-{format_date.month+1}-{int(format_date.day)+days_to_sunday-monthrange(format_date.year, format_date.month)[1]}"
            else:
                sunday = f"{format_date.year+1}-01-{int(format_date.day)+days_to_sunday-monthrange(format_date.year, format_date.month)[1]}"

        # Відбувається підгін отриманої дати понеділка під формат YYYY-MM-DD
        temp_list = monday.split('-')
        for i in range(len(temp_list)):
            if len(temp_list[i]) <2:
                temp_list[i] = '0' + temp_list[i]
        monday = '-'.join(temp_list)

        # Відбувається підгін отриманої дати неділі під формат YYYY-MM-DD
        temp_list2 = sunday.split('-')
        for i in range(len(temp_list2)):
            if len(temp_list2[i]) < 2:
                temp_list2[i] = '0' + temp_list2[i]
        sunday = '-'.join(temp_list2)

        rw = requests.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&"
            f"daily=temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,precipitation_sum,precipitation_hours,"
            f"windspeed_10m_max,windgusts_10m_max,winddirection_10m_dominant&"
            f"windspeed_unit=ms&"
            f"timezone=Europe%2FKiev&"
            f"start_date={monday}&"
            f"end_date={sunday}")
        data_week = rw.json()
        #pprint(data_week)

        temp_max = data_week["daily"]["temperature_2m_max"]
        temp_min = data_week["daily"]["temperature_2m_min"]
        apparent_temp_max = data_week["daily"]["apparent_temperature_max"]
        apparent_temp_min = data_week["daily"]["apparent_temperature_min"]
        precipitation_hours = data_week["daily"]["precipitation_hours"]
        precipitation_sum = data_week["daily"]["precipitation_sum"]
        time = data_week["daily"]["time"]
        windspeed = data_week["daily"]["windspeed_10m_max"]
        windgusts = data_week["daily"]["windgusts_10m_max"]
        winddirection = data_week["daily"]["winddirection_10m_dominant"]

        week_days = ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця", "Субота", "Неділя"]

        for day in range(len(time)):
            print(f"{week_days[day]} - {time[day]}\nМакс. температура: {temp_max[day]}°C\nМакс. темп. по відчуттям: {apparent_temp_max[day]}°C\n"
                  f"Мін. температура: {temp_min[day]}°C\nМін. темп. по відчуттям: {apparent_temp_min[day]}°C\n"
                  f"К-сть годин опадів: {precipitation_hours[day]} годин\nК-сть опадів: {precipitation_sum[day]}мм\n"
                  f"Макс. шв. вітру: {windspeed[day]}м/с\nМакс. порив вітру: {windgusts[day]}м/с\nНапрям вітру: {winddirection[day]}°\n")

    except Exception as ex:
        print(ex)
        print("Перевірте правильність введених данних!")

def interval_weather(latitude, longitude, start_date, end_date):
    try:
        r = requests.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&"
            f"daily=temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,precipitation_sum,precipitation_hours,"
            f"windspeed_10m_max,windgusts_10m_max,winddirection_10m_dominant&"
            f"windspeed_unit=ms&"
            f"timezone=Europe%2FKiev&"
            f"start_date={start_date}&"
            f"end_date={end_date}")
        data = r.json()
        #pprint(data_week)

        temp_max = data["daily"]["temperature_2m_max"]
        temp_min = data["daily"]["temperature_2m_min"]
        apparent_temp_max = data["daily"]["apparent_temperature_max"]
        apparent_temp_min = data["daily"]["apparent_temperature_min"]
        precipitation_hours = data["daily"]["precipitation_hours"]
        precipitation_sum = data["daily"]["precipitation_sum"]
        time = data["daily"]["time"]
        windspeed = data["daily"]["windspeed_10m_max"]
        windgusts = data["daily"]["windgusts_10m_max"]
        winddirection = data["daily"]["winddirection_10m_dominant"]

        for day in range(len(time)):
            print(f"Дата: {time[day]}\nМакс. температура: {temp_max[day]}°C\nМакс. темп. по відчуттям: {apparent_temp_max[day]}°C\n"
                  f"Мін. температура: {temp_min[day]}°C\nМін. темп. по відчуттям: {apparent_temp_min[day]}°C\n"
                  f"К-сть годин опадів: {precipitation_hours[day]} годин\nК-сть опадів: {precipitation_sum[day]}мм\n"
                  f"Макс. шв. вітру: {windspeed[day]}м/с\nМакс. порив вітру: {windgusts[day]}м/с\nНапрям вітру: {winddirection[day]}°\n")

        dictionary = {'Дата': time,
                      'Макс. темп., °C': temp_max,
                      'Макс. темп. по відчуттям, °C': apparent_temp_max,
                      'Мін. темп., °C': temp_min,
                      'Мін. темп. по відчуттям, °C': apparent_temp_min,
                      'К-сть годин опадів, h': precipitation_hours,
                      'К-сть опадів, мм': precipitation_sum,
                      'Макс. шв. вітру, м/с': windspeed,
                      'Макс. порив вітру, м/с': windgusts,
                      'Напрям вітру, °': winddirection}
        return dictionary

    except Exception as ex:
        print(ex)
        print("Перевірте правильність введених данних!")

def historical_interval_weather(latitude, longitude, start_date, end_date):
    try:
        r = requests.get(
            f"https://archive-api.open-meteo.com/v1/era5?latitude={latitude}&longitude={longitude}&"
            f"start_date={start_date}&"
            f"end_date={end_date}&"
            f"daily=temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,precipitation_sum,precipitation_hours,"
            f"windspeed_10m_max,windgusts_10m_max,winddirection_10m_dominant&"
            f"timezone=Europe%2FKiev&"
            f"windspeed_unit=ms"
        )
        data = r.json()
        #pprint(data_week)

        temp_max = data["daily"]["temperature_2m_max"]
        temp_min = data["daily"]["temperature_2m_min"]
        apparent_temp_max = data["daily"]["apparent_temperature_max"]
        apparent_temp_min = data["daily"]["apparent_temperature_min"]
        precipitation_hours = data["daily"]["precipitation_hours"]
        precipitation_sum = data["daily"]["precipitation_sum"]
        time = data["daily"]["time"]
        windspeed = data["daily"]["windspeed_10m_max"]
        windgusts = data["daily"]["windgusts_10m_max"]
        winddirection = data["daily"]["winddirection_10m_dominant"]

        for day in range(len(time)):
            print(f"Дата: {time[day]}\nМакс. температура: {temp_max[day]}°C\nМакс. темп. по відчуттям: {apparent_temp_max[day]}°C\n"
                  f"Мін. температура: {temp_min[day]}°C\nМін. темп. по відчуттям: {apparent_temp_min[day]}°C\n"
                  f"К-сть годин опадів: {precipitation_hours[day]} годин\nК-сть опадів: {precipitation_sum[day]}мм\n"
                  f"Макс. шв. вітру: {windspeed[day]}м/с\nМакс. порив вітру: {windgusts[day]}м/с\nНапрям вітру: {winddirection[day]}°\n")

        dictionary = {'Дата': time,
                      'Макс. темп., °C': temp_max,
                      'Макс. темп. по відчуттям, °C': apparent_temp_max,
                      'Мін. темп., °C': temp_min,
                      'Мін. темп. по відчуттям, °C': apparent_temp_min,
                      'К-сть годин опадів, h': precipitation_hours,
                      'К-сть опадів, мм': precipitation_sum,
                      'Макс. шв. вітру, м/с': windspeed,
                      'Макс. порив вітру, м/с': windgusts,
                      'Напрям вітру, °': winddirection}
        return dictionary

    except Exception as ex:
        print(ex)
        print("Перевірте правильність введених данних!")

warnings.simplefilter(action='ignore', category=FutureWarning)

def export(dictionary, file_name, sheet_name):
    df = pd.DataFrame(dictionary)
    writer = pd.ExcelWriter(file_name)
    df.to_excel(writer, sheet_name=sheet_name, index=False)

    # Відбувається вирівнювання ширини колонок під найдовшу назву в них
    for column in df:
        column_width = max(df[column].astype(str).map(len).max(), len(column))
        col_idx = df.columns.get_loc(column)
        writer.sheets[sheet_name].set_column(col_idx, col_idx, column_width)
    writer.save()

def hourly_interval_weather(latitude, longitude, start_date, end_date):
    try:
        r = requests.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&"
            f"hourly=temperature_2m,relativehumidity_2m,apparent_temperature,precipitation,surface_pressure,cloudcover,"
            f"windspeed_10m,windgusts_10m,winddirection_10m&"
            f"windspeed_unit=ms&"
            f"timezone=Europe%2FKiev&"
            f"start_date={start_date}&"
            f"end_date={end_date}")
        data = r.json()
        #pprint(data)

        temp = data["hourly"]["temperature_2m"]
        apparent_temp = data["hourly"]["apparent_temperature"]
        humidity = data["hourly"]["relativehumidity_2m"]
        precipitation = data["hourly"]["precipitation"]
        cloudcover = data["hourly"]["cloudcover"]
        pressure_hPa = data["hourly"]["surface_pressure"]
        windspeed = data["hourly"]["windspeed_10m"]
        windgusts = data["hourly"]["windgusts_10m"]
        winddirection = data["hourly"]["winddirection_10m"]

        pressure = list()
        for i in range(len(pressure_hPa)):
            pressure.append(round(pressure_hPa[i]*0.75006375541921, 2))

        for hour in range(len(data["hourly"]["time"])):
            if hour%3==0:
                print(f"Час: {data['hourly']['time'][hour].split('T')[0]} - {data['hourly']['time'][hour].split('T')[1]}\n"
                      f"Температура: {temp[hour]}°C (Відчувається як: {apparent_temp[hour]}°C)\nВологість: {humidity[hour]}%\n"
                      f"Кількість опадів: {precipitation[hour]}мм\nХмарність: {cloudcover[hour]}%\n"
                      f"Тиск: {pressure[hour]}мм.рт.ст.\nШвидкість вітру: {windspeed[hour]}м/c\nПорив вітру: {windgusts[hour]}м/c\n"
                      f"Напрям вітру: {winddirection[hour]}°\n")

        dict_time = list()
        for date in range(len(data['hourly']['time'])):
            dict_time.append(data['hourly']['time'][date].split('T')[0]+' - '+data['hourly']['time'][date].split('T')[1])

        dictionary = {'Час': dict_time,
                      'Температура, °C': temp,
                      'Темп. по відчуттям, °C': apparent_temp,
                      'Вологість, %': humidity,
                      'Кількість опадів, мм': precipitation,
                      'Хмарність, %': cloudcover,
                      'Тиск, мм.рт.ст.': pressure,
                      'Шв. вітру, м/с': windspeed,
                      'Порив вітру, м/с': windgusts,
                      'Напрям вітру, °': winddirection}
        return dictionary

    except Exception as ex:
        print(ex)
        print("Перевірте правильність введених данних!")

def hourly_historical_interval_weather(latitude, longitude, start_date, end_date):
    try:
        r = requests.get(
            f"https://archive-api.open-meteo.com/v1/era5?latitude={latitude}&longitude={longitude}&"
            f"start_date={start_date}&"
            f"end_date={end_date}&"
            f"hourly=temperature_2m,relativehumidity_2m,apparent_temperature,surface_pressure,precipitation,cloudcover,"
            f"windspeed_10m,winddirection_10m,windgusts_10m&"
            f"timezone=Europe%2FKiev&"
            f"windspeed_unit=ms")
        data = r.json()
        #pprint(data)

        temp = data["hourly"]["temperature_2m"]
        apparent_temp = data["hourly"]["apparent_temperature"]
        humidity = data["hourly"]["relativehumidity_2m"]
        precipitation = data["hourly"]["precipitation"]
        cloudcover = data["hourly"]["cloudcover"]
        pressure_hPa = data["hourly"]["surface_pressure"]
        windspeed = data["hourly"]["windspeed_10m"]
        windgusts = data["hourly"]["windgusts_10m"]
        winddirection = data["hourly"]["winddirection_10m"]

        pressure = list()
        for i in range(len(pressure_hPa)):
            pressure.append(round(pressure_hPa[i]*0.75006375541921, 2))

        for hour in range(len(data["hourly"]["time"])):
            if hour%3==0:
                print(f"Час: {data['hourly']['time'][hour].split('T')[0]} - {data['hourly']['time'][hour].split('T')[1]}\n"
                      f"Температура: {temp[hour]}°C (Відчувається як: {apparent_temp[hour]}°C)\nВологість: {humidity[hour]}%\n"
                      f"Кількість опадів: {precipitation[hour]}мм\nХмарність: {cloudcover[hour]}%\n"
                      f"Тиск: {pressure[hour]}мм.рт.ст.\nШвидкість вітру: {windspeed[hour]}м/c\nПорив вітру: {windgusts[hour]}м/c\n"
                      f"Напрям вітру: {winddirection[hour]}°\n")

        dict_time = list()
        for date in range(len(data['hourly']['time'])):
            dict_time.append(data['hourly']['time'][date].split('T')[0]+' - '+data['hourly']['time'][date].split('T')[1])

        dictionary = {'Час': dict_time,
                      'Температура, °C': temp,
                      'Темп. по відчуттям, °C': apparent_temp,
                      'Вологість, %': humidity,
                      'Кількість опадів, мм': precipitation,
                      'Хмарність, %': cloudcover,
                      'Тиск, мм.рт.ст.': pressure,
                      'Шв. вітру, м/с': windspeed,
                      'Порив вітру, м/с': windgusts,
                      'Напрям вітру, °': winddirection}
        return dictionary

    except Exception as ex:
        print(ex)
        print("Перевірте правильність введених данних!")

def main():
    latitude = 49.23
    longitude = 31.88
    date = '2022-12-28'
    #current_weather(latitude, longitude)
    #hourly_weather(latitude, longitude, date)
    #week_weather(latitude, longitude, date)

    start_date = '2022-12-31'
    end_date = '2023-01-07'
    #interval_weather(latitude, longitude, start_date, end_date)
    #export(interval_weather(latitude, longitude, start_date, end_date), 'weather_forecast.xlsx', 'forecast')
    #hourly_interval_weather(latitude, longitude, start_date, end_date)
    #export(hourly_interval_weather(latitude, longitude, start_date, end_date), 'weather_forecast.xlsx', 'forecast')

    start_date = '2016-11-28'
    end_date = '2022-11-28'
    #historical_interval_weather(latitude, longitude, start_date, end_date)
    #export(historical_interval_weather(latitude, longitude, start_date, end_date), 'weather_forecast.xlsx', 'forecast')
    #hourly_historical_interval_weather(latitude, longitude, start_date, end_date)
    #export(hourly_historical_interval_weather(latitude, longitude, start_date, end_date), 'weather_forecast.xlsx', 'forecast')

if __name__ == '__main__':
    main()