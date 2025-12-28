"""Data engineering utilities for ETL pipelines."""

import pandas as pd
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataProcessor:
    """Process and transform data."""
    
    def __init__(self, csv_path: str):
        """Initialize with data file."""
        self.df = pd.read_csv(csv_path)
        logger.info(f"Loaded {len(self.df)} rows from {csv_path}")
    
    def clean_data(self) -> pd.DataFrame:
        """Clean the dataset."""
        # Remove duplicates
        self.df = self.df.drop_duplicates()
        
        # Remove rows with null values
        self.df = self.df.dropna()
        
        logger.info(f"After cleaning: {len(self.df)} rows")
        return self.df
    
    def filter_by_date(self, date_column: str, start_date: str, end_date: str) -> pd.DataFrame:
        """Filter data by date range."""
        self.df[date_column] = pd.to_datetime(self.df[date_column])
        filtered = self.df[
            (self.df[date_column] >= start_date) & 
            (self.df[date_column] <= end_date)
        ]
        logger.info(f"Filtered to {len(filtered)} rows")
        return filtered
    
    def aggregate(self, group_by: List[str], agg_dict: Dict[str, str]) -> pd.DataFrame:
        """Aggregate data."""
        result = self.df.groupby(group_by).agg(agg_dict)
        logger.info(f"Aggregation complete: {len(result)} groups")
        return result
    
    def get_summary(self) -> Dict[str, Any]:
        """Get data summary statistics."""
        return {
            "total_rows": len(self.df),
            "total_columns": len(self.df.columns),
            "columns": self.df.columns.tolist(),
            "dtypes": self.df.dtypes.to_dict(),
            "missing_values": self.df.isnull().sum().to_dict(),
        }


def process_pipeline(input_file: str, output_file: str) -> None:
    """Run a complete data processing pipeline."""
    logger.info(f"Starting pipeline: {input_file} -> {output_file}")
    
    processor = DataProcessor(input_file)
    
    # Clean
    processor.clean_data()
    
    # Transform
    summary = processor.get_summary()
    logger.info(f"Data summary: {summary}")
    
    # Save
    processor.df.to_csv(output_file, index=False)
    logger.info(f"Pipeline complete. Output saved to {output_file}")


if __name__ == "__main__":
    # Example usage
    logger.info("Data engineering module loaded")
