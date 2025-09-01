"""
Service for analyzing brand voice and generating content with a brand profile.

This is a lightweight implementation used to support the `/brand-voice` API.
It performs rudimentary analysis on text (counts words, sentences, emoji
usage, etc.) and returns structured information that can guide content
generation.  In a production system, you would replace this with a more
sophisticated NLP model.
"""

import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from services.seo_service import seo_service


class BrandVoiceAnalysisService:
    """Analyze text to extract brand voice characteristics and generate content."""

    def analyze_from_text_input(self, content: str, content_type: str = "mixed") -> dict:
        """Perform a simple analysis of the provided text.

        The analysis returns a dominant tone (professional vs. casual), a basic
        vocabulary level estimate, and SEO analysis.  It also includes a
        `brand_voice_strength` metric based on length and punctuation usage.
        """
        if not content or not content.strip():
            return {
                "dominant_tone": "neutral",
                "writing_style": "unknown",
                "personality_traits": [],
                "communication_preferences": {},
                "vocabulary_level": "unknown",
                "brand_voice_strength": 0,
                "seo": {"score": 0, "recommendations": ["Content is empty."]},
            }

        text = content.strip()
        words = re.findall(r"\b\w+\b", text)
        sentences = re.split(r"[.!?]", text)

        # Determine dominant tone: more exclamation marks -> energetic, more periods -> professional
        exclamations = text.count("!")
        questions = text.count("?")
        if exclamations > questions:
            dominant_tone = "energetic"
        elif questions > exclamations:
            dominant_tone = "inquisitive"
        else:
            dominant_tone = "professional"

        # Vocabulary level based on average word length
        avg_word_len = sum(len(w) for w in words) / len(words) if words else 0
        if avg_word_len > 6:
            vocab_level = "advanced"
        elif avg_word_len > 4:
            vocab_level = "intermediate"
        else:
            vocab_level = "basic"

        # Brand voice strength: normalize on number of sentences and punctuation
        strength = min(100, int(len(words) * 0.5 + exclamations * 5 + questions * 3))

        # SEO analysis using the existing service
        seo_result = seo_service.analyze_content(text)

        return {
            "dominant_tone": dominant_tone,
            "writing_style": "balanced" if len(sentences) <= 3 else "detailed",
            "personality_traits": [dominant_tone],
            "communication_preferences": {
                "uses_questions": questions > 0,
                "uses_exclamations": exclamations > 0,
                "uses_emojis": bool(re.search(r"[\U0001F600-\U0001F64F]", text)),
                "prefers_short_sentences": len(text.split()) < 50,
                "prefers_long_sentences": len(text.split()) > 100,
            },
            "vocabulary_level": vocab_level,
            "brand_voice_strength": strength,
            "seo": seo_result,
        }

    def generate_content_with_voice(
        self,
        prompt: str,
        brand_profile: Dict[str, any],
        content_type: str = "social_post",
    ) -> str:
        """Generate content using a simple brand profile and a prompt.

        This function appends information from the brand profile to the prompt
        to demonstrate how the voice might influence generation.  It is
        intentionally naive and should be replaced with proper language models
        in a production environment.
        """
        tone = brand_profile.get("dominant_tone", "professional")
        style = brand_profile.get("writing_style", "balanced")
        hashtags = brand_profile.get("hashtags", ["#RealEstate", "#Windsor"])
        generated = f"{prompt}\n\n(Tone: {tone}, Style: {style})"
        generated += "\n" + " ".join(hashtags)
        return generated

    def get_sample_profile(self) -> dict:
        """Return a default brand profile for demonstration purposes."""
        return {
            "dominant_tone": "professional",
            "writing_style": "balanced",
            "personality_traits": ["professional", "helpful", "knowledgeable"],
            "communication_preferences": {
                "uses_questions": True,
                "uses_exclamations": False,
                "uses_emojis": True,
                "prefers_short_sentences": False,
                "prefers_long_sentences": False,
            },
            "vocabulary_level": "professional",
            "brand_voice_strength": 75,
            "last_updated": datetime.utcnow().isoformat(),
        }


# Singleton instance
brand_voice_analysis_service = BrandVoiceAnalysisService()
