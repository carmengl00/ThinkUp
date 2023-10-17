# ThinkUp

## Getting Started

To get a working local copy on Windows, follow these steps.

### Prerequisites

Before working with the project, you need to have installed the following tools.

```sh
# Install python. Version used for development: Python 3.11.4
# Install PostgreSQL. Version used for development: PostgreSQL 15.3
pip install --upgrade pip
pip install virtualenv
```
### Installation

1. Clone the repo

```sh
git clone https://github.com/carmengl00/ThinkUp.git
```
2. Create virtual environment

```sh
python -m venv venv
```

3. Install requirements

Install requirements in the virtual environment.
```sh
.\venv\Scripts\activate
pip install -r requirements.txt
```

4. Create database

Open terminal run the following command.
```sh
psql -U postgres
```
Complete with credentials used in the PostgreSQL installation.

```sh
CREATE USER think_admin WITH PASSWORD 'th1nk_adm1n'; #Create user
CREATE DATABASE thinkup WITH OWNER think_admin; #Create database with the created user
```

Migrations.
```sh
python manage.py makemigrations
python manage.py migrate
#Complete with credentials
python manage.py createsuperuser
```

5. Run

```sh
python manage.py runserver
```

### Json
The request collection is as follows and can be tested in /graphql.

* Register user
```sh
mutation{
  registerUser(username:"pepito", email:"pepito@gmail.com", password:"p@ssw0rd"){
    username
  }
}
```

* User login
```sh
mutation{
  tokenAuth(username: "pepito", password:"p@ssw0rd"){
    success
    errors
    token{
      token
    }
  }
}
```

* Password change
```sh
mutation{
  passwordChange(oldPassword:"p@ssw0rd",
    newPassword1:"newpassword123",
  	newPassword2:"newpassword123"
  ){
    success
    errors
  }
}
```

* Magic link
* Create idea
* Update visibility idea
* My ideas
* Delete idea
* Follow request
* My follow request
* My followers
* My followed
* Unfollow
* Delete follower
* Search user
* Ideas from other user
* Timeline
* My notifications
