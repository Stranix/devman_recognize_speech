# Распознаем сообщения

Это бот для Телеграма и ВК, который умеет отвечать на типичные вопросы с использованием [DialogFlow](https://cloud.google.com/dialogflow/docs)

<img src="https://github.com/Stranix/devman_recognize_speech/blob/master/promo/tg.gif?raw=true" width="250"> <img src="https://github.com/Stranix/devman_recognize_speech/blob/master/promo/vk.gif?raw=true" width="250">


## Требования
`Python => 3.10 `  
Необходимо зарегистрировать бота и получить токен для доступа к API Телеграма. Подробная инструкция [как зарегистрировать бота](https://way23.ru/%D1%80%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D1%8F-%D0%B1%D0%BE%D1%82%D0%B0-%D0%B2-telegram/)  
Также необходимо узнать ID чата, в который бот будет слать логи. Сделать это можно с помощью бота [Userinfobot](https://telegram.me/userinfobot). Отправьте боту любое сообщение, он в ответ пришлет ID.  
В группе ВК, в меню справа находим пункт **Управление**, затем **Работа с API**, и создаем ключ доступа. Ключ понадобится чуть позже.
Далее идем **Сообщения ⟶ Настройки для бота** и включаем "Возможности ботов".

Для работы с Dialogflow понадобится:

- Создайте проект в Google Cloud и сохранить его `id`. Подробнее [здесь](https://cloud.google.com/dialogflow/es/docs/quick/setup#project).
- Создайте "агента", который будет отвечать на вопросы. При создании агента понадобится ввести `id` проекта из предыдущего пункта. Укажите язык агента "русский", иначе он вас не поймет. Подробнее [здесь](https://cloud.google.com/dialogflow/es/docs/quick/build-agent).
- Зарегистрируйте сервисный аккаунт для проекта и скачайте JSON-ключ. Подробнее [здесь](https://cloud.google.com/docs/authentication/getting-started).

## Подготовка перед запуском

* Скачайте код с GitHub. 
```sh
git clone https://github.com/Stranix/devman_recognize_speech.git
```
* Установите зависимости:

```sh
pip install -r requirements.txt
```

## Переменные окружения

Настройки берутся из переменных окружения.

Доступные переменные:

- `TG_BOT_TOKEN` — токен бота, который отправлять уведомления.
- `TG_ADMIN_ID` — id чата, куда будут отправляться логи.
- `DIALOGFLOW_PROJECT_ID` — id проекта в Google Cloud, указанный при создании агента.
- `GOOGLE_APPLICATION_CREDENTIALS` — путь до файла с ключами для подключения к Google API.
- `VK_GROUP_API_KEY` — ключ доступа к группе VK.

## Обучаем бота

Чтобы бот умел отвечать на вопросы по разным темам, его надо обучить.  
Создайте json-файл с вопросами и ответами по следующей схеме:

```json
{
    "Тема": {
        "questions": [
            "Вопрос 1",
            "Вопрос 2"
        ],
        "answer": "Ответ"
    },
    ...
}
```

Пример:

```json
{
    "Устройство на работу": {
        "questions": [
            "Как устроиться к вам на работу?",
            "Как работать у вас?",
            "Хочу работать у вас"
        ],
        "answer": "Если вы хотите устроиться к нам, напишите на почту."
    },
    "Забыл пароль": {
        "questions": [
            "Не помню пароль",
            "Не могу войти",
            "Проблемы со входом"
        ],
        "answer": "Если вы не можете войти на сайт, воспользуйтесь кнопкой «Забыли пароль?»"
    }
}
```

Запустите скрипт, чтобы обучить агента:

```sh
python dialogflow.py --json /path/to/questions.json 
```
По умолчанию ищется файл `questions.json` в корне проекта.  
В случае успешного выполнения скрипт ничего не выводит.

## Запуск

Запустите бота для ВК:

```sh
python vk_bot.py
```

Для Телеграма:

```sh
python tg_bot.py
```

В случае успешного старта скрипт ничего не выводит и запускает бесконечный цикл.


## Цели проекта

Код написан в учебных целях — для курса по Python на сайте [Devman](https://dvmn.org/)