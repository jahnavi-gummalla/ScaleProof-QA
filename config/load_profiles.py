LOAD_PROFILES = {
    "smoke": {
        "users": 5,
        "spawn_rate": 1,
        "run_time": "15s",
        "description": "Quick validation that the system accepts traffic.",
    },
    "baseline": {
        "users": 10,
        "spawn_rate": 2,
        "run_time": "30s",
        "description": "Measures normal system performance under light traffic.",
    },
    "load": {
        "users": 50,
        "spawn_rate": 5,
        "run_time": "1m",
        "description": "Validates performance under expected business traffic.",
    },
    "stress": {
        "users": 100,
        "spawn_rate": 10,
        "run_time": "1m",
        "description": "Evaluates behavior near and beyond expected capacity.",
    },
    "reliability": {
        "users": 20,
        "spawn_rate": 4,
        "run_time": "30s",
        "locustfile": "performance_tests/reliability_locustfile.py",
        "description": (
            "Validates availability, degraded latency, and controlled failure behavior."
        ),
    },
    "spike": {
        "users": 150,
        "spawn_rate": 50,
        "run_time": "45s",
        "description": "Measures stability during a sudden traffic increase.",
    },
}