# yamdb_final
yamdb_final

[![yamdb workflow](https://github.com/RakitDautov/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)](https://github.com/RakitDautov/yamdb_final/actions/workflows/yamdb_workflow.yml)

Необходимые инструменты для запуска

    docker
    docker-compose

Запуск приложения

    sudo docker pull rocke215/yamdb_final
    sudo docker-compose up -d --build
    
    sudo docker-compose exec -T web python manage.py makemigrations users
    sudo docker-compose exec -T web python manage.py makemigrations api
    sudo docker-compose exec -T web python manage.py migrate --no-input
    sudo docker-compose exec -T web python manage.py collectstatic --no-input

Описание проекта
    
    Проект yamdb_final собирает пользовательские отзывы на произведения (кино, музыка,
    книги)

Адрес сайта
    
    http://178.154.214.98/api/v1/

Автор проекта
    
    Даутов Ракит, студент Яндекс.Практикум, курс backedn разработка