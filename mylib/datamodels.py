from pydantic import BaseModel, Field

class Factor(BaseModel):
    """
    Represents an individual factor within an element.

    Attributes:
        factor_index (str): The index label of the factor (e.g., 'Factor 1').
        factor_title (str): The short title of the factor (e.g., 'Program structure').
        factor_description (str): The full description text of the factor.
        factor_explanation (str): Additional notes or explanation related to the factor.
        factor_critical (bool): Whether the factor is marked as 'MUST-PASS' or otherwise critical.
    """
    factor_index: str = Field(..., description="The index label of the factor (e.g., 'Factor 1').")
    factor_title: str = Field(..., description="The title of the factor.")
    factor_description: str = Field(..., description="Detailed description of the factor's content.")
    factor_explanation: str = Field(..., description="Explanation or rationale for the factor.")
    factor_critical: bool = Field(False, description="Indicates if the factor is a critical factor.")