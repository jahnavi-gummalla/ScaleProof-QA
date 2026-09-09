import json
import os
from datetime import datetime, timezone
from pathlib import Path


def save_json_summary(environment, status, violations):
    stats = environment.stats.total
    profile = os.getenv("SCALEPROOF_PROFILE", "manual")

    endpoint_results = []

    for entry in environment.stats.entries.values():
        endpoint_results.append(
            {
                "method": entry.method,
                "name": entry.name,
                "requests": entry.num_requests,
                "failures": entry.num_failures,
                "average_response_time_ms": round(
                    entry.avg_response_time,
                    2,
                ),
                "p95_response_time_ms": round(
                    entry.get_response_time_percentile(0.95),
                    2,
                ),
                "p99_response_time_ms": round(
                    entry.get_response_time_percentile(0.99),
                    2,
                ),
            }
        )

    summary = {
        "project": "ScaleProof QA",
        "profile": profile,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "summary": {
            "total_requests": stats.num_requests,
            "total_failures": stats.num_failures,
            "failure_rate_percent": round(stats.fail_ratio * 100, 2),
            "average_response_time_ms": round(
                stats.avg_response_time,
                2,
            ),
            "p95_response_time_ms": round(
                stats.get_response_time_percentile(0.95),
                2,
            ),
            "p99_response_time_ms": round(
                stats.get_response_time_percentile(0.99),
                2,
            ),
            "requests_per_second": round(stats.total_rps, 2),
        },
        "threshold_violations": violations,
        "endpoints": endpoint_results,
    }

    reports_directory = Path("reports")
    reports_directory.mkdir(exist_ok=True)

    report_path = reports_directory / f"{profile}_latest_summary.json"

    with report_path.open("w", encoding="utf-8") as report_file:
        json.dump(summary, report_file, indent=2)

    print(f"JSON summary created: {report_path}")