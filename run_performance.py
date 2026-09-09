import argparse
import subprocess
import sys
import os
from datetime import datetime
from pathlib import Path

from config.load_profiles import LOAD_PROFILES


def build_argument_parser():
    parser = argparse.ArgumentParser(
        description="Run ScaleProof QA performance-test profiles."
    )
    parser.add_argument(
        "profile",
        choices=LOAD_PROFILES.keys(),
        help="Performance profile to execute.",
    )
    parser.add_argument(
        "--host",
        default="http://127.0.0.1:8000",
        help="Application host to test.",
    )
    return parser


def main():
    parser = build_argument_parser()
    args = parser.parse_args()
    profile = LOAD_PROFILES[args.profile]

    reports_directory = Path("reports")
    reports_directory.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = reports_directory / f"{args.profile}_{timestamp}.html"

    command = [
        sys.executable,
        "-m",
        "locust",
        "-f",
        profile.get(
            "locustfile",
            "performance_tests/locustfile.py",
        ),
        "--headless",
        "--users",
        str(profile["users"]),
        "--spawn-rate",
        str(profile["spawn_rate"]),
        "--run-time",
        profile["run_time"],
        "--host",
        args.host,
        "--html",
        str(report_path),
    ]

    print("\n--- ScaleProof QA Test Profile ---")
    print(f"Profile: {args.profile}")
    print(f"Description: {profile['description']}")
    print(f"Users: {profile['users']}")
    print(f"Spawn rate: {profile['spawn_rate']} users/second")
    print(f"Run time: {profile['run_time']}")
    print(f"Target: {args.host}")
    print(f"Report: {report_path}\n")

    process_environment = os.environ.copy()
    process_environment["SCALEPROOF_PROFILE"] = args.profile

    completed_process = subprocess.run(
        command,
        check=False,
        env=process_environment,
    )

    if completed_process.returncode == 0:
        print(f"\nProfile '{args.profile}' completed successfully.")
        print(f"HTML report created: {report_path}")
    else:
        print(f"\nProfile '{args.profile}' failed performance validation.")

    raise SystemExit(completed_process.returncode)


if __name__ == "__main__":
    main()