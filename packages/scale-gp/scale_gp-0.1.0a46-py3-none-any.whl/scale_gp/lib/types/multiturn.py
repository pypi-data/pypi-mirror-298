from typing import Any, Dict, List, Union, Optional

from scale_gp import BaseModel
from scale_gp.types.evaluation_datasets import FlexibleMessage


class MultiturnTestCaseSchema(BaseModel):
    messages: List[FlexibleMessage]
    turns: Optional[List[int]] = None
    expected_messages: Optional[List[FlexibleMessage]] = None
    other_inputs: Optional[Union[str, float, Dict[str, Any]]] = None
    other_expected: Optional[Union[str, float, Dict[str, Any]]] = None
