from aether import MeshApp

app = MeshApp("user-profile-service")

@app.route("/profile/{user_id}", traffic_split={"v1": 0.9, "v2": 0.1})
def get_profile(user_id):
    # Aether automatically injects headers for tracing here
    return {"status": "success", "id": user_id}