---create

> docker build -t docker-django .

//correr docker
> docker run -p 8000:8000 docker-django

eliminar un docker
> docker rm -f <container-name>


-- antes de correr el sistema
asegurarse de caargar la data.

-- guardar backup
> python manage.py dumpdata -o main.json 

-- ingresar backup
> python manage.py loaddata main.json
