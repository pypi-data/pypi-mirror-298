from __future__ import annotations

import logging
from typing import Any, Dict, List

from splink.internals.comparison_level import ComparisonLevel
from splink.internals.constants import LEVEL_NOT_OBSERVED_TEXT

logger = logging.getLogger(__name__)


def m_u_records_to_lookup_dict(
    m_u_records: List[Dict[str, Any]],
) -> Dict[str, Dict[int, Any]]:
    lookup: Dict[str, Dict[int, Any]] = {}
    for m_u_record in m_u_records:
        comparison_name = m_u_record["output_column_name"]
        level_value = m_u_record["comparison_vector_value"]
        if comparison_name not in lookup:
            lookup[comparison_name] = {}
        if level_value not in lookup[comparison_name]:
            lookup[comparison_name][level_value] = {}

        m_prob = m_u_record["m_probability"]

        u_prob = m_u_record["u_probability"]

        if m_prob is not None:
            lookup[comparison_name][level_value]["m_probability"] = m_prob
        if u_prob is not None:
            lookup[comparison_name][level_value]["u_probability"] = u_prob

    return lookup


def not_trained_message(
    comparison_level: ComparisonLevel, output_column_name: str
) -> str:
    cl = comparison_level
    return (
        f"not trained for {output_column_name} - "
        f"{cl.label_for_charts} (comparison vector value: "
        f"{cl.comparison_vector_value}). This usually means the "
        "comparison level was never observed in the training data."
    )


def append_u_probability_to_comparison_level_trained_probabilities(
    comparison_level: ComparisonLevel,
    m_u_records_lookup: Dict[str, Any],
    output_column_name: str,
    training_description: str,
) -> None:
    cl = comparison_level

    try:
        u_probability = m_u_records_lookup[output_column_name][
            cl.comparison_vector_value
        ]["u_probability"]

    except KeyError:
        u_probability = LEVEL_NOT_OBSERVED_TEXT

        logger.info(f"u probability {not_trained_message(cl, output_column_name)}")
    cl._add_trained_u_probability(
        u_probability,
        training_description,
    )


def append_m_probability_to_comparison_level_trained_probabilities(
    comparison_level: ComparisonLevel,
    m_u_records_lookup: Dict[str, Any],
    output_column_name: str,
    training_description: str,
) -> None:
    cl = comparison_level

    try:
        m_probability = m_u_records_lookup[output_column_name][
            cl.comparison_vector_value
        ]["m_probability"]

    except KeyError:
        m_probability = LEVEL_NOT_OBSERVED_TEXT

        logger.info(f"m probability {not_trained_message(cl, output_column_name)}")
    cl._add_trained_m_probability(
        m_probability,
        training_description,
    )
