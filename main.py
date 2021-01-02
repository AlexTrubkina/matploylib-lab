key = "48fe513588b0d6b78ac39e51a4189b50"

def getweather(api_key=None):
    import json
    import requests
    city, lat, lon = "Saint Petersburg, RU", 59.57, 30.19

    dt = 1607299200  # datetime of 07/12/2020 in unix-like format
    # Для определения unixtime диапазона для получения температур, 
    # можно использовать сервис https://unixtime-converter.com/

    if api_key:
        result = dict()
        req = requests.get(
            f'http://api.openweathermap.org/data/2.5/'
            f'onecall/timemachine?lat={lat}&lon={lon}&dt={dt}&'
            f'appid={api_key}&lang=ru&units=metric')
        
        # для других параметров см. https://openweathermap.org/api/one-call-api#history

        req_obj = json.loads(req.text)  # Преобразуем объект типа Request в json-формат

        # Сохраним результаты температур в формате json, чтобы ниже их визуализировать
        result['city'] = city
        measures = [{"dt": str(measure['dt']), "temp": str(measure['temp'])} for measure in req_obj["hourly"]]
        

        result['temps'] = measures
        return json.dumps(result)


weather_data_json = getweather(key)

def visualise_data(json_data=''):

    if json_data:
        import matplotlib.pyplot as pplt
        import pandas
        # Мы можем загрузить данные в пригодный для дальнейшей обработки формат
        # с помощью метода read_json из pandas.
        data = pandas.read_json(json_data)
        # print(data)
        city_name = data['city']

        # получим отдельные столбцы с датами 
        dates = [_d['dt'] for _d in data['temps'][:]]
        # и тепературами
        temps = [_t['temp'] for _t in data['temps'][:]]

        # построим их на диаграмме рассеяния
        pplt.scatter(dates, temps)


        pplt.show()

        # построенный график необходимо оптимизировать:
        #  - добавить название 
        #  - правильно расположить ось абсцисс
        #  - упростить вывод дат (на этом графике они выводятся в формате unixtime)
        #  - вывести более строгие значения для подписей осей абсцисс и ординат 
        #  (xticks, yticks)
        # - добавить на график температуры остальных дат 
        # - добавить второй график со средними значениями

visualise_data(weather_data_json)
