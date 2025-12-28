"""Tests for data processing utilities."""

import pytest
import pandas as pd
import tempfile
import os
from data_processor import DataProcessor, process_pipeline


@pytest.fixture
def sample_data():
    """Create sample CSV for testing."""
    data = {
        'id': [1, 2, 3, 4, 5],
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'amount': [100.0, 200.0, 150.0, 300.0, 250.0],
        'date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05']
    }
    df = pd.DataFrame(data)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        df.to_csv(f.name, index=False)
        yield f.name
    
    os.unlink(f.name)


def test_data_processor_init(sample_data):
    """Test DataProcessor initialization."""
    processor = DataProcessor(sample_data)
    assert len(processor.df) == 5
    assert list(processor.df.columns) == ['id', 'name', 'amount', 'date']


def test_clean_data(sample_data):
    """Test data cleaning."""
    processor = DataProcessor(sample_data)
    cleaned = processor.clean_data()
    assert len(cleaned) == 5


def test_filter_by_date(sample_data):
    """Test date filtering."""
    processor = DataProcessor(sample_data)
    filtered = processor.filter_by_date('date', '2024-01-02', '2024-01-04')
    assert len(filtered) == 3


def test_get_summary(sample_data):
    """Test summary generation."""
    processor = DataProcessor(sample_data)
    summary = processor.get_summary()
    assert summary['total_rows'] == 5
    assert summary['total_columns'] == 4
    assert 'id' in summary['columns']
