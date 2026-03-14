# Микелянджело дай пивчик | Mikelanjelo give me beer

[Русская версия](#russian-version) | [English version](#english-version)

<a id="russian-version"></a>
## Русская версия

Идея проекта - попытаться повторить бот для знакомств "Леонардо дай винчик". Реализован весь основной функционал:
- Создание анкеты (прикрепление медиафайлов работает)
- Листание подходящих по возрасту и полу анкет (человек сам указывает, какой пол его интересует, максимальная разница в возрасте с показываемыми анкетами 2 года)
- Редактирование анкеты
- Лайки на анкеты
- Просмотр входящих лайков, при взаимном лайке выдаётся ссылка на профиль человека, который тебя лайкнул
- Реализована настройка местоположения (города и опционально координаты). При поиске анкеты проверяется либо жительство в одном городе, либо расстояние между пользователями меньше 5км

## Инструкция по локальному запуску


1) В корневой директории проекта создать файл .env и там установить настройки подключения к БД, а также токен вашего телеграмм бота, пример:
```
TOKEN=<your_token>
POSTGRES_USER=wisetree
POSTGRES_PASSWORD=123456789
POSTGRES_DB=mydb
DATABASE_URL=postgresql+asyncpg://wisetree:123456789@db:5432/mydb
```
2) Поднять докер (на Windows просто запустите Docker Desktop, на Linux выполните команду `sudo systemctl start docker`)
3) Выполните команду `sudo docker compose up`
4) Когда Docker поднимется, откройте второй терминал и выполните
```commandline
sudo docker compose run --rm app alembic revision --autogenerate -m "New migration"
```
а потом
```commandline
sudo docker compose run --rm app alembic upgrade head
```
(создание таблиц в БД)

5) Готово, бот должен работать!


## Генерация документации
1) Перейдите в папку docs (```cd docs```)
2) выполните команду 
```commandline
make html
```
(если не сработало, то ```.\make html```)

3) Теперь, когда документация сгенерирована, откройте в браузере файл, который располагается по адресу docs/build/html/index.html

---
<a id="english-version"></a>
## English Version

The idea of the project is to try to replicate the dating bot "Leonardo give me wine". All the main functionality has been implemented:
- Creating a profile (attaching media files works)
- Browsing suitable profiles based on age and gender (the user specifies the gender they are interested in, with a maximum age difference of 2 years with the displayed profiles)
- Editing the profile
- Liking profiles
- Viewing incoming likes, when a mutual like occurs, a link to the profile of the person who liked you is provided
- Location settings have been implemented (cities and optionally coordinates). When searching for a profile, it checks either residence in the same city or the distance between users is less than 5 km

## Instructions for local launch


1) In the root directory of the project, create a `.env` file and set the database connection settings as well as your Telegram bot token, example:
```
TOKEN=<your_token>
POSTGRES_USER=wisetree
POSTGRES_PASSWORD=123456789
POSTGRES_DB=mydb
DATABASE_URL=postgresql+asyncpg://wisetree:123456789@db:5432/mydb
```
2) Start Docker (on Windows just run Docker Desktop, on Linux run the command `sudo systemctl start docker`)
3) When Docker is up, open a second terminal and run:
```commandline
sudo docker compose run --rm app alembic revision --autogenerate -m "New migration"
```
then run:
```commandline
sudo docker compose run --rm app alembic upgrade head
```
(creating tables in the database)

4) Done, the bot should work!



## Generating Documentation
1) Navigate to the docs folder (```cd docs```)
2) Run the command:
```commandline
make html
```
(if it doesn't work, then ```.\make html```)

3) Now, when the documentation is generated, open the file located at docs/build/html/index.html in your browser.