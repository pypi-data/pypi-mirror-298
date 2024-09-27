import logging
from typing import List, Union, Literal

from ..types import EvaluationDataset
from .._client import SGPClient
from .types.multiturn import MultiturnTestCaseSchema
from .types.summarization import SummarizationTestCaseSchema
from ..types.evaluation_datasets import FlexibleTestCaseSchema, GenerationTestCaseSchema
from ..types.evaluation_datasets.test_case_batch_params import (
    Item as TestCaseItem,
)

log: logging.Logger = logging.getLogger("scale_gp")


TestCaseSchemas = Union[
    FlexibleTestCaseSchema, GenerationTestCaseSchema, SummarizationTestCaseSchema, MultiturnTestCaseSchema
]


class DatasetBuilder:
    def __init__(self, client: SGPClient):
        self.client = client
        self.dataset = None
        self.test_cases = None
        self.dataset_version = None

    def initialize(self, *, account_id: str, name: str, test_cases: List[TestCaseSchemas]) -> EvaluationDataset:
        if len(test_cases) == 0:
            raise ValueError(f"No test cases provided for dataset: {name}")

        formatted_test_cases = self._validate_test_case_schemas(test_cases=test_cases)
        schema_type = self._get_dataset_schema_type(formatted_test_cases)

        dataset = self.client.evaluation_datasets.create(account_id=account_id, schema_type=schema_type, name=name)
        log.info(f"Successfully created dataset with id: {dataset.id}")

        tc_items = [
            TestCaseItem(
                account_id=account_id,
                test_case_data=tc,
            )
            for tc in formatted_test_cases
        ]

        tcs = self.client.evaluation_datasets.test_cases.batch(evaluation_dataset_id=dataset.id, items=tc_items)
        log.info(f"Successfully created {len(tcs)} test cases")

        dataset_version = self.client.evaluation_datasets.publish(evaluation_dataset_id=dataset.id)

        self.dataset = dataset
        self.test_cases = tcs
        self.dataset_version = dataset_version

        return dataset

    def _get_dataset_schema_type(self, test_cases: List[TestCaseSchemas]) -> Literal["FLEXIBLE", "GENERATION"]:
        tc = test_cases[0]

        if isinstance(tc, FlexibleTestCaseSchema):
            return "FLEXIBLE"
        if isinstance(tc, GenerationTestCaseSchema):
            return "GENERATION"

        raise ValueError("Invalid test case schema")

    def _validate_test_case_schemas(self, test_cases: List[TestCaseSchemas]):
        if not test_cases:
            raise ValueError("No test cases provided")

        first_schema_type = type(test_cases[0])

        for i, tc in enumerate(test_cases[1:], start=1):
            if not isinstance(tc, first_schema_type):
                raise ValueError(
                    f"Inconsistent schema types. Test case at index 0 is {first_schema_type.__name__}, "
                    f"but test case at index {i} is {type(tc).__name__}"
                )

        log.info(f"All test cases validated. Schema type: {first_schema_type.__name__}")

        if first_schema_type == SummarizationTestCaseSchema:
            flexible_test_cases = [
                FlexibleTestCaseSchema(
                    input={"document": tc.document, **(tc.other_inputs or {})},
                    expected_output={
                        **({"expected_summary": tc.expected_summary} if tc.expected_summary is not None else {}),
                        **(tc.other_expected or {}),
                    },
                )
                for tc in test_cases
            ]
            return flexible_test_cases
        elif first_schema_type == MultiturnTestCaseSchema:
            flexible_test_cases = [
                FlexibleTestCaseSchema(
                    input={
                        "messages": tc.messages,
                        **({"turns": tc.turns} if tc.turns is not None else {}),
                        **(tc.other_inputs or {}),
                    },
                    expected_output={
                        **({"expected_messages": tc.expected_messages} if tc.expected_messages is not None else {}),
                        **(tc.other_expected or {}),
                    },
                )
                for tc in test_cases
            ]
            return flexible_test_cases

        return test_cases
