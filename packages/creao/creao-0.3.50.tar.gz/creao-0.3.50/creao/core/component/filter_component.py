import operator
from typing import Dict, List, Union
from creao.core.component.util import creao_component

@creao_component  # This decorator registers the class as a component in a pipeline framework
class FilterComponent:
    """
    FilterComponent is responsible for filtering data based on a specific condition applied to a designated column.
    The component can perform two types of filtering:
    1. Exact match filtering for strings or direct equality comparison.
    2. Numeric condition filtering for values that need to meet a specified numeric condition (e.g., >, <, >=).

    Attributes:
    - filtered_column (str): The name of the column on which the filter is applied.
    - condition_type (str): The type of filtering condition. It can be either "exact_match" or "numeric_condition".
    - condition_value (List[Union[str, int, float]]): The values or conditions used for filtering. 
      It can be a list of strings for an exact match condition or a list of numeric conditions (e.g., ["> 5", "== 10"]).
    - pipeline_id (str): Identifier for the pipeline this component belongs to. Defaults to "pipeline_id_default".
    - component_name (str): Name of the component, default is "FilterComponent".
    - **kwargs: Additional arguments that can be passed for customization.

    Methods:
    - run(chained_input: List[Dict[str, Union[str, int, float]]]) -> List[Dict[str, Union[str, int, float]]]:
      This method performs the filtering on the input data (a list of dictionaries). It processes each dictionary (or row)
      and filters it based on the specified conditions. It returns the filtered data as a list of dictionaries.

      - chained_input: The input data, which is expected to be a list of dictionaries where each dictionary represents a row or record.
      - filtered_output: The filtered data after applying the conditions.

      The method supports:
      - "exact_match" condition: Filters based on string equality or direct comparison to specific values.
      - "numeric_condition" condition: Filters based on numerical comparison using operators like >, <, >=, etc.

      Example usage:
      - If the condition_type is "exact_match" and condition_value is ["apple"], it will filter and return only the rows where
        the specified column has the value "apple".
      - If the condition_type is "numeric_condition" and condition_value is ["> 50"], it will filter and return rows where the
        numeric value in the specified column meets the condition "> 50".

      If the column value cannot be found in the row or cannot be converted to a number for numeric conditions, the row is skipped.
    """

    def __init__(
        self,
        filtered_column: str,
        condition_type: str = "exact_match",  # or "numeric_condition"
        condition_value: List[Union[str, int, float]] = [],
        pipeline_id: str = "pipeline_id_default",
        component_name: str = "FilterComponent",
        **kwargs,
    ):
        self.filtered_column = filtered_column  # Column to apply the filter on
        self.condition_type = condition_type  # Type of condition, either "exact_match" or "numeric_condition"
        self.condition_value = [condition_value] if not isinstance(condition_value, list) else condition_value
        self.pipeline_id = pipeline_id  # ID of the pipeline this component belongs to
        self.component_name = component_name  # Name of the component
    
    def get_operator(self, condition: str):
        if ">" in condition:
            return operator.gt, float(condition.split(">")[1].strip())
        elif "<" in condition:
            return operator.lt, float(condition.split("<")[1].strip())
        elif ">=" in condition:
            return operator.ge, float(condition.split(">=")[1].strip())
        elif "<=" in condition:
            return operator.le, float(condition.split("<=")[1].strip())
        elif "==" in condition:
            return operator.eq, float(condition.split("==")[1].strip())
        else:
            raise ValueError(f"Unsupported numeric condition: {condition}")
        
    def run(
        self, chained_input: List[Dict[str, Union[str, int, float]]]
    ) -> List[Dict[str, Union[str, int, float]]]:
        filtered_data = []
        for single_chained_input in chained_input:
            assert (
                self.filtered_column in single_chained_input
            ), f"Column '{self.filtered_column}' not found in the input data."
            
            column_values = single_chained_input.get(self.filtered_column, [])
            filtered_output = []
            
            # Handle different condition types
            for column_value in column_values:
                if self.condition_type == "exact_match":
                    if column_value in self.condition_value:
                        filtered_output.append(column_value)

                elif self.condition_type == "numeric_condition":
                    try:
                        numeric_value = float(column_value)
                        valid = True
                        for condition in self.condition_value:
                            condition_op, condition_val = self.get_operator(condition)
                            if not condition_op(numeric_value, condition_val):
                                valid = False
                                break
                        if valid:
                            filtered_output.append(column_value)
                    except ValueError:
                        continue
            
            single_chained_input[self.filtered_column] = filtered_output
            filtered_data.append(single_chained_input)
        
        return filtered_data  # Return the filtered data