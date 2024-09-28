import pandas as pd


def assert_that_type_value(df: pd.DataFrame, column_name: str, data_type: type) -> bool:
    """
    Check if all non-null entries in a specified column of a DataFrame are of the specified data type.

    Args:
        df : The DataFrame to check.
        column_name : The name of the column to check.
        data_type : The expected data type of the column entries.

    Returns:
        bool: True if all non-null entries in the specified column are of the specified data type, False otherwise.

    Raises:
        ValueError: If the column does not exist in the DataFrame or if at least one entry is not of the specified data type.
    """
    if column_name not in df.columns:
        raise ValueError(f'Column "{column_name}" not in DataFrame.')

    filtered_values = df[df[column_name].notnull()]
    return filtered_values[column_name].apply(lambda x: isinstance(x, data_type)).all()
