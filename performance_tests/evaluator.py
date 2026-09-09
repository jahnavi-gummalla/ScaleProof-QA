from locust import events
from performance_tests.result_reporter import save_json_summary
from config.thresholds import PERFORMANCE_THRESHOLDS


@events.quitting.add_listener
def evaluate_performance_thresholds(environment, **kwargs):
    stats = environment.stats.total

    if stats.num_requests == 0:
        print("\nSCALEPROOF RESULT: FAIL - No requests were executed.")
        environment.process_exit_code = 1
        return

    failure_rate = stats.fail_ratio * 100
    average_response_time = stats.avg_response_time
    p95_response_time = stats.get_response_time_percentile(0.95)
    p99_response_time = stats.get_response_time_percentile(0.99)

    violations = []

    if failure_rate > PERFORMANCE_THRESHOLDS["maximum_failure_rate_percent"]:
        violations.append(
            f"Failure rate {failure_rate:.2f}% exceeded the allowed threshold."
        )

    if average_response_time > PERFORMANCE_THRESHOLDS[
        "maximum_average_response_time_ms"
    ]:
        violations.append(
            f"Average response time {average_response_time:.2f} ms exceeded the threshold."
        )

    if p95_response_time > PERFORMANCE_THRESHOLDS[
        "maximum_p95_response_time_ms"
    ]:
        violations.append(
            f"P95 response time {p95_response_time:.2f} ms exceeded the threshold."
        )

    if p99_response_time > PERFORMANCE_THRESHOLDS[
        "maximum_p99_response_time_ms"
    ]:
        violations.append(
            f"P99 response time {p99_response_time:.2f} ms exceeded the threshold."
        )

    print("\n--- ScaleProof QA Performance Evaluation ---")
    print(f"Failure rate: {failure_rate:.2f}%")
    print(f"Average response time: {average_response_time:.2f} ms")
    print(f"P95 response time: {p95_response_time:.2f} ms")
    print(f"P99 response time: {p99_response_time:.2f} ms")

    if violations:
        status = "FAIL"
        print("SCALEPROOF RESULT: FAIL")

        for violation in violations:
            print(f"- {violation}")

        environment.process_exit_code = 1
    else:
        status = "PASS"
        print("SCALEPROOF RESULT: PASS")
        environment.process_exit_code = 0

    save_json_summary(
        environment=environment,
        status=status,
        violations=violations,
    )