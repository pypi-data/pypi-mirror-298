# Downer Azure Helper

Collection of functions to wrap the Azure SDK.

## Get Secret Value

Retrieve the value of a keyvault secret.

### Example Usage

```python
from azurehelper import PostgresLogHandler

value = get_secret_value(secret_name, keyvault_url)
```

## Postgres Log Handler

Simple handler to enter logs directly to postgres databases, uses psycopg2 for connection. Creates a new `table` if does not already exist, and groups logs by `job_id`.

### Example Usage

```python
from azurehelper import PostgresLogHandler

db_config = {
    'dbname': <dbname>,
    'user': <user>,
    'password': <password>,
    'host': <host>,
}
logger_name = 'logger name'
job_id = 'test_id'
table = 'table name'

logger = PostgresLogHandler(logger_name, job_id, table, db_config)
logger.info("this is a test info message")
```