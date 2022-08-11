##- Переменные окружения берутся с помощью "dotenv" из .env 


##- Запуск базы на докере:  $ docker-compose up

#**Задание**:

## Домашнее задание к лекции «Asyncio»

В этом задании мы будем выгружать из API персонажей Start Wars и загружать в базу данных.<br>
Документация по API находится здесь: [SWAPI](https://swapi.dev/documentation#people). <br>

Необходимо выгрузить cледующие поля:<br>
**id** - ID персонажа <br>
**birth_year** <br>
**eye_color** <br>
**films** - строка с названиями фильмов через запятую <br>
**gender** <br>
**hair_color** <br>
**height** <br>
**homeworld** <br>
**mass** <br>
**name** <br>
**skin_color** <br>
**species** - строка с названиями типов через запятую <br>
**starships** - строка с названиями кораблей через запятую <br>
**vehicles** - строка с названиями транспорта через запятую <br>
Данные по каждому персонажу необходимо загрузить в любую базу данных. <br>
Выгрузка из апи и загрузка в базу должна происходить аснхронно. <br>
Результатом работы будет: <br>
1) скрипт миграции базы данных <br>
2) скрипт загрузки данных из API в базу <br>

В базу должны быть загружены все персонажи