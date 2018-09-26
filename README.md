# Python Flask WebTemplate
This Project is using the Bootstrap admin theme [SB Admin 2](https://startbootstrap.com/template-overviews/sb-admin-2/) 
from [Start Bootstrap](https://startbootstrap.com).

### API Schemas
| Method | URL | Headers | Data | Description |
|:---:|:---:|:---:|:---:|:---:|
| GET | /api/auth | Access-Token | / | Get information about your Account |
| POST | /api/auth |  | username, password | Sign in |
| DELETE | /api/auth | Access-Token | / | Sign out |
||||||
| GET | /api/roles | Access-Token | / | Get all roles |
| GET | /api/roles/{name:string} | Access-Token | / | Get a role |
| POST | /api/roles | Access-Token | name, description | Admin: Create a role |
| PUT | /api/roles/{name:string} | Access-Token | description | Admin: Modify a role |
| DELETE | /api/roles/{name:string} | Access-Token | / | Admin: Delete a role |
||||||
| GET | /api/users | Access-Token | / | Admin: Get all accounts |
| GET | /api/users/{public_id:string} | Access-Token | / | Admin: Get an account |
| POST | /api/users | Access-Token | username, email, password, role | Admin: Create a new account |
| PUT | /api/users/{public_id:string} | Access-Token | username (and/or) email (and/or) password | Admin: Update account |
| PUT | /api/users/me | Access-Token | username (and/or) email (and/or) password | Update your account |
| DELETE | /api/users/{public_id:string} | Access-Token | / | Admin: Delete an account |
| DELETE | /api/users/me | Access-Token | / | delete your account |

### Database Schema
| Table | Attribute | Datatype (Length) (+ Description) | Settings |
|:---------:|:-------------:|:---------------------------------:|:---------------------------:|
| users | id | Integer(11) | primary key, auto increment |
|  | publicId | Varchar(36) (for uuid4) | unique |
|  | username | Varchar(80) | unique |
|  | displayName | Varchar(80) | |
|  | email | Varchar(100) | unique |
|  | password | Blob(512) (sha512 Hash) |  |
|  | lastLogin | TimeStamp |  |
|  | created | TimeStamp |  |
|  | role | Integer(11) | foreign key -> role.id |
| roles | id | Integer(11) | primary key, auto increment |
|  | name | Varchar(80) |  |
|  | description | Varchar(100) |  |
| tokens | id | Integer(11) | primary key, auto increment |
|  | user | Integer(11) | foreign key -> user.id |
|  | token | Varchar(128) | unique |
|  | created | TimeStamp |  |
|  | expires | TimeStamp |  |
|  | broken | Integer(1) (boolean) |  |


### Installation via Docker
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
