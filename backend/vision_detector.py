"""
Visual Understanding Layer - Component Detection using YOLO and Detectron2
"""
import os
from typing import Dict, List

import cv2
import numpy as np

class VisionDetector:
    """
    Detects UI components using Computer Vision models
    Supports: buttons, text blocks, images, cards, forms, navbars, etc.
    """
    
    def __init__(self, model_path: str = None):
        """Initialize an optional UI-specific YOLO model."""
        self.model_path = model_path
        self.model = None

        if model_path and os.path.exists(model_path):
            try:
                from ultralytics import YOLO

                self.model = YOLO(model_path)
            except Exception as e:
                print(f"Warning: Could not load YOLO model: {e}")
        
        self.component_classes = [
            'button', 'text', 'image', 'card', 'form', 'input',
            'navbar', 'sidebar', 'icon', 'container', 'table',
            'menu', 'header', 'footer', 'modal', 'dropdown'
        ]
    
    def detect_components(self, image_path: str) -> List[Dict]:
        """
        Detect UI components in the image
        
        Returns:
            List of detected components with bounding boxes and types
        """
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image: {image_path}")
        
        height, width = image.shape[:2]
        
        if self.model:
            results = self.model(image)
            components = self._parse_yolo_results(results, width, height)
        else:
            components = self._fallback_detection(image, width, height)
        
        return components
    
    def _parse_yolo_results(self, results, width: int, height: int) -> List[Dict]:
        """Parse YOLO detection results"""
        components = []
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                conf = float(box.conf[0])
                cls = int(box.cls[0])
                
                component = {
                    'type': self._map_class_to_component(cls),
                    'bbox': {
                        'x': int(x1),
                        'y': int(y1),
                        'width': int(x2 - x1),
                        'height': int(y2 - y1)
                    },
                    'confidence': conf,
                    'center': {
                        'x': int((x1 + x2) / 2),
                        'y': int((y1 + y2) / 2)
                    }
                }
                components.append(component)
        
        return components
    
    def _fallback_detection(self, image: np.ndarray, width: int, height: int) -> List[Dict]:
        """
        Fallback detection using traditional CV methods
        Detects rectangular regions that could be UI components
        """
        components = []
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        edges = cv2.Canny(blurred, 40, 130)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            area = w * h
            
            # Filter small components
            if area < 100 or w < 10 or h < 10:
                continue
            
            component_type = self._classify_by_shape(x, y, w, h, area, width, height)
            
            component = {
                'type': component_type,
                'bbox': {
                    'x': int(x),
                    'y': int(y),
                    'width': int(w),
                    'height': int(h)
                },
                'confidence': 0.7,
                'center': {
                    'x': int(x + w/2),
                    'y': int(y + h/2)
                }
            }
            components.append(component)
        
        components = self._merge_overlapping(components)
        components = self._infer_large_regions(components, width, height)
        
        return components
    
    def _classify_by_shape(self, x: int, y: int, w: int, h: int, area: int, img_w: int, img_h: int) -> str:
        """Classify component based on shape and size"""
        aspect_ratio = w / h if h > 0 else 1
        relative_width = w / img_w
        relative_height = h / img_h
        relative_area = area / (img_w * img_h)
        
        if relative_width > 0.75 and relative_height < 0.16 and y < img_h * 0.2:
            return 'navbar'

        if relative_height > 0.5 and relative_width < 0.28 and x < img_w * 0.12:
            return 'sidebar'
        
        if 2 < aspect_ratio < 8 and relative_area < 0.045 and h < img_h * 0.12:
            return 'button'
        
        if 0.55 < aspect_ratio < 2.8 and 0.025 < relative_area < 0.28:
            return 'card'
        
        if 0.7 < aspect_ratio < 1.7 and relative_area > 0.01:
            return 'image'
        
        if aspect_ratio > 3 and h < img_h * 0.08:
            return 'text'
        
        return 'container'

    def _infer_large_regions(self, components: List[Dict], width: int, height: int) -> List[Dict]:
        """Add high-level semantic regions that contour detection can miss."""
        inferred = list(components)

        has_navbar = any(item["type"] == "navbar" for item in inferred)
        if not has_navbar:
            top_components = [
                item for item in inferred
                if item["bbox"]["y"] < height * 0.18 and item["bbox"]["width"] > width * 0.08
            ]
            if len(top_components) >= 2:
                inferred.append({
                    "type": "navbar",
                    "bbox": {"x": 0, "y": 0, "width": width, "height": int(height * 0.12)},
                    "confidence": 0.62,
                    "center": {"x": width // 2, "y": int(height * 0.06)},
                })

        main_components = [
            item for item in inferred
            if item["bbox"]["y"] > height * 0.12 and item["bbox"]["height"] > 12
        ]
        if main_components:
            x1 = min(item["bbox"]["x"] for item in main_components)
            y1 = min(item["bbox"]["y"] for item in main_components)
            x2 = max(item["bbox"]["x"] + item["bbox"]["width"] for item in main_components)
            y2 = max(item["bbox"]["y"] + item["bbox"]["height"] for item in main_components)
            inferred.append({
                "type": "container",
                "bbox": {"x": x1, "y": y1, "width": x2 - x1, "height": y2 - y1},
                "confidence": 0.58,
                "center": {"x": (x1 + x2) // 2, "y": (y1 + y2) // 2},
            })

        return inferred
    
    def _merge_overlapping(self, components: List[Dict], threshold: float = 0.5) -> List[Dict]:
        """Merge overlapping components"""
        if len(components) <= 1:
            return components
        
        merged = []
        used = set()
        
        for i, comp1 in enumerate(components):
            if i in used:
                continue
            
            current = comp1.copy()
            for j, comp2 in enumerate(components[i+1:], i+1):
                if j in used:
                    continue
                
                iou = self._calculate_iou(comp1['bbox'], comp2['bbox'])
                if iou > threshold:
                    # Merge bounding boxes
                    current = self._merge_boxes(current, comp2)
                    used.add(j)
            
            merged.append(current)
            used.add(i)
        
        return merged
    
    def _calculate_iou(self, box1: Dict, box2: Dict) -> float:
        """Calculate Intersection over Union"""
        x1 = max(box1['x'], box2['x'])
        y1 = max(box1['y'], box2['y'])
        x2 = min(box1['x'] + box1['width'], box2['x'] + box2['width'])
        y2 = min(box1['y'] + box1['height'], box2['y'] + box2['height'])
        
        if x2 < x1 or y2 < y1:
            return 0.0
        
        intersection = (x2 - x1) * (y2 - y1)
        area1 = box1['width'] * box1['height']
        area2 = box2['width'] * box2['height']
        union = area1 + area2 - intersection
        
        return intersection / union if union > 0 else 0
    
    def _merge_boxes(self, comp1: Dict, comp2: Dict) -> Dict:
        """Merge two component boxes"""
        x1 = min(comp1['bbox']['x'], comp2['bbox']['x'])
        y1 = min(comp1['bbox']['y'], comp2['bbox']['y'])
        x2 = max(comp1['bbox']['x'] + comp1['bbox']['width'], 
                 comp2['bbox']['x'] + comp2['bbox']['width'])
        y2 = max(comp1['bbox']['y'] + comp1['bbox']['height'],
                 comp2['bbox']['y'] + comp2['bbox']['height'])
        
        return {
            'type': comp1['type'],
            'bbox': {
                'x': x1,
                'y': y1,
                'width': x2 - x1,
                'height': y2 - y1
            },
            'confidence': max(comp1['confidence'], comp2['confidence']),
            'center': {
                'x': (x1 + x2) // 2,
                'y': (y1 + y2) // 2
            }
        }
    
    def _map_class_to_component(self, cls: int) -> str:
        """Map YOLO class index to component type"""
        if cls < len(self.component_classes):
            return self.component_classes[cls]
        return 'container'
    
    def visualize_detections(self, image_path: str, components: List[Dict], output_path: str):
        """Draw bounding boxes on image for visualization"""
        image = cv2.imread(image_path)
        
        colors = {
            'button': (0, 255, 0),
            'text': (255, 0, 0),
            'image': (0, 0, 255),
            'card': (255, 255, 0),
            'navbar': (255, 0, 255),
            'container': (128, 128, 128)
        }
        
        for comp in components:
            bbox = comp['bbox']
            color = colors.get(comp['type'], (255, 255, 255))
            
            cv2.rectangle(image, 
                         (bbox['x'], bbox['y']),
                         (bbox['x'] + bbox['width'], bbox['y'] + bbox['height']),
                         color, 2)
            
            label = f"{comp['type']} ({comp['confidence']:.2f})"
            cv2.putText(image, label, 
                       (bbox['x'], bbox['y'] - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        cv2.imwrite(output_path, image)
