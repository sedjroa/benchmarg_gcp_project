from locust import HttpUser, task, between
import random

class TinyInstaUser(HttpUser):
    wait_time = between(0.1, 1.0)

    users = [f"user{i}" for i in range(1000)]  # les 1000 users du seed

    @task
    def timeline(self):
        user = random.choice(self.users)
        self.client.get(f"/api/timeline?user={user}", name="/api/timeline")