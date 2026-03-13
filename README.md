## Project Structure

```text
big-fish-zhongbao
├── zhongBao_unit
│   ├── cookie2.txt      # Website login session / cookie storage
│   ├── emaill.py        # Email sender module for error alerts
│   ├── sqlserver.py     # SQL Server connection and database operations
│   └── __init__.py      # Python package initializer
│
├── config.json          # Application configuration file
├── orderLs.py           # Retrieves order data from the website order page
└── run.py               # Main entry script; processes data and saves it into the database
