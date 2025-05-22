from locust import HttpUser, task, between
import random
import string
import os

class RecipeUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        """Signup a new user and then log in"""
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
            return

        with open("test_image.png", "rb") as image_file:
            files = {
                "title": (None, f"Locust Recipe {random.randint(1,100)}"),
                "ingredients": (None, "eggs, flour, sugar"),
                "instructions": (None, "Mix and bake for 30 minutes"),
                "time": (None, "30"),
                "coverImage": ("test_image.png", image_file, "image/png")
            }

            headers = {
                "Authorization": f"Bearer {self.token}"
            }

            self.client.post("/recipe", files=files, headers=headers)
