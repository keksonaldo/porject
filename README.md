# Photo WebP Converter

Django MVP for uploading one image, detecting its type and size, and converting it to WebP.

## Local Setup

```bash
source bin/activate
cp .env.example .env
python my_project/manage.py check
python my_project/manage.py runserver
```

The app opens at http://127.0.0.1:8000/.

## Configuration

Database settings are read from `.env`:

```bash
DB_NAME=project
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306
```

The local `.env`, virtual environment, uploaded media, caches, and SQLite files are ignored by Git.
