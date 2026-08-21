from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from apparatus.canonical import load_json, write_json
from apparatus.constants import ROOT


MUTATION_ACTIONS = {"patch", "replace_file"}


def _cell_root(run_root: Path, cell: str) -> Path:
    matches = list((run_root / "cells").glob(f"*-{cell}-recurrent-oldest-fit-horizon-v0"))
    if len(matches) != 1:
        raise RuntimeError(f"cannot resolve measured cell directory: {cell}")
    return matches[0]


def _sum_changes(changes: list[dict[str, Any]] | None) -> int:
    return sum(int(change["token_savings"]) for change in (changes or []))


def analyze(run_root: Path) -> dict[str, Any]:
    run_root = run_root.resolve()
    run = load_json(run_root / "RUN_RESULT.json")
    capacity = load_json(ROOT / "CAPACITY_PREFLIGHT.json")
    initial_by_cell = {row["cell"]: row for row in capacity["cells"]}
    cells: list[dict[str, Any]] = []

    for cell_result in run["cells"]:
        cell = cell_result["cell"]
        root = _cell_root(run_root, cell)
        initial = initial_by_cell[cell]
        calls: list[dict[str, Any]] = []

        for call in cell_result["calls"]:
            number = int(call["call"])
            budget = load_json(root / "budget" / f"after-call-{number:02d}.json")
            changes = budget.get("changes") or []
            action_name = call["action"]["action"]
            calls.append(
                {
                    "call": number,
                    "action": call["action"],
                    "classification": call["classification"],
                    "admitted": call["admitted"],
                    "candidate_changed": call["candidate_before"] != call["candidate_after"],
                    "prompt_tokens": call["provider_usage"]["prompt_tokens"],
                    "cached_prompt_tokens": call["provider_usage"].get("prompt_tokens_details", {}).get("cached_tokens", 0),
                    "completion_tokens": call["provider_usage"]["completion_tokens"],
                    "total_tokens": call["provider_usage"]["total_tokens"],
                    "http_duration_ms": call["http_duration_ms"],
                    "result_delivered_to_later_call": call["result_delivered_to_later_call"],
                    "result_message_sha256": call["result_message_sha256"],
                    "post_call_pressure_observed": budget["pressure_triggered"],
                    "post_call_delivery_status": budget["delivery_status"],
                    "post_call_raw_capacity": budget["raw_post_result"],
                    "post_call_policy_attempted": "policy_applied" in budget,
                    "post_call_policy_applied": budget.get("policy_applied"),
                    "post_call_policy_capacity": budget.get("post_policy"),
                    "post_call_new_demotions": len(changes),
                    "post_call_tokens_recovered": _sum_changes(changes),
                    "post_call_changes": changes,
                    "action_key": call["action_key"],
                    "acquisition_novelty": call["acquisition_novelty"],
                    "repeat_within_four_acquisitions": call["repeat_within_four_acquisitions"],
                    "formal_short_cycle_thrash_ending_here": call["formal_short_cycle_thrash_ending_here"],
                    "local_nonchurn_window_ending_here": call["local_nonchurn_window_ending_here"],
                    "is_mutation": action_name in MUTATION_ACTIONS,
                    "is_check": action_name == "check",
                    "is_submission": action_name == "submit",
                }
            )

        prompt_tokens = sum(row["prompt_tokens"] for row in calls)
        cached_tokens = sum(row["cached_prompt_tokens"] for row in calls)
        recurrent_resolved = sum(
            row["post_call_policy_applied"] is True
            and row["post_call_policy_capacity"] is not None
            and row["post_call_policy_capacity"]["fits"] is True
            for row in calls
        )
        recurrent_demotions = sum(row["post_call_new_demotions"] for row in calls)
        recurrent_recovered = sum(row["post_call_tokens_recovered"] for row in calls)
        cells.append(
            {
                "cell": cell,
                "seed": cell_result["seed"],
                "initial_control_capacity": initial["raw_control_after_pending_result"],
                "initial_treatment_capacity": initial["horizon_start_after_pressure_policy"],
                "initial_demotions": initial["newly_demoted_count"],
                "initial_tokens_recovered": initial["tokens_recovered"],
                "calls": calls,
                "model_calls": len(calls),
                "admitted_actions": sum(row["admitted"] is True for row in calls),
                "exact_reopens": sum(row["classification"] == "exact_reopen_of_demoted_result" for row in calls),
                "other_acquisitions": sum(row["classification"] == "other_acquisition" for row in calls),
                "mutations": sum(row["is_mutation"] for row in calls),
                "checks": sum(row["is_check"] for row in calls),
                "submissions": sum(row["is_submission"] for row in calls),
                "new_call_results_delivered_to_later_calls": sum(row["result_delivered_to_later_call"] for row in calls),
                "delivered_results_including_predecessor_call_03": cell_result["delivered_result_count_including_predecessor_call_03_result"],
                "recurrent_pressure_events_resolved": recurrent_resolved,
                "post_call_pressure_events_observed": sum(row["post_call_pressure_observed"] is True for row in calls),
                "post_call_results_custodied_not_delivered": sum(
                    row["post_call_delivery_status"] == "not_attempted_due_to_frozen_call_limit" for row in calls
                ),
                "recurrent_demotions": recurrent_demotions,
                "recurrent_tokens_recovered": recurrent_recovered,
                "all_demotions_including_initial": initial["newly_demoted_count"] + recurrent_demotions,
                "all_tokens_recovered_including_initial": initial["tokens_recovered"] + recurrent_recovered,
                "prompt_tokens": prompt_tokens,
                "cached_prompt_tokens": cached_tokens,
                "uncached_prompt_tokens": prompt_tokens - cached_tokens,
                "completion_tokens": sum(row["completion_tokens"] for row in calls),
                "serialized_tokens": sum(row["total_tokens"] for row in calls),
                "http_duration_ms": sum(row["http_duration_ms"] for row in calls),
                "candidate_changed": cell_result["initial_candidate_id"] != cell_result["final_candidate_id"],
                "formal_short_cycle_thrash_observed": cell_result["formal_short_cycle_thrash_observed"],
                "formal_short_cycle_thrash_calls": cell_result["formal_short_cycle_thrash_calls"],
                "repeat_within_four_calls": cell_result["repeat_within_four_calls"],
                "local_nonchurn_window_observed": cell_result["local_nonchurn_window_observed"],
                "local_nonchurn_window_calls": cell_result["local_nonchurn_window_calls"],
                "duplicate_acquisitions": cell_result["duplicate_acquisitions"],
                "novel_acquisitions": cell_result["novel_acquisitions"],
                "terminal_class": cell_result["terminal_class"],
                "endpoint": cell_result["endpoint"],
            }
        )

    aggregate = {
        "cells": len(cells),
        "model_calls": sum(row["model_calls"] for row in cells),
        "admitted_actions": sum(row["admitted_actions"] for row in cells),
        "exact_reopens": sum(row["exact_reopens"] for row in cells),
        "other_acquisitions": sum(row["other_acquisitions"] for row in cells),
        "mutations": sum(row["mutations"] for row in cells),
        "checks": sum(row["checks"] for row in cells),
        "submissions": sum(row["submissions"] for row in cells),
        "initial_pressure_events_resolved": len(cells),
        "recurrent_pressure_events_resolved": sum(row["recurrent_pressure_events_resolved"] for row in cells),
        "results_delivered_to_new_decisions_including_frozen_pending": sum(
            row["delivered_results_including_predecessor_call_03"] for row in cells
        ),
        "new_call_results_delivered_to_later_calls": sum(
            row["new_call_results_delivered_to_later_calls"] for row in cells
        ),
        "post_call_pressure_events_observed": sum(row["post_call_pressure_events_observed"] for row in cells),
        "terminal_results_custodied_not_delivered": sum(
            row["post_call_results_custodied_not_delivered"] for row in cells
        ),
        "initial_demotions": sum(row["initial_demotions"] for row in cells),
        "recurrent_demotions": sum(row["recurrent_demotions"] for row in cells),
        "all_demotions_including_initial": sum(row["all_demotions_including_initial"] for row in cells),
        "initial_tokens_recovered": sum(row["initial_tokens_recovered"] for row in cells),
        "recurrent_tokens_recovered": sum(row["recurrent_tokens_recovered"] for row in cells),
        "all_tokens_recovered_including_initial": sum(row["all_tokens_recovered_including_initial"] for row in cells),
        "prompt_tokens": sum(row["prompt_tokens"] for row in cells),
        "cached_prompt_tokens": sum(row["cached_prompt_tokens"] for row in cells),
        "uncached_prompt_tokens": sum(row["uncached_prompt_tokens"] for row in cells),
        "completion_tokens": sum(row["completion_tokens"] for row in cells),
        "serialized_tokens": sum(row["serialized_tokens"] for row in cells),
        "http_duration_ms": sum(row["http_duration_ms"] for row in cells),
        "candidate_changes": sum(row["candidate_changed"] for row in cells),
        "cells_with_formal_short_cycle_thrash": sum(row["formal_short_cycle_thrash_observed"] for row in cells),
        "cells_with_local_nonchurn_window": sum(row["local_nonchurn_window_observed"] for row in cells),
        "duplicate_acquisitions": sum(row["duplicate_acquisitions"] for row in cells),
        "novel_acquisitions": sum(row["novel_acquisitions"] for row in cells),
        "terminal_classes": {name: sum(row["terminal_class"] == name for row in cells) for name in sorted({row["terminal_class"] for row in cells})},
    }
    aggregate["cached_prompt_fraction"] = (
        aggregate["cached_prompt_tokens"] / aggregate["prompt_tokens"] if aggregate["prompt_tokens"] else 0.0
    )

    return {
        "schema_version": "recurrent-context-reduction-horizon-measured-analysis-v0",
        "run_id": run["run_id"],
        "standalone_commit_at_inference": run["standalone_commit"],
        "source_lock_sha256": run["source_lock_sha256"],
        "policy_id": "pressure_oldest_positive_savings_until_fit_v1",
        "cells": cells,
        "aggregate": aggregate,
        "claim_boundary": (
            "The long-horizon recurrence result is measured at two trajectories on one task/world under one policy. "
            "Formal repetition is mechanical, and later action choice is descriptive because no matched behavioral comparator exists."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-root", type=Path, required=True)
    args = parser.parse_args()
    receipt = analyze(args.run_root)
    write_json(args.run_root.resolve() / "analysis" / "ANALYSIS.json", receipt)
    print(json.dumps({"run_id": receipt["run_id"], "aggregate": receipt["aggregate"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
