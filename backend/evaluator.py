"""
Evaluation System
Scores UI understanding quality and generated code readiness.
"""
from __future__ import annotations

from typing import Dict, List


class EvaluationEngine:
    """Computes practical quality metrics for a screenshot-to-code run."""

    def evaluate(
        self,
        components: List[Dict],
        text_elements: List[Dict],
        layout: Dict,
        hierarchy: Dict,
        generated_files: Dict[str, str],
    ) -> Dict:
        component_score = self._component_detection_score(components)
        ocr_score = self._ocr_score(text_elements)
        layout_score = self._layout_score(layout)
        visual_score = self._visual_similarity_proxy(components, hierarchy)
        code_score = self._code_quality_score(generated_files)

        overall = round(
            (
                component_score
                + ocr_score
                + layout_score
                + visual_score
                + code_score
            )
            / 5,
            3,
        )

        return {
            "component_detection_accuracy": component_score,
            "ocr_accuracy": ocr_score,
            "layout_reconstruction_accuracy": layout_score,
            "visual_similarity_score": visual_score,
            "code_quality_score": code_score,
            "overall_score": overall,
            "notes": [
                "Scores are heuristic unless ground-truth annotations are supplied.",
                "Visual similarity uses layout coverage and hierarchy richness as a proxy.",
            ],
        }

    def _component_detection_score(self, components: List[Dict]) -> float:
        if not components:
            return 0.0
        confidences = [float(item.get("confidence", 0.5)) for item in components]
        diversity = len({item.get("type", "unknown") for item in components})
        diversity_bonus = min(diversity / 8, 1) * 0.15
        return round(min(sum(confidences) / len(confidences) + diversity_bonus, 1), 3)

    def _ocr_score(self, text_elements: List[Dict]) -> float:
        if not text_elements:
            return 0.0
        confidences = [float(item.get("confidence", 0.75)) for item in text_elements]
        classified = sum(1 for item in text_elements if item.get("type") != "text")
        classification_bonus = (classified / len(text_elements)) * 0.15
        return round(min(sum(confidences) / len(confidences) + classification_bonus, 1), 3)

    def _layout_score(self, layout: Dict) -> float:
        if layout.get("type") in {"empty", None}:
            return 0.0
        score = 0.45
        if layout.get("rows"):
            score += 0.2
        if layout.get("grids"):
            score += 0.15
        if layout.get("spacing", {}).get("horizontal") or layout.get("spacing", {}).get("vertical"):
            score += 0.1
        if layout.get("alignment", {}).get("left_aligned") or layout.get("alignment", {}).get("top_aligned"):
            score += 0.1
        return round(min(score, 1), 3)

    def _visual_similarity_proxy(self, components: List[Dict], hierarchy: Dict) -> float:
        if not components:
            return 0.0
        node_count = self._count_nodes(hierarchy)
        hierarchy_ratio = min(node_count / max(len(components), 1), 1)
        typed_ratio = sum(1 for item in components if item.get("type") != "container") / len(components)
        return round((hierarchy_ratio * 0.5) + (typed_ratio * 0.5), 3)

    def _code_quality_score(self, generated_files: Dict[str, str]) -> float:
        if not generated_files:
            return 0.0
        expected = ["package.json", "styles/globals.css"]
        has_expected = sum(1 for name in expected if name in generated_files) / len(expected)
        has_components = any(path.startswith("components/") for path in generated_files)
        has_page = any(path in generated_files for path in ["App.jsx", "pages/index.js", "index.html"])
        score = 0.35 + (has_expected * 0.25) + (0.2 if has_components else 0) + (0.2 if has_page else 0)
        return round(min(score, 1), 3)

    def _count_nodes(self, node: Dict) -> int:
        return 1 + sum(self._count_nodes(child) for child in node.get("children", []))
