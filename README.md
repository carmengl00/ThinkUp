# ThinkUp

## Getting Started

To get a local copy up and running follow these steps:

### Prerequisites

Before working with the project, you need to have installed the following tools:

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

2. Install requirements

```sh
pip install -r requirements.txt
```
Install requirements in the virtual environment too.
```sh
.\venv\Scripts\activate
pip install -r requirements.txt
```

4. Create database

Open terminal with command
```sh
psql -U postgres
```
Complete with credentials used in the PostgreSQL installation.

```sh
CREATE USER think_admin WITH PASSWORD 'th1nk_adm1n'; #Create user
CREATE DATABASE thinkup WITH OWNER think_admin; #Create database with the created user
```

Migrations
```sh
python manage.py makemigrations
python manage.py migrate
#Complete with credentials
python manage.py createsuperuser
```

4. Run

```sh
python manage.py runserver
```
