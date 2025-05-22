from locust import HttpUser, task, between
import random
import string
import os

class RecipeUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        """Sign up a new user and then log in to get a token"""
        self.email = self._generate_email()
        self.password = "test123"

        # Sign up
        self.client.post("/signUp", json={
            "email": self.email,
            "password": self.password
        })

        # Login
        response = self.client.post("/login", json={
            "email": self.email,
            "password": self.password
        })

        if response.status_code == 200:
            self.token = response.json().get("token")
        else:
            self.token = None
            print("Login failed")

    def _generate_email(self):
        return "user_" + ''.join(random.choices(string.ascii_lowercase, k=6)) + "@test.com"

    @task(1)
    def view_recipes(self):
        self.client.get("/recipe")

    @task(2)
    def add_recipe(self):
        if not self.token:
            return  # Skip if no token

        image_path = "test_image.png"  # Make sure this file exists
        if not os.path.exists(image_path):
            print(f"Image file {image_path} not found, skipping add_recipe")
            return

        with open(image_path, "rb") as image_file:
            files = {
                "file": ("test_image.png", image_file, "image/png"),
            }

            data = {
                "title": f"Locust Recipe {random.randint(1, 1000)}",
                "ingredients": "eggs, flour, sugar",
                "instructions": "Mix everything well and bake.",
                "time": "45 minutes"
            }

            headers = {
                "Authorization": f"Bearer {self.token}"
            }

            self.client.post(
                "/recipe",
                headers=headers,
                files=files,
                data=data,
                name="POST /recipe (add recipe)"
            )
