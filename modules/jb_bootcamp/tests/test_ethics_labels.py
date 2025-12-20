"""Additional coverage for human-readable ethical labels."""

from jb_bootcamp.ethics import ethic_evaluation


def test_low_risk_labels_map_to_compliant_status():
    result = ethic_evaluation({"safety": "Low"})
    assert result.overall_score == 0.9
    assert result.status == "compliant"


def test_medium_risk_labels_map_to_review_status():
    result = ethic_evaluation({"privacy": "Medium"})
    assert result.overall_score == 0.7
    assert result.status == "needs_review"


def test_high_risk_labels_map_to_non_compliant_status():
    result = ethic_evaluation({"impact": "High"})
    assert result.overall_score == 0.35
    assert result.status == "non_compliant"
