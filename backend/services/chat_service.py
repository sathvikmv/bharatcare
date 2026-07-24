"""Service layer for chat history CRUD operations."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy.orm import Session

from backend.database.models import Chat, Message, User


class ChatService:
    """Business logic for creating and reading chat conversations."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_or_create_user(self, username: str) -> User:
        """Return an existing user or create one with the given username."""
        user = self.db.query(User).filter(User.username == username).first()
        if user is None:
            user = User(username=username)
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
        return user

    def create_chat(self, username: str, title: Optional[str] = None) -> Chat:
        """Create a new chat for the supplied username."""
        user = self.get_or_create_user(username)
        chat = Chat(user_id=user.id, title=title or "New Chat")
        self.db.add(chat)
        self.db.commit()
        self.db.refresh(chat)
        return chat

    def list_chats(self, username: str) -> List[Chat]:
        """List all chats for a given user."""
        user = self.get_or_create_user(username)
        return self.db.query(Chat).filter(Chat.user_id == user.id).order_by(Chat.created_at.desc()).all()

    def get_chat(self, chat_id: int, username: str) -> Optional[Chat]:
        """Retrieve a specific chat for a user."""
        user = self.get_or_create_user(username)
        return (
            self.db.query(Chat)
            .filter(Chat.id == chat_id, Chat.user_id == user.id)
            .first()
        )

    def add_message(self, chat_id: int, role: str, content: str, username: str) -> Message:
        """Append a message to a chat and return the created message."""
        chat = self.get_chat(chat_id, username)
        if chat is None:
            raise ValueError("Chat not found")

        message = Message(chat_id=chat.id, role=role, content=content, timestamp=datetime.now(timezone.utc))
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def delete_chat(self, chat_id: int, username: str) -> bool:
        """Delete a chat owned by the specified user."""
        chat = self.get_chat(chat_id, username)
        if chat is None:
            return False

        self.db.delete(chat)
        self.db.commit()
        return True
