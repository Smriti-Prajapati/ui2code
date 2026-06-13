"""
Layout Intelligence Engine
Analyzes spacing, alignment, hierarchy, and converts to semantic layouts
"""
import numpy as np
from typing import List, Dict, Tuple
from collections import defaultdict

class LayoutAnalyzer:
    """
    Analyzes layout structure and converts absolute positions to semantic layouts
    Detects: rows, columns, grids, flex layouts, containers, nested components
    """
    
    def __init__(self):
        self.alignment_threshold = 10  # pixels
        self.spacing_threshold = 20
    
    def analyze_layout(self, components: List[Dict], 
                      image_width: int, image_height: int) -> Dict:
        """
        Analyze the layout structure of components
        
        Returns:
            Layout structure with hierarchy and relationships
        """
        if not components:
            return {'type': 'empty', 'children': []}
        
        # Sort components by position
        sorted_components = sorted(components, key=lambda c: (c['bbox']['y'], c['bbox']['x']))
        
        # Detect layout patterns
        layout_type = self._detect_layout_type(sorted_components, image_width, image_height)
        
        # Group components into rows and columns
        rows = self._group_into_rows(sorted_components)
        
        # Detect grids
        grids = self._detect_grids(rows)
        
        # Build hierarchy
        hierarchy = self._build_hierarchy(sorted_components, rows, grids)
        
        # Analyze spacing
        spacing = self._analyze_spacing(sorted_components)
        
        # Detect alignment
        alignment = self._detect_alignment(sorted_components)
        
        return {
            'type': layout_type,
            'hierarchy': hierarchy,
            'rows': rows,
            'grids': grids,
            'spacing': spacing,
            'alignment': alignment,
            'dimensions': {
                'width': image_width,
                'height': image_height
            }
        }
    
    def _detect_layout_type(self, components: List[Dict], 
                           width: int, height: int) -> str:
        """Detect the overall layout type"""
        if not components:
            return 'empty'
        
        # Check for navbar at top
        has_navbar = any(c['type'] == 'navbar' and c['bbox']['y'] < height * 0.15 
                        for c in components)
        
        # Check for sidebar
        has_sidebar = any(c['type'] == 'sidebar' and c['bbox']['x'] < width * 0.2
                         for c in components)
        
        # Check for grid layout
        rows = self._group_into_rows(components)
        if len(rows) > 2:
            avg_items_per_row = sum(len(row) for row in rows) / len(rows)
            if avg_items_per_row >= 2:
                return 'grid'
        
        # Check for single column
        if all(c['bbox']['x'] < width * 0.2 or c['bbox']['x'] > width * 0.8 
               for c in components):
            return 'single_column'
        
        if has_navbar and has_sidebar:
            return 'dashboard'
        elif has_navbar:
            return 'landing_page'
        elif has_sidebar:
            return 'sidebar_layout'
        
        return 'flex'
    
    def _group_into_rows(self, components: List[Dict]) -> List[List[Dict]]:
        """Group components into horizontal rows"""
        if not components:
            return []
        
        rows = []
        current_row = [components[0]]
        
        for comp in components[1:]:
            # Check if component is in the same row as the last component
            last_comp = current_row[-1]
            y_diff = abs(comp['center']['y'] - last_comp['center']['y'])
            
            if y_diff < self.alignment_threshold:
                current_row.append(comp)
            else:
                rows.append(current_row)
                current_row = [comp]
        
        if current_row:
            rows.append(current_row)
        
        return rows
    
    def _detect_grids(self, rows: List[List[Dict]]) -> List[Dict]:
        """Detect grid patterns in the layout"""
        grids = []
        
        if len(rows) < 2:
            return grids
        
        # Look for consecutive rows with similar number of items
        i = 0
        while i < len(rows):
            grid_rows = [rows[i]]
            j = i + 1
            
            while j < len(rows):
                # Check if rows have similar structure
                if self._are_rows_similar(rows[i], rows[j]):
                    grid_rows.append(rows[j])
                    j += 1
                else:
                    break
            
            # If we found at least 2 similar rows, it's a grid
            if len(grid_rows) >= 2:
                grid = {
                    'type': 'grid',
                    'rows': len(grid_rows),
                    'columns': len(grid_rows[0]),
                    'components': [comp for row in grid_rows for comp in row],
                    'start_row': i,
                    'end_row': j - 1
                }
                grids.append(grid)
                i = j
            else:
                i += 1
        
        return grids
    
    def _are_rows_similar(self, row1: List[Dict], row2: List[Dict]) -> bool:
        """Check if two rows have similar structure"""
        if abs(len(row1) - len(row2)) > 1:
            return False
        
        # Check if components have similar widths
        if len(row1) != len(row2):
            return False
        
        for comp1, comp2 in zip(row1, row2):
            width_diff = abs(comp1['bbox']['width'] - comp2['bbox']['width'])
            if width_diff > 50:  # Allow 50px difference
                return False
        
        return True
    
    def _build_hierarchy(self, components: List[Dict], 
                        rows: List[List[Dict]], 
                        grids: List[Dict]) -> Dict:
        """Build component hierarchy"""
        root = {
            'type': 'page',
            'children': []
        }
        
        # Group components by type and position
        navbar_components = [c for c in components if c['type'] == 'navbar']
        header_components = [c for c in components if c['type'] == 'header']
        footer_components = [c for c in components if c['type'] == 'footer']
        
        # Add navbar
        if navbar_components:
            root['children'].append({
                'type': 'navbar',
                'components': navbar_components
            })
        
        # Add header
        if header_components:
            root['children'].append({
                'type': 'header',
                'components': header_components
            })
        
        # Add main content
        main_content = {
            'type': 'main',
            'children': []
        }
        
        # Add grids
        for grid in grids:
            main_content['children'].append(grid)
        
        # Add remaining components
        grid_components = set()
        for grid in grids:
            grid_components.update(id(c) for c in grid['components'])
        
        other_components = [c for c in components 
                          if id(c) not in grid_components 
                          and c['type'] not in ['navbar', 'header', 'footer']]
        
        if other_components:
            main_content['children'].append({
                'type': 'section',
                'components': other_components
            })
        
        root['children'].append(main_content)
        
        # Add footer
        if footer_components:
            root['children'].append({
                'type': 'footer',
                'components': footer_components
            })
        
        return root
    
    def _analyze_spacing(self, components: List[Dict]) -> Dict:
        """Analyze spacing between components"""
        if len(components) < 2:
            return {'horizontal': [], 'vertical': []}
        
        horizontal_gaps = []
        vertical_gaps = []
        
        for i, comp1 in enumerate(components):
            for comp2 in components[i+1:]:
                # Calculate gaps
                h_gap = self._calculate_horizontal_gap(comp1['bbox'], comp2['bbox'])
                v_gap = self._calculate_vertical_gap(comp1['bbox'], comp2['bbox'])
                
                if h_gap > 0:
                    horizontal_gaps.append(h_gap)
                if v_gap > 0:
                    vertical_gaps.append(v_gap)
        
        # Find common spacing values
        h_spacing = self._find_common_values(horizontal_gaps)
        v_spacing = self._find_common_values(vertical_gaps)
        
        return {
            'horizontal': h_spacing,
            'vertical': v_spacing,
            'padding': self._estimate_padding(components),
            'margin': self._estimate_margin(components)
        }
    
    def _calculate_horizontal_gap(self, bbox1: Dict, bbox2: Dict) -> int:
        """Calculate horizontal gap between two boxes"""
        right1 = bbox1['x'] + bbox1['width']
        left2 = bbox2['x']
        
        if right1 < left2:
            return left2 - right1
        
        right2 = bbox2['x'] + bbox2['width']
        left1 = bbox1['x']
        
        if right2 < left1:
            return left1 - right2
        
        return 0
    
    def _calculate_vertical_gap(self, bbox1: Dict, bbox2: Dict) -> int:
        """Calculate vertical gap between two boxes"""
        bottom1 = bbox1['y'] + bbox1['height']
        top2 = bbox2['y']
        
        if bottom1 < top2:
            return top2 - bottom1
        
        bottom2 = bbox2['y'] + bbox2['height']
        top1 = bbox1['y']
        
        if bottom2 < top1:
            return top1 - bottom2
        
        return 0
    
    def _find_common_values(self, values: List[int], tolerance: int = 5) -> List[int]:
        """Find common spacing values"""
        if not values:
            return []
        
        # Group similar values
        groups = defaultdict(list)
        for val in values:
            # Round to nearest multiple of tolerance
            key = round(val / tolerance) * tolerance
            groups[key].append(val)
        
        # Return most common values
        common = sorted(groups.items(), key=lambda x: len(x[1]), reverse=True)
        return [int(np.mean(vals)) for key, vals in common[:3]]
    
    def _estimate_padding(self, components: List[Dict]) -> int:
        """Estimate common padding value"""
        # Use smallest common spacing as padding
        all_gaps = []
        for i, comp1 in enumerate(components):
            for comp2 in components[i+1:]:
                h_gap = self._calculate_horizontal_gap(comp1['bbox'], comp2['bbox'])
                v_gap = self._calculate_vertical_gap(comp1['bbox'], comp2['bbox'])
                if h_gap > 0:
                    all_gaps.append(h_gap)
                if v_gap > 0:
                    all_gaps.append(v_gap)
        
        if all_gaps:
            return min(all_gaps)
        return 16  # Default
    
    def _estimate_margin(self, components: List[Dict]) -> int:
        """Estimate common margin value"""
        if not components:
            return 20
        
        # Find minimum distance from edges
        min_x = min(c['bbox']['x'] for c in components)
        return max(16, min_x)
    
    def _detect_alignment(self, components: List[Dict]) -> Dict:
        """Detect alignment patterns"""
        alignments = {
            'left_aligned': [],
            'right_aligned': [],
            'center_aligned': [],
            'top_aligned': [],
            'bottom_aligned': []
        }
        
        # Group by similar x coordinates (left alignment)
        x_groups = defaultdict(list)
        for comp in components:
            x_key = round(comp['bbox']['x'] / self.alignment_threshold) * self.alignment_threshold
            x_groups[x_key].append(comp)
        
        for x, group in x_groups.items():
            if len(group) >= 2:
                alignments['left_aligned'].append({
                    'x': x,
                    'components': group
                })
        
        # Group by similar y coordinates (top alignment)
        y_groups = defaultdict(list)
        for comp in components:
            y_key = round(comp['bbox']['y'] / self.alignment_threshold) * self.alignment_threshold
            y_groups[y_key].append(comp)
        
        for y, group in y_groups.items():
            if len(group) >= 2:
                alignments['top_aligned'].append({
                    'y': y,
                    'components': group
                })
        
        return alignments
