"""
Database models related to social media content.

This module defines the `TrainingData` model used to store examples
of user content.  It imports the shared `db` instance from
`models.__init__` rather than creating a new one.
"""

from datetime import datetime

from . import db


class TrainingData(db.Model):
    """Represents a single piece of content provided by the user.

    This model stores content that will be used to train the brand
    voice analysis and generation algorithms.  Each record tracks
    which user provided the content, the text itself, an optional
    image URL, the type of post, and when it was created.
    """

    __tablename__ = "training_data"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(2048), nullable=True)
    post_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<TrainingData {self.id} for user {self.user_id}>"

    def to_dict(self) -> dict:
        """Return a JSON‑serialisable representation of this record."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "content": self.content,
            "image_url": self.image_url,
            "post_type": self.post_type,
            "created_at": self.created_at.isoformat(),
        }
