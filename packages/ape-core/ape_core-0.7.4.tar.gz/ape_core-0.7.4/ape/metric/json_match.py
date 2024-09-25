from typing import Any, Dict, Optional, List
from ape.prompt.prompt_base import Prompt
from ape.metric.metric_base import BaseMetric
from ape.types import DataItem, DatasetItem, MetricResult
from ape.utils.logging import logger


class JsonMatchMetric(BaseMetric):
    """
    A metric class that computes the similarity between two JSON-like structures.

    This metric compares two dictionaries or lists, considering the structure and content
    of nested objects. It can optionally consider list order and ignore specified keys.

    Attributes:
        consider_list_order (bool): If True, list order is considered in comparisons.
            Defaults to False.
        ignore_keys (List[str]): A list of keys to ignore during comparison.
            Keys are normalized to lowercase with spaces replaced by underscores.

    Methods:
        compute(gold: DataItem, pred: Dict[str, Any], trace: Optional[Dict] = None) -> float:
            Computes the similarity score between the gold standard and prediction.

    The similarity score is calculated as the ratio of correctly matched fields to total fields,
    with nested structures being recursively compared. For non-exact matches, it falls back to
    using an LLM-based binary judge for scoring.
    """

    def __init__(
        self, consider_list_order: bool = False, ignore_keys: Optional[List[str]] = None
    ):
        self.binary_judge = Prompt.from_filename("binary-judge")
        self.consider_list_order = (
            consider_list_order  # Flag to determine whether to consider list order
        )
        self.ignore_keys = (
            [key.lower().replace(" ", "_") for key in ignore_keys]
            if ignore_keys
            else []
        )  # List of keys to ignore during comparison

    async def compute(
        self, inputs: Dict[str, Any], gold: DataItem, pred: Dict[str, Any], trace: Optional[Dict] = None, metadata: Optional[Dict] = None
    ) -> MetricResult:
        """
        Compute the similarity score between the gold standard and prediction.

        Args:
            gold (DataItem): The gold standard data item.
            pred (Dict[str, Any]): The prediction to compare against the gold standard.
            trace (Optional[Dict]): Additional trace information (not used in this implementation).

        Returns:
            float: The computed similarity score between 0 and 1.

        This method normalizes both inputs, compares their structures recursively,
        and returns a float representing the overall similarity. It handles nested
        dictionaries and lists, applying special comparison logic based on the
        `consider_list_order` attribute.
        """

        async def compare_lists(list1, list2):
            if not list1 and not list2:
                return 1.0
            if not list1 or not list2:
                return 0.0

            if self.consider_list_order:
                if len(list1) != len(list2):
                    return 0.0
                total_score = 0.0
                for a, b in zip(list1, list2):
                    if isinstance(a, dict) and isinstance(b, dict):
                        score = await compare_dicts(a, b)
                    else:
                        score = 1.0 if a == b else 0.0
                    total_score += score
                return total_score / len(list1)
            else:
                # For unordered lists, handle dictionaries by matching each dict in list1 to the best match in list2
                if any(isinstance(item, dict) for item in list1 + list2):
                    matched_indices = set()
                    total_score = 0.0
                    for a in list1:
                        best_score = 0.0
                        best_idx = -1
                        for idx, b in enumerate(list2):
                            if idx in matched_indices:
                                continue
                            if isinstance(a, dict) and isinstance(b, dict):
                                score = await compare_dicts(a, b)
                            else:
                                score = 1.0 if a == b else 0.0
                            if score > best_score:
                                best_score = score
                                best_idx = idx
                        if best_score > 0.0:
                            matched_indices.add(best_idx)
                        total_score += best_score
                    total_score += (len(list2) - len(matched_indices)) * 0.0  # Unmatched items contribute 0
                    total_items = max(len(list1), len(list2))
                    return total_score / total_items if total_items > 0 else 0.0
                else:
                    # If no dictionaries, proceed with set comparison
                    set1 = set(list1)
                    set2 = set(list2)

                    num_identical = len(set1.intersection(set2))
                    total_unique = len(set1.union(set2))

                    return num_identical / total_unique

        async def compare_dicts(dict1, dict2):
            total_fields = 0
            correct_fields = 0
            for key in dict1:
                if key in self.ignore_keys:
                    continue  # Skip keys that should be ignored
                if key in dict2:
                    try:
                        total_fields += 1
                        if isinstance(dict1[key], list) and isinstance(dict2[key], list):
                            score = await compare_lists(dict1[key], dict2[key])
                        elif isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                            score = await compare_dicts(dict1[key], dict2[key])
                        elif dict1[key] == dict2[key]:
                            score = 1.0
                        else:
                            # Use LLM judge as a fallback for non-matching fields
                            res: dict = await self.binary_judge(
                                ground_truth=dict1[key], prediction=dict2[key]
                            )
                            score = res.get("score", 0)
                        correct_fields += score
                    except Exception as err:
                        logger.error(f"Error in JsonMatchMetric compare_dicts: {err}")
                        continue
            return correct_fields / total_fields if total_fields > 0 else 0

        try:
            gold = gold.model_dump() if isinstance(gold, DatasetItem) else gold
            pred = pred.model_dump() if isinstance(pred, DatasetItem) else pred

            # Normalize keys
            gold_dict = {k.lower().replace(" ", "_"): v for k, v in gold.items()}
            pred_dict = {k.lower().replace(" ", "_"): v for k, v in pred.items()}

            accuracy = await compare_dicts(gold_dict, pred_dict)
            return MetricResult(
                score=accuracy,
            )

        except Exception as e:
            logger.error(f"Error in JsonMatchMetric: {e}")
            return MetricResult(
                score=0.0,
                intermediate_values={"error": str(e)}
            )