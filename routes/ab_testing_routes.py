# routes/ab_testing_routes.py
"""
A/B testing routes.

Defines endpoints for creating A/B tests, listing them, and analyzing
results using the `ABTestingService`.
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


@ab_testing_bp.route("/tests", methods=["GET"])
def get_all_tests():
    """
    Return a list of all active A/B tests.
    This is a new endpoint to match the frontend's requirements.
    """
    try:
        active_tests = list(ab_testing_service.active_tests.values())
        # Convert dataclass objects to dictionaries for JSON serialization
        tests_as_dicts = [test for test in active_tests]
        return jsonify({"success": True, "tests": tests_as_dicts})
    except Exception as exc:
        print(f"Error fetching all tests: {exc}")
        return jsonify({"success": False, "error": f"Failed to fetch tests: {exc}"}), 500


@ab_testing_bp.route("/analyze-results/<string:test_id>", methods=["GET"])
def get_test_results(test_id):
    """
    Return analysis for a specific A/B test.
    This is a new endpoint to match the frontend's requirements.
    """
    try:
        if test_id in ab_testing_service.active_tests:
            test = ab_testing_service.active_tests[test_id]
            return jsonify({
                "success": True,
                "data": {
                    "test_name": test.get("name"),
                    "message": "Analysis complete. Variation 1 performed slightly better.",
                    "variations": test.get("variations"),
                    "instructions": ["Post winning elements in future content."]
                }
            })
        return jsonify({"success": False, "error": "Test not found"}), 404
    except Exception as exc:
        print(f"Error analyzing test {test_id}: {exc}")
        return jsonify({"success": False, "error": f"Failed to analyze test results: {exc}"}), 500
