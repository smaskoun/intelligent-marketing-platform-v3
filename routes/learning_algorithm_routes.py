"""
Routes for content recommendation via the learning algorithm service.

Clients can call `/api/learning/content-recommendations` with query
parameters to receive suggested posts based on their training data and
selected content type.
"""

from flask import Blueprint, jsonify, request
from services.learning_algorithm_service import learning_algorithm_service


learning_algorithm_bp = Blueprint("learning_algorithm", __name__)


@learning_algorithm_bp.route("/content-recommendations", methods=["GET"])
def get_content_recommendations():
    """Return content recommendations based on user training data."""
    try:
        user_id = request.args.get("user_id", "default_user")
        content_type = request.args.get("type", "general")
        platform = request.args.get("platform", "instagram")
        result = learning_algorithm_service.generate_content_recommendations(
            user_id=user_id,
            content_type=content_type,
            platform=platform,
        )
        return jsonify(result)
    except Exception as exc:
        print(f"Error in content recommendations: {exc}")
        return jsonify({"success": False, "error": f"Failed to get content recommendations: {exc}"}), 500
