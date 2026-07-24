import unittest
import os
import shutil
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
from backend.database.connection import Base, engine

client = TestClient(app)

class TestMember3Backend(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)

    def test_01_healthcheck(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())

    def test_02_chat_flow(self):
        # Create chat
        res = client.post("/chat/create", json={"username": "test_user", "title": "Test Chat"})
        self.assertEqual(res.status_code, 201)
        data = res.json()
        chat_id = data["id"]
        
        # Add message
        msg_res = client.post(f"/chat/{chat_id}/message?username=test_user", json={"role": "user", "content": "Hello"})
        self.assertEqual(msg_res.status_code, 201)
        
        # List chats
        list_res = client.get("/chat/list?username=test_user")
        self.assertEqual(list_res.status_code, 200)
        self.assertTrue(len(list_res.json()) >= 1)
        
        # Get single chat
        get_res = client.get(f"/chat/{chat_id}?username=test_user")
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(len(get_res.json()["messages"]), 1)
        
        # Delete chat
        del_res = client.delete(f"/chat/{chat_id}?username=test_user")
        self.assertEqual(del_res.status_code, 204)

    def test_03_dashboard(self):
        res = client.get("/dashboard/")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("total_chats", data)
        self.assertIn("total_messages", data)
        self.assertIn("total_uploaded_files", data)
        self.assertIn("total_documents_in_vector_db", data)

    def test_04_rag_retrieve_empty(self):
        res = client.post("/rag/retrieve", json={"query": "test query"})
        self.assertEqual(res.status_code, 200)
        self.assertIn("context", res.json())

if __name__ == "__main__":
    unittest.main()
