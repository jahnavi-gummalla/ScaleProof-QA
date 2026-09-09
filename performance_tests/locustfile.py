from locust import HttpUser, between, task
from performance_tests import evaluator as _evaluator
from random import randint

class ScaleProofUser(HttpUser):
    host = "http://127.0.0.1:8000"
    wait_time = between(1, 3)

    @task(1)
    def check_health(self):
        with self.client.get(
            "/health",
            name="GET /health",
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(
                    f"Health check returned status {response.status_code}"
                )
            elif response.json().get("status") != "healthy":
                response.failure("Service reported an unhealthy status")
            else:
                response.success()

    @task(3)
    def browse_products(self):
        with self.client.get(
            "/api/products",
            name="GET /api/products",
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(
                    f"Products request returned status {response.status_code}"
                )
            elif not response.json().get("products"):
                response.failure("Products response was empty")
            else:
                response.success()

    @task(1)
    def visit_homepage(self):
        self.client.get("/", name="GET /")

    @task(2)
    def place_order(self):
        order_payload = {
            "customer_id": randint(100, 999),
            "items": [
                {
                    "product_id": randint(1, 3),
                    "quantity": randint(1, 3),
                }
            ],
        }

        with self.client.post(
            "/api/orders",
            json=order_payload,
            name="POST /api/orders",
            catch_response=True,
        ) as response:
            if response.status_code != 201:
                response.failure(
                    f"Order request returned status {response.status_code}"
                )
            else:
                body = response.json()

                if body.get("status") != "confirmed":
                    response.failure("Order was not confirmed")
                elif not body.get("order_id", "").startswith("ORD-"):
                    response.failure("Order ID was missing or invalid")
                else:
                    response.success()