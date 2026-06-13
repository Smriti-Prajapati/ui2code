"""
Component Hierarchy Generation
Generates structured JSON representation of UI components
"""
from typing import List, Dict
import json

class HierarchyBuilder:
    """
    Builds hierarchical component structure from detected components
    """
    
    def __init__(self):
        self.component_priorities = {
            'navbar': 1,
            'header': 2,
            'sidebar': 3,
            'main': 4,
            'hero': 5,
            'section': 6,
            'card': 7,
            'button': 8,
            'text': 9,
            'image': 10,
            'footer': 11
        }
    
    def build_hierarchy(self, components: List[Dict], 
                       layout: Dict,
                       text_elements: List[Dict]) -> Dict:
        """
        Build hierarchical component structure
        
        Returns:
            Structured JSON representation
        """
        # Sort components by priority and position
        sorted_components = self._sort_components(components)
        
        # Build page structure
        page = {
            'type': 'page',
            'layout': layout['type'],
            'children': []
        }
        
        # Group components by sections
        sections = self._group_into_sections(sorted_components, layout)
        
        # Build each section
        for section in sections:
            section_node = self._build_section(section, text_elements)
            page['children'].append(section_node)
        
        return page
    
    def _sort_components(self, components: List[Dict]) -> List[Dict]:
        """Sort components by priority and position"""
        return sorted(components, key=lambda c: (
            self.component_priorities.get(c['type'], 99),
            c['bbox']['y'],
            c['bbox']['x']
        ))
    
    def _group_into_sections(self, components: List[Dict], 
                            layout: Dict) -> List[List[Dict]]:
        """Group components into logical sections"""
        sections = []
        current_section = []
        last_y = 0
        section_gap_threshold = 100
        
        for comp in components:
            # Start new section if there's a large vertical gap
            if comp['bbox']['y'] - last_y > section_gap_threshold and current_section:
                sections.append(current_section)
                current_section = []
            
            current_section.append(comp)
            last_y = comp['bbox']['y'] + comp['bbox']['height']
        
        if current_section:
            sections.append(current_section)
        
        return sections
    
    def _build_section(self, components: List[Dict], 
                      text_elements: List[Dict]) -> Dict:
        """Build a section node"""
        if not components:
            return {'type': 'section', 'children': []}
        
        # Determine section type
        section_type = self._determine_section_type(components)
        
        section = {
            'type': section_type,
            'children': []
        }
        
        # Add components to section
        for comp in components:
            comp_node = self._build_component_node(comp, text_elements)
            section['children'].append(comp_node)
        
        return section
    
    def _determine_section_type(self, components: List[Dict]) -> str:
        """Determine the type of section based on components"""
        types = [c['type'] for c in components]
        
        if 'navbar' in types:
            return 'navbar'
        elif 'header' in types:
            return 'header'
        elif 'footer' in types:
            return 'footer'
        elif 'sidebar' in types:
            return 'sidebar'
        elif types.count('card') >= 3:
            return 'cardGrid'
        elif 'form' in types:
            return 'form'
        elif any(t in types for t in ['hero', 'header']):
            return 'hero'
        else:
            return 'section'
    
    def _build_component_node(self, component: Dict, 
                             text_elements: List[Dict]) -> Dict:
        """Build a component node"""
        node = {
            'type': component['type'],
            'bbox': component['bbox'],
            'props': {}
        }
        
        # Add text content if available
        if 'text_content' in component and component['text_content']:
            node['text'] = ' '.join([t['text'] for t in component['text_content']])
            node['textType'] = component['text_content'][0]['type'] if component['text_content'] else 'text'
        
        # Add component-specific properties
        if component['type'] == 'button':
            node['props']['variant'] = 'primary'
            node['props']['size'] = 'medium'
        elif component['type'] == 'card':
            node['props']['elevation'] = 'medium'
            node['props']['padding'] = 'medium'
        elif component['type'] == 'image':
            node['props']['alt'] = 'Image'
            node['props']['objectFit'] = 'cover'
        
        return node
    
    def to_json(self, hierarchy: Dict, pretty: bool = True) -> str:
        """Convert hierarchy to JSON string"""
        if pretty:
            return json.dumps(hierarchy, indent=2)
        return json.dumps(hierarchy)
    
    def visualize_hierarchy(self, hierarchy: Dict, indent: int = 0) -> str:
        """Create a text visualization of the hierarchy"""
        lines = []
        prefix = "  " * indent
        
        node_type = hierarchy.get('type', 'unknown')
        lines.append(f"{prefix}├─ {node_type}")
        
        # Add text if available
        if 'text' in hierarchy:
            text_preview = hierarchy['text'][:30] + "..." if len(hierarchy['text']) > 30 else hierarchy['text']
            lines.append(f"{prefix}│  └─ text: \"{text_preview}\"")
        
        # Recursively process children
        if 'children' in hierarchy:
            for child in hierarchy['children']:
                lines.append(self.visualize_hierarchy(child, indent + 1))
        
        return "\n".join(lines)
