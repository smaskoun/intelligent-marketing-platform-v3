"""
Service for generating content recommendations.

This service reads the user's training data from the database and
generates simple content recommendations while invoking the SEO
analysis service to score the generated content.
"""

import random

from models.social_media import TrainingData, db
from services.seo_service import seo_service


class LearningAlgorithmService:
    """Service for generating new, SEO‑optimized content recommendations."""

    def generate_content_recommendations(
        self, user_id: str, content_type: str, platform: str
    ) -> dict:
        """Generate content recommendations based on a topic and learned brand voice."""
        # Fetch training examples for the specific user and content type
        training_examples = (
            TrainingData.query.filter_by(user_id=user_id, post_type=content_type)
            .limit(10)
            .all()
        )

        # If no data, return a helpful error
        if not training_examples:
            return {
                "success": False,
                "error": f"No training data found for '{content_type}'. Please add examples first.",
            }

        recommendations = []

        # Generate three recommendations
        for i in range(3):
            base_example = random.choice(training_examples)
            focus = f"Variation {i + 1} based on your '{base_example.post_type}' style"
            topic = f"A new post about {content_type.replace('_', ' ')}"
            new_content = f"{topic}.\n\n(Inspired by your post: '{base_example.content[:50]}...')"
            seo_analysis = seo_service.analyze_content(new_content)

            recommendations.append(
                {
                    "content": new_content,
                    "focus": focus,
                    "hashtags": ["#WindsorRealEstate", f"#{content_type}"],
                    "seo_score": seo_analysis.get("score"),
                    "seo_recommendations": seo_analysis.get("recommendations"),
                }
            )

        return {"success": True, "recommendations": recommendations}


# Create a singleton instance
learning_algorithm_service = LearningAlgorithmService()
