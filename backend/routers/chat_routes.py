"""FastAPI routes for chat history management."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.schemas.chat_schemas import ChatCreateRequest, ChatOut, MessageCreateRequest, MessageOut
from backend.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/create", response_model=ChatOut, status_code=status.HTTP_201_CREATED)
def create_chat(payload: ChatCreateRequest, db: Annotated[Session, Depends(get_db)]) -> ChatOut:
    """Create a new chat for the supplied username."""
    service = ChatService(db)
    chat = service.create_chat(payload.username, payload.title)
    return ChatOut(
        id=chat.id,
        user_id=chat.user_id,
        title=chat.title,
        created_at=chat.created_at,
        messages=[],
    )


@router.get("/list", response_model=list[ChatOut])
def list_chats(username: str, db: Annotated[Session, Depends(get_db)]) -> list[ChatOut]:
    """List all chats for the supplied username."""
    service = ChatService(db)
    chats = service.list_chats(username)
    return [
        ChatOut(
            id=chat.id,
            user_id=chat.user_id,
            title=chat.title,
            created_at=chat.created_at,
            messages=[
                MessageOut(id=message.id, role=message.role, content=message.content, timestamp=message.timestamp)
                for message in chat.messages
            ],
        )
        for chat in chats
    ]


@router.get("/{chat_id}", response_model=ChatOut)
def get_chat(chat_id: int, username: str, db: Annotated[Session, Depends(get_db)]) -> ChatOut:
    """Retrieve a single chat by id."""
    service = ChatService(db)
    chat = service.get_chat(chat_id, username)
    if chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")
    return ChatOut(
        id=chat.id,
        user_id=chat.user_id,
        title=chat.title,
        created_at=chat.created_at,
        messages=[
            MessageOut(id=message.id, role=message.role, content=message.content, timestamp=message.timestamp)
            for message in chat.messages
        ],
    )


@router.post("/{chat_id}/message", response_model=MessageOut, status_code=status.HTTP_201_CREATED)
def add_message(chat_id: int, payload: MessageCreateRequest, username: str, db: Annotated[Session, Depends(get_db)]) -> MessageOut:
    """Add a message into an existing chat."""
    service = ChatService(db)
    try:
        message = service.add_message(chat_id, payload.role, payload.content, username)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return MessageOut(id=message.id, role=message.role, content=message.content, timestamp=message.timestamp)


@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chat(chat_id: int, username: str, db: Annotated[Session, Depends(get_db)]) -> Response:
    """Delete a chat owned by the specified username."""
    service = ChatService(db)
    deleted = service.delete_chat(chat_id, username)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
