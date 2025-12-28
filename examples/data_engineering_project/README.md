# Data Engineering Project Example

A complete data engineering project demonstrating ETL pipelines with pandas, polars, and SQLAlchemy.

## Features

- Data processing with pandas
- Multiple dependency groups (core, database, pipeline, viz)
- Data cleaning and transformation
- Comprehensive tests
- Production-ready structure

## Getting Started

### Install dependencies

```bash
# Install core dependencies only
uv sync

# Or install all dependencies including pipeline and visualization
uv sync --all-groups
```

### Run the data processor

```bash
# Process a CSV file
uv run python data_processor.py

# Or use as a module
uv run python -c "from data_processor import DataProcessor; p = DataProcessor('data.csv')"
```

### Run tests

```bash
uv run pytest
uv run pytest -v --cov
```

### Format code

```bash
uv run black .
uv run ruff check . --fix
```

## Project Structure

```
data_engineering_project/
├── pyproject.toml              # Project configuration with dependency groups
├── data_processor.py           # Main data processing module
├── test_data_processor.py      # Unit tests
├── README.md                   # This file
└── notebooks/                  # Jupyter notebooks (if using)
    └── analysis.ipynb
```

## Dependency Groups

This project uses dependency groups for different use cases:

### Core Dependencies
Essential for data processing:
- pandas - Data manipulation
- polars - Fast dataframes
- sqlalchemy - Database ORM
- python-dotenv - Environment variables

```bash
uv sync --group core
```

### Database Dependencies
For database connectivity:
- psycopg2 - PostgreSQL
- pymysql - MySQL

```bash
uv sync --group database
```

### Pipeline Dependencies
For orchestration:
- apache-airflow - Workflow orchestration
- dbt-core - Data transformation

```bash
uv sync --group pipeline
```

### Visualization Dependencies
For data visualization:
- matplotlib - Static plots
- plotly - Interactive plots

```bash
uv sync --group viz
```

### Development Dependencies
For development and testing:
- pytest - Testing framework
- black - Code formatting
- ruff - Linting
- mypy - Type checking
- jupyter - Notebooks

```bash
uv sync --group dev
```

## Usage Examples

### Load and process CSV

```python
from data_processor import DataProcessor

processor = DataProcessor('data.csv')
processor.clean_data()
summary = processor.get_summary()
print(summary)
```

### Filter data

```python
filtered = processor.filter_by_date('date_column', '2024-01-01', '2024-12-31')
```

### Aggregate data

```python
aggregated = processor.aggregate(
    group_by=['category'],
    agg_dict={'amount': 'sum', 'count': 'count'}
)
```

## Running a Pipeline

```bash
uv run python -c "from data_processor import process_pipeline; process_pipeline('input.csv', 'output.csv')"
```

## Working with Jupyter Notebooks

```bash
# Install Jupyter
uv sync --group dev

# Start Jupyter
uv run jupyter notebook
```

## Next Steps

- Integrate with a database (PostgreSQL, MySQL)
- Set up Airflow DAGs for scheduled pipelines
- Add dbt for data modeling
- Deploy to cloud platforms (AWS, GCP, Azure)
- Add data quality checks
