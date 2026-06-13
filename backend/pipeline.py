"""
UI2CODE screenshot understanding pipeline.

Coordinates visual detection, OCR semantics, layout intelligence, design-system
extraction, hierarchy generation, AI reasoning, code generation, and evaluation.
"""
from __future__ import annotations

import os
from typing import Dict

import cv2

from ai_reasoner import AIReasoner
from code_gen_engine import CodeGenerator
from config import Config
from design_extractor import DesignExtractor
from evaluator import EvaluationEngine
from hierarchy_builder import HierarchyBuilder
from layout_analyzer import LayoutAnalyzer
from ocr_engine import OCREngine
from vision_detector import VisionDetector


class UI2CodePipeline:
    """End-to-end production pipeline for understanding UI screenshots."""

    def __init__(self):
        self.detector = VisionDetector(Config.YOLO_MODEL_PATH)
        self.ocr = OCREngine(["en"])
        self.layout_analyzer = LayoutAnalyzer()
        self.design_extractor = DesignExtractor()
        self.hierarchy_builder = HierarchyBuilder()
        self.reasoner = AIReasoner(Config.OPENAI_API_KEY)
        self.evaluator = EvaluationEngine()

    def analyze(
        self,
        image_path: str,
        framework: str = "nextjs",
        styling: str = "tailwind",
    ) -> Dict:
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image: {image_path}")

        image_height, image_width = image.shape[:2]

        components = self.detector.detect_components(image_path)
        text_elements = self.ocr.extract_text(image_path)
        components = self.ocr.merge_with_components(text_elements, components)

        layout = self.layout_analyzer.analyze_layout(components, image_width, image_height)
        design_system = self.design_extractor.extract_design_system(
            image_path,
            components,
            text_elements,
        )
        hierarchy = self.hierarchy_builder.build_hierarchy(components, layout, text_elements)
        reasoned_hierarchy = self.reasoner.reason_about_components(
            hierarchy,
            design_system,
            layout,
        )

        generator = CodeGenerator(framework=framework, styling=styling)
        generated_files = generator.generate_code(reasoned_hierarchy, design_system, layout)

        evaluation = self.evaluator.evaluate(
            components,
            text_elements,
            layout,
            reasoned_hierarchy,
            generated_files,
        )

        return {
            "image": {
                "filename": os.path.basename(image_path),
                "width": image_width,
                "height": image_height,
            },
            "visual_understanding": {
                "components": components,
                "component_count": len(components),
                "component_types": sorted({item.get("type", "unknown") for item in components}),
            },
            "ocr_semantics": {
                "text_elements": text_elements,
                "semantic_structure": self.ocr.extract_semantic_structure(text_elements),
            },
            "layout_intelligence": layout,
            "design_system": design_system,
            "component_hierarchy": reasoned_hierarchy,
            "generated_project": {
                "framework": framework,
                "styling": styling,
                "structure": [
                    "project/",
                    "  components/",
                    "  pages/",
                    "  styles/",
                    "  assets/",
                ],
                "files": generated_files,
            },
            "evaluation": evaluation,
            "future_features": [
                "Figma to code",
                "Sketch to code",
                "Hand-drawn wireframe to code",
                "Design improvement suggestions",
                "Automatic accessibility fixes",
                "Multi-page application generation",
                "Design system generation",
                "Component library creation",
            ],
        }
