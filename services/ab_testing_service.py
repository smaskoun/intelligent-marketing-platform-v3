"""
Simplified A/B testing service.

This service allows creation of simple A/B tests by generating
variations from a base piece of content.  In a full implementation,
variations could alter hooks, call‑to‑action styles, emoji usage,
and hashtags.  For demonstration purposes the service below creates
two basic variations.
"""

from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
import uuid


@dataclass
class ABTestVariation:
    id: str
    content: str
    hashtags: List[str]
    image_prompt: str | None = None


@dataclass
class ABTest:
    id: str
    name: str
    content_type: str
    platform: str
    variations: List[ABTestVariation]
    status: str


class ABTestingService:
    """Service for creating and managing simple A/B tests."""

    def __init__(self) -> None:
        self.active_tests: Dict[str, ABTest] = {}

    def create_test_variations(self, test_name: str, base_content: Dict) -> Dict:
        """Generate a new A/B test with two basic variations."""
        test_id = str(uuid.uuid4())
        content_text = base_content.get("content", "")
        content_type = base_content.get("content_type", "general")
        platform = base_content.get("platform", "instagram")

        # Create two simple variations by appending suffixes
        variations: List[ABTestVariation] = []
        for i in range(2):
            variation_id = str(uuid.uuid4())
            variation_content = f"{content_text}\n\nVariation {i + 1}: try a different opening."
            hashtags = ["#Test", f"#{content_type}"]
            variations.append(
                ABTestVariation(id=variation_id, content=variation_content, hashtags=hashtags)
            )

        ab_test = ABTest(
            id=test_id,
            name=test_name,
            content_type=content_type,
            platform=platform,
            variations=variations,
            status="draft",
        )
        self.active_tests[test_id] = ab_test
        # Return serialisable structure
        return asdict(ab_test)


# Singleton instance
ab_testing_service = ABTestingService()
