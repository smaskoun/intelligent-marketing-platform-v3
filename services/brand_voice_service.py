"""
Service to manage training data for brand voice.

This service creates new training examples in the database.  It does not
perform analysis; see `brand_voice_analysis_service` for analysis.
"""

from models.social_media import TrainingData, db


class BrandVoiceService:
    """Handles persistence of brand voice training data."""

    def add_training_data(
        self, user_id: str, content: str, image_url: str | None, post_type: str
    ) -> TrainingData:
        """Create a new training data entry and save it to the database."""
        try:
            new_entry = TrainingData(
                user_id=user_id,
                content=content,
                image_url=image_url,
                post_type=post_type,
            )
            db.session.add(new_entry)
            db.session.commit()
            return new_entry
        except Exception as e:
            db.session.rollback()
            print(f"Database error in BrandVoiceService: {e}")
            raise e


# Singleton instance
brand_voice_service = BrandVoiceService()
