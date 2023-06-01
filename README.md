Проект реализует API согласно заданию.


Для запуска приложения необходимо выполнить:
```commandline
docker network create alsinet
docker-compose -f ./docker-compose.yml build
docker-compose -f ./docker-compose.yml up -d
```
Приложение запускается на 8000/tcp.
Реализованы методы для груза:
* GET 127.0.0.1:8000/cargos/all - возвращает все грузы;
* GET 127.0.0.1:8000/cargos/id - возвращает всю информацию о грузе;
* GET 127.0.0.1:8000/cargos/filter?weight=100&distance=1300 - возвращает информацию о грузе с фильтрами;
* POST 127.0.0.1:8000/cargos/ с передачей параметров zip_delivery, zip_pickup, weight, description - создает новый груз;
* PUT 127.0.0.1:8000/cargos/id с передачей параметров weight, description - изменяет иформацию о грузе;
* DELETE 127.0.0.1:8000/cargos/id - удаляет груз.

Реализованы методы для грузовика:
* GET 127.0.0.1:8000/trucks/id возвращает информацию о грузовике
* PUT 127.0.0.1:8000/trucks/id с передачей параметра location_zip - изменяет информацию о грузовике
