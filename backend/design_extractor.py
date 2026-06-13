"""
Design System Extraction
Extracts colors, typography, spacing, shadows, and generates reusable design system
"""
import cv2
import numpy as np
from typing import List, Dict, Tuple
from collections import Counter

class DesignExtractor:
    """
    Extract design system from UI screenshot
    Includes: colors, typography, spacing, borders, shadows
    """
    
    def __init__(self):
        self.n_colors = 8  # Number of main colors to extract
    
    def extract_design_system(self, image_path: str, 
                             components: List[Dict],
                             text_elements: List[Dict]) -> Dict:
        """
        Extract complete design system from image
        
        Returns:
            Design system with colors, typography, spacing, etc.
        """
        image = cv2.imread(image_path)
        
        # Extract color palette
        colors = self._extract_colors(image)
        
        # Extract typography
        typography = self._extract_typography(text_elements)
        
        # Extract spacing scale
        spacing = self._extract_spacing_scale(components)
        
        # Extract border radius
        border_radius = self._extract_border_radius(image, components)
        
        # Extract shadows
        shadows = self._detect_shadows(image, components)
        
        # Generate design tokens
        design_tokens = self._generate_design_tokens(
            colors, typography, spacing, border_radius, shadows
        )
        
        return {
            'colors': colors,
            'typography': typography,
            'spacing': spacing,
            'border_radius': border_radius,
            'shadows': shadows,
            'design_tokens': design_tokens
        }
    
    def _extract_colors(self, image: np.ndarray) -> Dict:
        """Extract color palette using K-means clustering"""
        # Reshape image to list of pixels
        pixels = image.reshape(-1, 3)
        
        # Sample pixels for faster processing
        sample_size = min(10000, len(pixels))
        sampled_pixels = pixels[np.random.choice(len(pixels), sample_size, replace=False)]
        
        try:
            from sklearn.cluster import KMeans

            kmeans = KMeans(n_clusters=self.n_colors, random_state=42, n_init=10)
            kmeans.fit(sampled_pixels)
            colors_bgr = kmeans.cluster_centers_.astype(int)
        except Exception:
            quantized = (sampled_pixels // 24) * 24
            counts = Counter(map(tuple, quantized))
            colors_bgr = np.array([color for color, _ in counts.most_common(self.n_colors)])
        
        # Convert BGR to RGB and hex
        colors = []
        for bgr in colors_bgr:
            rgb = (int(bgr[2]), int(bgr[1]), int(bgr[0]))
            hex_color = '#{:02x}{:02x}{:02x}'.format(*rgb)
            
            # Classify color
            color_type = self._classify_color(rgb)
            
            colors.append({
                'rgb': rgb,
                'hex': hex_color,
                'type': color_type
            })
        
        # Sort colors by brightness
        colors.sort(key=lambda c: sum(c['rgb']) / 3, reverse=True)
        
        # Identify primary, secondary, accent colors
        palette = {
            'primary': colors[0]['hex'] if colors else '#000000',
            'secondary': colors[1]['hex'] if len(colors) > 1 else '#666666',
            'accent': colors[2]['hex'] if len(colors) > 2 else '#0066cc',
            'background': self._find_background_color(colors),
            'text': self._find_text_color(colors),
            'all_colors': colors
        }
        
        return palette
    
    def _classify_color(self, rgb: Tuple[int, int, int]) -> str:
        """Classify color type (light, dark, neutral, etc.)"""
        r, g, b = rgb
        brightness = (r + g + b) / 3
        
        # Check if grayscale
        if max(r, g, b) - min(r, g, b) < 30:
            if brightness > 200:
                return 'light_neutral'
            elif brightness < 50:
                return 'dark_neutral'
            else:
                return 'neutral'
        
        # Check dominant channel
        if r > g and r > b:
            return 'red'
        elif g > r and g > b:
            return 'green'
        elif b > r and b > g:
            return 'blue'
        
        return 'mixed'
    
    def _find_background_color(self, colors: List[Dict]) -> str:
        """Find most likely background color (lightest)"""
        light_colors = [c for c in colors if c['type'] in ['light_neutral', 'neutral']]
        if light_colors:
            return light_colors[0]['hex']
        return '#ffffff'
    
    def _find_text_color(self, colors: List[Dict]) -> str:
        """Find most likely text color (darkest)"""
        dark_colors = [c for c in colors if c['type'] in ['dark_neutral', 'neutral']]
        if dark_colors:
            return dark_colors[-1]['hex']
        return '#000000'
    
    def _extract_typography(self, text_elements: List[Dict]) -> Dict:
        """Extract typography system"""
        if not text_elements:
            return self._default_typography()
        
        # Collect font sizes
        font_sizes = [elem['font_size'] for elem in text_elements]
        
        # Find unique font sizes
        unique_sizes = sorted(set(font_sizes), reverse=True)
        
        # Create typography scale
        typography = {
            'h1': unique_sizes[0] if len(unique_sizes) > 0 else 48,
            'h2': unique_sizes[1] if len(unique_sizes) > 1 else 36,
            'h3': unique_sizes[2] if len(unique_sizes) > 2 else 28,
            'h4': unique_sizes[3] if len(unique_sizes) > 3 else 24,
            'body': unique_sizes[4] if len(unique_sizes) > 4 else 16,
            'small': unique_sizes[5] if len(unique_sizes) > 5 else 14,
            'font_family': 'Inter, system-ui, sans-serif',
            'line_height': 1.5,
            'font_weights': {
                'normal': 400,
                'medium': 500,
                'semibold': 600,
                'bold': 700
            }
        }
        
        return typography
    
    def _default_typography(self) -> Dict:
        """Default typography system"""
        return {
            'h1': 48,
            'h2': 36,
            'h3': 28,
            'h4': 24,
            'body': 16,
            'small': 14,
            'font_family': 'Inter, system-ui, sans-serif',
            'line_height': 1.5,
            'font_weights': {
                'normal': 400,
                'medium': 500,
                'semibold': 600,
                'bold': 700
            }
        }
    
    def _extract_spacing_scale(self, components: List[Dict]) -> Dict:
        """Extract spacing scale from component gaps"""
        if len(components) < 2:
            return self._default_spacing()
        
        gaps = []
        for i, comp1 in enumerate(components):
            for comp2 in components[i+1:]:
                gap = self._calculate_gap(comp1['bbox'], comp2['bbox'])
                if gap > 0:
                    gaps.append(gap)
        
        if not gaps:
            return self._default_spacing()
        
        # Find common spacing values
        gap_counts = Counter(gaps)
        common_gaps = sorted([g for g, _ in gap_counts.most_common(6)])
        
        # Create spacing scale
        spacing = {
            'xs': common_gaps[0] if len(common_gaps) > 0 else 4,
            'sm': common_gaps[1] if len(common_gaps) > 1 else 8,
            'md': common_gaps[2] if len(common_gaps) > 2 else 16,
            'lg': common_gaps[3] if len(common_gaps) > 3 else 24,
            'xl': common_gaps[4] if len(common_gaps) > 4 else 32,
            '2xl': common_gaps[5] if len(common_gaps) > 5 else 48
        }
        
        return spacing
    
    def _default_spacing(self) -> Dict:
        """Default spacing scale"""
        return {
            'xs': 4,
            'sm': 8,
            'md': 16,
            'lg': 24,
            'xl': 32,
            '2xl': 48
        }
    
    def _calculate_gap(self, bbox1: Dict, bbox2: Dict) -> int:
        """Calculate minimum gap between two boxes"""
        # Horizontal gap
        h_gap = min(
            abs(bbox1['x'] - (bbox2['x'] + bbox2['width'])),
            abs(bbox2['x'] - (bbox1['x'] + bbox1['width']))
        )
        
        # Vertical gap
        v_gap = min(
            abs(bbox1['y'] - (bbox2['y'] + bbox2['height'])),
            abs(bbox2['y'] - (bbox1['y'] + bbox1['height']))
        )
        
        return min(h_gap, v_gap)
    
    def _extract_border_radius(self, image: np.ndarray, 
                               components: List[Dict]) -> Dict:
        """Detect border radius from components"""
        # Simplified: return common border radius values
        return {
            'none': 0,
            'sm': 4,
            'md': 8,
            'lg': 12,
            'xl': 16,
            'full': 9999
        }
    
    def _detect_shadows(self, image: np.ndarray, 
                       components: List[Dict]) -> Dict:
        """Detect shadow styles"""
        # Simplified: return common shadow values
        return {
            'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
            'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
            'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
            'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1)',
            '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.25)'
        }
    
    def _generate_design_tokens(self, colors: Dict, typography: Dict,
                               spacing: Dict, border_radius: Dict,
                               shadows: Dict) -> Dict:
        """Generate design tokens for code generation"""
        return {
            'colors': {
                '--color-primary': colors['primary'],
                '--color-secondary': colors['secondary'],
                '--color-accent': colors['accent'],
                '--color-background': colors['background'],
                '--color-text': colors['text']
            },
            'typography': {
                '--font-family': typography['font_family'],
                '--font-size-h1': f"{typography['h1']}px",
                '--font-size-h2': f"{typography['h2']}px",
                '--font-size-h3': f"{typography['h3']}px",
                '--font-size-body': f"{typography['body']}px",
                '--line-height': typography['line_height']
            },
            'spacing': {
                '--spacing-xs': f"{spacing['xs']}px",
                '--spacing-sm': f"{spacing['sm']}px",
                '--spacing-md': f"{spacing['md']}px",
                '--spacing-lg': f"{spacing['lg']}px",
                '--spacing-xl': f"{spacing['xl']}px"
            },
            'borders': {
                '--radius-sm': f"{border_radius['sm']}px",
                '--radius-md': f"{border_radius['md']}px",
                '--radius-lg': f"{border_radius['lg']}px"
            },
            'shadows': {
                '--shadow-sm': shadows['sm'],
                '--shadow-md': shadows['md'],
                '--shadow-lg': shadows['lg']
            }
        }
