# Database Schema
| Table | Attribute | Datatype (Length) (+ Description) | Settings |
|:---------:|:-------------:|:---------------------------------:|:---------------------------:|
| users | id | Integer | primary key, auto increment |
|  | publicId | Varchar(36) (for uuid4) | unique |
|  | username | Varchar(100) | unique |
|  | displayName | Varchar(100) | |
|  | email | Varchar(100) | unique |
|  | password | Varchar(255) (sha512 Hash) |  |
|  | lastLogin | DateTime |  |
|  | created | DateTime |  |
|  | role | Integer | foreign key -> role.id |
| roles | id | Integer | primary key, auto increment |
|  | name | Varchar(80) |  |
|  | description | Varchar(80) |  |
| tokens | id | Integer | primary key, auto increment |
|  | user | Integer | foreign key -> user.id |
|  | token | Varchar(80) | unique |
|  | created | DateTime |  |
|  | expires | DateTime |  |
|  | broken | Integer(1) (boolean) |  |