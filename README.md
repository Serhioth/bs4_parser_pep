**Парсер информации о языке программирования Python**

Описание:
Многофункциональный парсер для получения информации о языке программирования **Python**!

Функции:
    1. Получение списка ссылок с информацией об изменениях в новых версиях языка
    2. Предоставление списка ссылок на документацию для всех версий
    3. Скачивание pdf-файла с документацией для самой свежей версии
    4. Предоставление информации обо всех PEP и их статусах

Парсер поддерживает несколько режимов работы, в зависимости от аргументов переданных при запуске в командной строке:
    1. whats-new - режим, при котором парсер возвращает список версий Python со ссылкой на список изменений для каждой из них
    2. latest-versions - режим, при котором парсер возвращает список всех версий Python с их текущими статусами поддержки разработчиками
    3. download - скачивает архив с документацией к последней версии Python
    4. pep - возвращает актуальный список PEP, а так же их текущий статус

Так же поддерживаются следующие именованные аргументы:
    -h, --help - показывает сообщение с информацией о возможных режимах работы
    -c, --clear-cache - очищает кэш текущей сессии
    -o {pretty, file}, --output {pretty, file} - формат вывода результата, pretty - формат вывода в таблице PrettyTable, file - вывод в формате csv-файла, функция download не поддерживает данные форматы вывода


