# Three-layer architecture using FastAPI, Pydantic, and a PostgreSQL database

```text
my_project/
│
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── questionnaire.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── questionnaire_service.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── repository.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── questionnaire.py
│   ├── main.py
│   ├── config.py
│
├── tests/
│   ├── test_api/
│   ├── test_services/
│   ├── test_db/
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   ├── script.py.mako
│
├── alembic.ini
├── requirements.txt
├── README.md

```