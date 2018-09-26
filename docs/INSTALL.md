# Installation via Docker
* Install [Docker](https://docs.docker.com/install/) and [docker-compose](https://docs.docker.com/compose/install/)
* Build Docker Image

```
git clone https://github.com/felbinger/webtemplate_flask.git
docker build -t web-template .
```

* Define your container in the file `docker-compose.yml`:

```yml
version: '3'
services:
  db:
    image: mysql:5.7
    container_name: root_db_1
    restart: always
    ports:
      - "9999:3306"
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: hc
    volumes:
      - "/srv/mysql:/var/lib/mysql"
  web-template:
    image: web-template
    container_name: root_web-template_1
    restart: always
    ports:
      - "8080:80"
    environment:
      MYSQL_PASSWORD: root
```

* Add database hc (in this example automatically)
* Change database collection from `latin1_swedish_ci` to `utf8mb4_unicode_ci`
* Execute following sql:
```sql
INSERT INTO `role` (`id`, `name`, `description`) VALUES
(1, 'admin', 'Admin'),
(2, 'user', 'User');
```

* Use docker-compose:
```bash
# Start all containers
docker-compose up -d
# Stop all containers
docker-compose stop
# Stop and remove all containers
docker-compose down  
# Start a specific container
docker-compose up -d <container>
# Stop a specific container
docker-compose stop <container>
# Stop and remove a specific container
docker-compose rm -fs <container>  
# Show logs
docker-compose logs [container]  
# Show status
docker-compose ps [container]
```
