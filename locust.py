from locust import HttpUser, task, between, events
import csv
import os
import statistics
import time
import random

CSV_FILE = "out/fanout.csv"

# --------------------------
# INIT CSV (si pas encore créé)
# --------------------------
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["PARAM", "AVG_TIME", "RUN", "FAILED"])

# --------------------------
# Variables temporaire pour un test
# --------------------------
latencies = []
failures = 0


# RESET AU DÉMARRAGE DU TEST
@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    global latencies, failures
    latencies = []
    failures = 0
    print(">>> Test démarré – Compteurs réinitialisés.")


# NOUVEL EVENT (Locust 2.16+) pour succès ET échec
@events.request.add_listener
def on_request(
    request_type,
    name,
    response_time,
    response_length,
    exception,
    context,
    **kwargs
):
    global latencies, failures

    if exception is None:
        # REQUÊTE RÉUSSIE
        latencies.append(response_time)
    else:
        # REQUÊTE ÉCHOUÉE
        failures += 1


# ENREGISTREMENT CSV À LA FIN DU TEST
@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    global latencies, failures

    # Nombre d'utilisateurs simultanés
    param = environment.runner.target_user_count

    # Temps moyen
    avg_time = statistics.mean(latencies) if latencies else 0

    # Déterminer le numéro de RUN pour ce paramètre
    existing_runs = 0
    with open(CSV_FILE, "r") as f:
        for line in f:
            if line.startswith(str(param) + ","):
                existing_runs += 1

    run_number = existing_runs + 1

    # Ajouter la ligne au CSV
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([param, round(avg_time, 3), run_number, failures])

    print(f">>> Résultat enregistré: PARAM={param}, AVG={avg_time}, RUN={run_number}, FAILED={failures}")


# --------------------------
# UTILISATEUR LOCUST
# --------------------------
class TinyInstaUser(HttpUser):
    wait_time = between(0.1, 0.5)
    users = [f"user{i}" for i in range(1000)]

    @task
    def get_timeline(self):
        user = random.choice(self.users)
        self.client.get(f"/api/timeline?user={user}", name="/api/timeline")
