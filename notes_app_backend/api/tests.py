from rest_framework.test import APITestCase
from django.urls import reverse


class HealthTests(APITestCase):
    def test_health(self):
        url = reverse('Health')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"message": "Server is up!"})


class NotesFlowTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('Register')
        self.login_url = reverse('Login')

    def test_register_login_and_notes_crud_smoke(self):
        # Register
        r = self.client.post(self.register_url, {"username": "alice", "password": "SuperSecret123!"}, format="json")
        self.assertIn(r.status_code, [200, 201])
        token = r.data.get("token")
        self.assertTrue(token)

        # Login
        r2 = self.client.post(self.login_url, {"username": "alice", "password": "SuperSecret123!"}, format="json")
        self.assertEqual(r2.status_code, 200)
        token2 = r2.data.get("token")
        self.assertTrue(token2)

        # Auth header
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token2}")

        # Create note
        create_resp = self.client.post("/api/notes/", {"title": "Test", "content": "Body"}, format="json")
        self.assertEqual(create_resp.status_code, 201)
        nid = create_resp.data["id"]

        # List notes
        list_resp = self.client.get("/api/notes/?q=Test")
        self.assertEqual(list_resp.status_code, 200)
        self.assertGreaterEqual(len(list_resp.data.get("results", [])), 1)

        # Retrieve
        get_resp = self.client.get(f"/api/notes/{nid}/")
        self.assertEqual(get_resp.status_code, 200)

        # Update
        put_resp = self.client.put(f"/api/notes/{nid}/", {"title": "Updated", "content": "Body2"}, format="json")
        self.assertEqual(put_resp.status_code, 200)
        self.assertEqual(put_resp.data["title"], "Updated")

        # Delete
        del_resp = self.client.delete(f"/api/notes/{nid}/")
        self.assertIn(del_resp.status_code, [200, 204])
