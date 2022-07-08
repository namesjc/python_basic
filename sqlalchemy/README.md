# Database

## Types of relationship in a database

There are 3 main types of relationship in a database:

- one-to-one
- one-to-many
- many-to-many

However, you may also encounter references to a many-to-one relationship which , in fact, is a special case of a one-to-many relationship and self-referencing relationship which occurs when only one table is involved.

## One-to-many relationship

A one-to-many relationship occurs when one record in table 1 is related to one or more record in table 2. However, one record in table 2 cannot be related to more than one record in table1. 

How to join tables with on-to-many relationship in SQL? **INNER JOINs** are considered to be the most effective way to combine data from two tables that have on-to-many relationship. 

```sql
SELECT
*
FEOM country AS c
INNER JOIN city as c1
ON c.country_id = c1.counrty_id
```

![image-20220615150034585](https://github.com/namesjc/python_basic/blob/main/screenshot/image-20220615150034585.png)

### Example of one-to-many relation in SQL Server

```sql
CREATE TABLE `city` (
  `city_id` integer PRIMARY KEY,
  `city` varchar(50) NOT NULL,
  `country_id` integer NOT NULL,
);

CREATE TABLE `country` (
  `country_id` integer PRIMARY KEY,
  `country` varchar(50) NOT NULL,
);

CREATE INDEX `city_index_0` ON `users` (`city`);

CREATE INDEX `country_index_1` ON `users` (`country`);

ALTER TABLE `city` ADD FOREIGN KEY (`country_id`) REFERENCES `country` (`id`);
```

## Many-to-many relationship

A many-to-many relationship occurs when multiple records in one table are related to multiple records in another table. For example, products and suppliers: one supplier may deliver one or many products and at the same time, the company may order one product from one or many suppliers.

### Example of creating many-to-many relation in SQL

Relational databases don't support direct many-to-many relationships between two tables. Then. how to implement many-to-many relationships in SQL? To create a many-to-many relationship in a database, you',, need to create a third table to connect the other two. This new table(also known as a *linking*, *joining*, *bridging*, or *junction* table) will contain the primary key columns of two tables you want to relate and wull seve as an intermediate table between them.

Example: *films* and *category*

```sql
CREATE TABLE films (
	film_id INTEGER PRIMARY KEY, 
	title VARCHAR(50) NOT NULL, 
	director VARCHAR(50)
    year_released DATETIME
)

CREATE TABLE category (
	category_id INTEGER PRIMARY KEY, 
	name VARCHAR(50)
)
```

 Next, we create a junction table *file_category* that will map these two tables together by referencing the primary keys of both tables.

```sql
CREATE TABLE file_category (
	film_id INTEGER, 
	category_id INTEGER, 
	FOREIGN KEY(film_id) REFERENCES film (id), 
	FOREIGN KEY(category_id) REFERENCES category (id)
)
```

![image-20220615153119420](https://github.com/namesjc/python_basic/blob/main/screenshot/image-20220615153119420.png)

## Self-referencing relationship

A self-referencing relationship (also known as a recursive relationship) in a database occurs when a column in a table relates to another column in the same table. In such a relationship, only one table is involved. For example, the *Staff* table contains information about company employees and their managers, however, managers themselves belong to staff too.

A self-referencing relationship example in SQL:

![image-20220615154027738](https://github.com/namesjc/python_basic/blob/main/screenshot/image-20220615154027738.png)

### How to create a self-referencing relationship in SQL

To establish a self-referencing relationship on a table, we create a table, define a primary key, and then add a foreign key referencing that primary key.

```sql
CREATE TABLE Staff (
  staff_id int IDENTITY,
  first_name varchar(50) NOT NULL,
  last_name varchar(50) NOT NULL,
  email varchar(255) NOT NULL,
  phone varchar(25) NULL,
  active tinyint NOT NULL,
  store_id int NOT NULL,
  manager_id int NULL,
  PRIMARY KEY CLUSTERED (staff_id),
  UNIQUE (Email)
)
ON [PRIMARY]
GO


ALTER TABLE Sales.Staff
  ADD FOREIGN KEY (manager_id) REFERENCES Staff (staff_id)
GO
```

## Microblog example

### Many-to-many

As an example, consider a database that has `students` and `teachers`. I can say that a student has *many* teachers, and a teacher has *many* students. It's like two overlapped one-to-many relationships from both ends.

The representation of a many-to-many relationship requires the use of an auxiliary table called an *association table* Here is how the database would look for the students and teacher example:

![image-20220614102525927](https://github.com/namesjc/python_basic/blob/main/screenshot/image-20220614102525927.png)

### Many-to-One and One-to-One

A many-to-one is similar to one-to-many relationship. The difference is that this relationship is looked at from the "many" side.

A one-to-one relationship is a special case of a one-to-many. The representation is similar, but a constraint is added to the database to prevent the "many" side to have more than one link. While there are cases in which this type of relationship is useful, it isn't as common as the other types.

### One-to-many with flask-sqlalchemy code

For one-to-many relationship, ad `sqla_orm.relationship` field is normally defined on the "one" side, and it used as a convenient way to get access to the "many." The `back_populates` argument defines the name of a field that will be added to the objects of the "many" class that points back at the "one" object. This will add a `post.author` expression that will return the user given a post. The `lazy` argument defines how the database query for the relationship will be issued.

```python
class User(Updateable, db.Model):
    __tablename__ = 'users'

    id = sqla.Column(sqla.Integer, primary_key=True)
    username = sqla.Column(sqla.String(64), index=True, unique=True, nullable=False)
    email = sqla.Column(sqla.String(120), index=True, unique=True, nullable=False)
    password_hash = sqla.Column(sqla.String(128))
    posts = sqla_orm.relationship('Post', back_populates='author', lazy='noload')
    
class Post(Updateable, db.Model):
    __tablename__ = 'posts'

    id = sqla.Column(sqla.Integer, primary_key=True)
    text = sqla.Column(sqla.String(280), nullable=False)
    timestamp = sqla.Column(sqla.DateTime, index=True, default=datetime.utcnow, nullable=False)
    user_id = sqla.Column(sqla.Integer, sqla.ForeignKey(User.id), index=True)

    author = sqla_orm.relationship('User', back_populates='posts')
```

### Many-to-many with flask-sqlalchemy code

Here is the diagram of the self-referential many-to-many relationship that keeps track of followers:

![image-20220614103838950](https://github.com/namesjc/python_basic/blob/main/screenshot/image-20220614103838950.png)

The `followers` table is the association table of the relationship. The foreign keys in this table are both pointing at entries in the user table, since it is linking users to users. Each record in this table represents one link between a follower user and a followed user. Like the students and teachers example, a setup like this one allows the database to answer all the questions about followed and followers users that we ever need.

Since this is an auxiliary table that  has no data other than the foreign keys, we created it without an associated model class.

```python
followers = sqla.Table(
    'followers',
    db.Model.metadata,
    sqla.Column('follower_id', sqla.Integer, sqla.ForeignKey('users.id')), # 左侧
    sqla.Column('followed_id', sqla.Integer, sqla.ForeignKey('users.id'))  # 右侧， 被关注的user
)
```

The setup of the relationship is no-trivial.  As a convention let's say that for a pair of users linked by this relationship, the left side user is following the right side user. We defining the relationship as seen from the left side user with the name `followed`, because when we query this relationship from the left side we will get the list of followed user.

```python

class User(Updateable, db.Model):
    __tablename__ = 'users'
    # ...
    following = sqla_orm.relationship(
        'User', secondary=followers, # 指定多对多关联表
        primaryjoin=(followers.c.follower_id == id), # left side, find users who I followed
        secondaryjoin=(followers.c.followed_id == id), # right side, find the users who followed me
        back_populates='followers', lazy='noload')
    followers = sqla_orm.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.followed_id == id),
        secondaryjoin=(followers.c.follower_id == id),
        back_populates='following', lazy='noload')
```

## Diagram tool

[WWW SQL Designer](http://ondras.zarovi.cz/sql/demo)

[dbdiagram](https://dbdiagram.io)