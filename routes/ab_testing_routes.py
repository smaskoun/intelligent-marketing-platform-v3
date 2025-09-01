"""
A/B testing routes.

Defines endpoints for creating A/B tests using the simplified
`ABTestingService`.  Clients can POST to `/api/ab-testing/create` with
a JSON body containing a `test_name` and `base_content` to receive a
test object with generated variations.
"""

from flask import Blueprint, jsonify, request
from services.ab_testing_service import ab_testing_service


ab_testing_bp = Blueprint("ab_testing", __name__)


@ab_testing_bp.route("/create", methods=["POST"])
def create_ab_test():
    """Create a new A/B test from the provided base content."""
    try:
        data = request.get_json() or {}
        if not data or "base_content" not in data:
            return jsonify({"success": False, "error": "Missing base_content in request."}), 400

        test_name = data.get("test_name", "New A/B Test")
        base_content = data["base_content"]

        test = ab_testing_service.create_test_variations(test_name, base_content)
        return jsonify({"success": True, "test": test})
    except Exception as exc:
        print(f"Error creating A/B test: {exc}")
        return jsonify({"success": False, "error": f"Failed to create A/B test: {exc}"}), 500
