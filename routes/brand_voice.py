"""
Brand voice routes.

This module defines endpoints to train and analyze a user's brand voice
and to generate content using that voice.  Analysis is handled by
`services.brand_voice_analysis_service`, while training data is stored
via `services.brand_voice_service`.
"""

from flask import Blueprint, jsonify, request
from services.brand_voice_service import brand_voice_service
from services.brand_voice_analysis_service import brand_voice_analysis_service


brand_voice_bp = Blueprint("brand_voice", __name__)


@brand_voice_bp.route("/train", methods=["POST"])
def train_brand_voice():
    """Accept training data for brand voice analysis."""
    data = request.get_json() or {}
    required_fields = {"user_id", "content", "post_type"}
    missing = required_fields - data.keys()
    if missing:
        return jsonify({"success": False, "error": f"Missing fields: {', '.join(sorted(missing))}"}), 400
    user_id = data["user_id"]
    content = data["content"]
    image_url = data.get("image_url")
    post_type = data["post_type"]
    try:
        new_entry = brand_voice_service.add_training_data(user_id, content, image_url, post_type)
        return jsonify({"success": True, "data": new_entry.to_dict(), "message": "Training data added successfully"})
    except Exception as exc:
        return jsonify({"success": False, "error": f"Failed to add training data: {exc}"}), 500


@brand_voice_bp.route("/analyze-text", methods=["POST"])
def analyze_text_content():
    """Analyze brand voice from manually provided text content."""
    try:
        data = request.get_json() or {}
        if not data or "content" not in data:
            return jsonify({"success": False, "error": "Content is required"}), 400
        content = data["content"]
        content_type = data.get("content_type", "mixed")
        analysis_result = brand_voice_analysis_service.analyze_from_text_input(content, content_type)
        return jsonify({"success": True, "data": analysis_result, "message": "Brand voice analysis completed successfully"})
    except Exception as exc:
        return jsonify({"success": False, "error": f"Analysis failed: {exc}"}), 500


@brand_voice_bp.route("/voice-profile", methods=["GET"])
def get_voice_profile():
    """Return a sample brand voice profile."""
    try:
        profile = brand_voice_analysis_service.get_sample_profile()
        return jsonify({"success": True, "data": profile, "message": "Voice profile retrieved successfully"})
    except Exception as exc:
        return jsonify({"success": False, "error": f"Failed to retrieve voice profile: {exc}"}), 500


@brand_voice_bp.route("/generate-content", methods=["POST"])
def generate_content_with_voice():
    """Generate content using the analyzed brand voice."""
    try:
        data = request.get_json() or {}
        if not data or "prompt" not in data:
            return jsonify({"success": False, "error": "Prompt is required"}), 400
        prompt = data["prompt"]
        content_type = data.get("content_type", "social_post")
        brand_profile = data.get("brand_profile", brand_voice_analysis_service.get_sample_profile())
        generated = brand_voice_analysis_service.generate_content_with_voice(prompt, brand_profile, content_type)
        return jsonify({"success": True, "data": {"generated_content": generated, "prompt": prompt, "content_type": content_type, "brand_profile_used": brand_profile}, "message": "Content generated successfully with brand voice"})
    except Exception as exc:
        return jsonify({"success": False, "error": f"Content generation failed: {exc}"}), 500


@brand_voice_bp.route("/sample-analysis", methods=["GET"])
def get_sample_analysis():
    """Return a sample analysis for demonstration."""
    try:
        sample_content = (
            "Just listed! Beautiful 3‑bedroom home in Windsor‑Essex with stunning curb appeal and move‑in ready condition. "
            "\n\nThis property features an open‑concept layout, updated kitchen, and spacious backyard perfect for entertaining. "
            "Located in a quiet neighborhood with excellent schools nearby.\n\nThinking of buying or selling? I'm here to help guide you through every step of the process. "
            "With over 10 years of experience in the Windsor‑Essex market, I provide personalised service and expert advice.\n\n"
            "Ready to find your dream home? Let's chat! Send me a DM or call today. ✨\n\n"
            "#WindsorEssexRealEstate #DreamHome #RealEstateExpert #HomeBuying #PropertyListing"
        )
        analysis_result = brand_voice_analysis_service.analyze_from_text_input(sample_content, "posts")
        return jsonify({"success": True, "data": analysis_result, "message": "Sample analysis completed successfully", "note": "This is a sample analysis. Upload your own content for personalised results."})
    except Exception as exc:
        return jsonify({"success": False, "error": f"Sample analysis failed: {exc}"}), 500


@brand_voice_bp.route("/upload-content", methods=["POST"])
def upload_content_file():
    """Upload and analyze content from a text file."""
    try:
        if 'file' not in request.files:
            return jsonify({"success": False, "error": "No file uploaded"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"success": False, "error": "No file selected"}), 400
        if not file.filename.lower().endswith('.txt'):
            return jsonify({"success": False, "error": "Only .txt files are supported"}), 400
        content = file.read().decode('utf-8')
        content_type = request.form.get('content_type', 'mixed')
        analysis_result = brand_voice_analysis_service.analyze_from_text_input(content, content_type)
        return jsonify({"success": True, "data": analysis_result, "message": "Content file analysed successfully"})
    except Exception as exc:
        return jsonify({"success": False, "error": f"File analysis failed: {exc}"}), 500
