"""
Routes for real‑estate market data.

Provides endpoints to retrieve current market statistics and simple
historical trends.  See `services.wecar_market_service` for the
implementation details.
"""

from flask import Blueprint, jsonify
from services.wecar_market_service import wecar_market_service


market_data_bp = Blueprint("market_data", __name__)


@market_data_bp.route("/current-stats", methods=["GET"])
def get_current_market_stats():
    """Return current Windsor‑Essex market statistics."""
    try:
        data = wecar_market_service.get_market_data()
        return jsonify({"success": True, "data": data, "source": "WECAR", "message": "Current market statistics retrieved successfully"})
    except Exception as exc:
        return jsonify({"success": False, "error": f"Failed to fetch market data: {exc}", "message": "Unable to retrieve current market statistics"}), 500


@market_data_bp.route("/market-trends", methods=["GET"])
def get_market_trends():
    """Return simplified market trends for the past six months."""
    try:
        trends = wecar_market_service.get_historical_trends()
        current_data = wecar_market_service.get_market_data()
        return jsonify({
            "success": True,
            "trends": trends,
            "current_period": current_data.get("report_period", "Current"),
            "insights": current_data.get("market_insights", {}),
            "source": "WECAR",
            "message": "Market trends retrieved successfully",
        })
    except Exception as exc:
        return jsonify({"success": False, "error": f"Failed to fetch market trends: {exc}", "message": "Unable to retrieve market trends"}), 500
