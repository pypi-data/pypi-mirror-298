# Postgres Logging Handler

Simple handler to enter logs directly to postgres databases, uses psycopg2 for connection. Creates a new `table` if does not already exist, and groups logs by `job_id`.

Table columns are,
 - id 
 - created_at
 - name
 - levelname
 - message
 - job_id

## Example Usage

```python
from pglogginghandler import PostgresHandler

db_config = {
    'dbname': <dbname>,
    'user': <user>,
    'password': <password>,
    'host': <host>,
}
logger_name = 'logger name'
job_id = 'test_id'
table = 'table name'

logger = PostgresHandler(logger_name, job_id, table, db_config)
logger.info("this is a test info message")
```