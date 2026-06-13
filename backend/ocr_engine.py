"""
OCR & Semantic Understanding Layer
Extracts text and classifies its purpose
"""
import cv2
import numpy as np
from typing import List, Dict, Tuple
import re

class OCREngine:
    """
    Extract text from UI screenshots and understand semantic meaning
    """
    
    def __init__(self, languages: List[str] = ['en']):
        """Initialize OCR reader"""
        self.reader = None
        try:
            import easyocr

            self.reader = easyocr.Reader(languages, gpu=False)
        except Exception as e:
            print(f"Warning: OCR engine unavailable: {e}")
        
        # Text classification patterns
        self.patterns = {
            'heading': [
                r'^[A-Z][A-Za-z\s]{3,50}$',
                r'^\d+\.\s+[A-Z]',
            ],
            'button_text': [
                r'^(Get|Start|Sign|Log|Click|Submit|Send|Buy|Learn|Try|Download|Upload)',
                r'^[A-Z][a-z]+(\s[A-Z][a-z]+){0,3}$',
            ],
            'menu_item': [
                r'^(Home|About|Services|Products|Contact|Blog|Features|Pricing|FAQ)',
            ],
            'form_label': [
                r'^(Name|Email|Password|Phone|Address|Message|Subject):?$',
                r'^\w+:$',
            ],
            'link': [
                r'^(Learn more|Read more|View all|See details)',
            ]
        }
    
    def extract_text(self, image_path: str) -> List[Dict]:
        """
        Extract all text from image with bounding boxes
        
        Returns:
            List of text elements with position and classification
        """
        if self.reader is None:
            return []

        results = self.reader.readtext(image_path)
        
        text_elements = []
        for bbox, text, confidence in results:
            # Clean text
            text = text.strip()
            if len(text) < 2:
                continue
            
            # Get bounding box coordinates
            x_coords = [point[0] for point in bbox]
            y_coords = [point[1] for point in bbox]
            
            x = int(min(x_coords))
            y = int(min(y_coords))
            width = int(max(x_coords) - x)
            height = int(max(y_coords) - y)
            
            # Classify text type
            text_type = self._classify_text(text, width, height)
            
            element = {
                'text': text,
                'type': text_type,
                'bbox': {
                    'x': x,
                    'y': y,
                    'width': width,
                    'height': height
                },
                'confidence': confidence,
                'font_size': self._estimate_font_size(height),
                'center': {
                    'x': x + width // 2,
                    'y': y + height // 2
                }
            }
            
            text_elements.append(element)
        
        # Sort by vertical position (top to bottom)
        text_elements.sort(key=lambda x: x['bbox']['y'])
        
        return text_elements
    
    def _classify_text(self, text: str, width: int, height: int) -> str:
        """
        Classify text based on content and visual properties
        """
        # Check patterns
        for text_type, patterns in self.patterns.items():
            for pattern in patterns:
                if re.match(pattern, text, re.IGNORECASE):
                    return text_type
        
        # Classify by visual properties
        aspect_ratio = width / height if height > 0 else 1
        
        # Large text = heading
        if height > 30:
            return 'heading'
        
        # Medium text = subheading
        if height > 20:
            return 'subheading'
        
        # Short text in button-like shape
        if len(text.split()) <= 3 and 2 < aspect_ratio < 8:
            return 'button_text'
        
        # Long text = paragraph
        if len(text.split()) > 10:
            return 'paragraph'
        
        # Default
        return 'text'
    
    def _estimate_font_size(self, height: int) -> int:
        """Estimate font size from text height"""
        # Rough estimation: height in pixels to font size in pt
        return max(8, int(height * 0.75))
    
    def extract_semantic_structure(self, text_elements: List[Dict]) -> Dict:
        """
        Understand the semantic structure of the page
        Group related text elements
        """
        structure = {
            'headings': [],
            'subheadings': [],
            'paragraphs': [],
            'buttons': [],
            'menu_items': [],
            'form_labels': [],
            'links': []
        }
        
        for element in text_elements:
            text_type = element['type']
            
            if text_type == 'heading':
                structure['headings'].append(element)
            elif text_type == 'subheading':
                structure['subheadings'].append(element)
            elif text_type == 'paragraph':
                structure['paragraphs'].append(element)
            elif text_type == 'button_text':
                structure['buttons'].append(element)
            elif text_type == 'menu_item':
                structure['menu_items'].append(element)
            elif text_type == 'form_label':
                structure['form_labels'].append(element)
            elif text_type == 'link':
                structure['links'].append(element)
        
        return structure
    
    def merge_with_components(self, text_elements: List[Dict], 
                             components: List[Dict]) -> List[Dict]:
        """
        Merge text elements with detected visual components
        """
        for component in components:
            comp_bbox = component['bbox']
            component['text_content'] = []
            
            for text_elem in text_elements:
                text_bbox = text_elem['bbox']
                
                # Check if text is inside component
                if self._is_inside(text_bbox, comp_bbox):
                    component['text_content'].append(text_elem)
        
        return components
    
    def _is_inside(self, inner_bbox: Dict, outer_bbox: Dict, 
                   threshold: float = 0.8) -> bool:
        """Check if inner bbox is inside outer bbox"""
        inner_x1 = inner_bbox['x']
        inner_y1 = inner_bbox['y']
        inner_x2 = inner_x1 + inner_bbox['width']
        inner_y2 = inner_y1 + inner_bbox['height']
        
        outer_x1 = outer_bbox['x']
        outer_y1 = outer_bbox['y']
        outer_x2 = outer_x1 + outer_bbox['width']
        outer_y2 = outer_y1 + outer_bbox['height']
        
        # Calculate overlap
        x_overlap = max(0, min(inner_x2, outer_x2) - max(inner_x1, outer_x1))
        y_overlap = max(0, min(inner_y2, outer_y2) - max(inner_y1, outer_y1))
        
        overlap_area = x_overlap * y_overlap
        inner_area = inner_bbox['width'] * inner_bbox['height']
        
        return (overlap_area / inner_area) >= threshold if inner_area > 0 else False
    
    def visualize_text(self, image_path: str, text_elements: List[Dict], 
                      output_path: str):
        """Draw text bounding boxes on image"""
        image = cv2.imread(image_path)
        
        colors = {
            'heading': (255, 0, 0),
            'subheading': (0, 255, 0),
            'button_text': (0, 0, 255),
            'paragraph': (255, 255, 0),
            'menu_item': (255, 0, 255),
            'form_label': (0, 255, 255)
        }
        
        for elem in text_elements:
            bbox = elem['bbox']
            color = colors.get(elem['type'], (128, 128, 128))
            
            cv2.rectangle(image,
                         (bbox['x'], bbox['y']),
                         (bbox['x'] + bbox['width'], bbox['y'] + bbox['height']),
                         color, 2)
            
            label = f"{elem['type']}: {elem['text'][:20]}"
            cv2.putText(image, label,
                       (bbox['x'], bbox['y'] - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
        
        cv2.imwrite(output_path, image)
