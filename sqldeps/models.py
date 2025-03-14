from dataclasses import dataclass

import pandas as pd


@dataclass
class SQLAnalysis:
    """Data class to hold both SQL dependencies and outcomes."""

    # Dependencies (input tables/columns required by the query)
    dependencies: dict[str, list[str]]  # {table_name: [column_names]}

    # Outcomes (tables/columns created or modified by the query)
    outcomes: dict[str, list[str]]  # {table_name: [column_names]}

    def __post_init__(self):
        # Sort tables and columns for consistent output
        self.dependencies = {
            table: sorted(cols) for table, cols in sorted(self.dependencies.items())
        }
        self.outcomes = {
            table: sorted(cols) for table, cols in sorted(self.outcomes.items())
        }

    @property
    def dependency_tables(self) -> list[str]:
        """Get list of dependency tables."""
        return sorted(self.dependencies.keys())

    @property
    def outcome_tables(self) -> list[str]:
        """Get list of outcome tables."""
        return sorted(self.outcomes.keys())

    def to_dict(self) -> dict:
        return {"dependencies": self.dependencies, "outcomes": self.outcomes}

    def to_dataframe(self) -> pd.DataFrame:
        """Convert to a DataFrame with type column indicating dependency or outcome."""
        records = []

        # Add dependencies
        for table, columns in self.dependencies.items():
            schema, table_name = table.split(".") if "." in table else (None, table)
            if columns:
                for column in columns:
                    records.append(
                        {
                            "type": "dependency",
                            "schema": schema,
                            "table": table_name,
                            "column": column,
                        }
                    )
            else:
                records.append(
                    {
                        "type": "dependency",
                        "schema": schema,
                        "table": table_name,
                        "column": None,
                    }
                )

        # Add outcomes
        for table, columns in self.outcomes.items():
            schema, table_name = table.split(".") if "." in table else (None, table)
            if columns:
                for column in columns:
                    records.append(
                        {
                            "type": "outcome",
                            "schema": schema,
                            "table": table_name,
                            "column": column,
                        }
                    )
            else:
                records.append(
                    {
                        "type": "outcome",
                        "schema": schema,
                        "table": table_name,
                        "column": None,
                    }
                )

        return pd.DataFrame(records)
