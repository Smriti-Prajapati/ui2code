"""
AI Reasoning Layer
Uses LLM to reason about component purpose, naming, hierarchy, accessibility
"""
import os
from typing import List, Dict, Optional
import json

class AIReasoner:
    """
    Uses LLM to add semantic understanding to detected components
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize AI reasoner with API key"""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.use_llm = bool(self.api_key)
        
        if self.use_llm:
            try:
                import openai
                self.client = openai.OpenAI(api_key=self.api_key)
            except ImportError:
                print("Warning: openai package not installed. Using rule-based reasoning.")
                self.use_llm = False
    
    def reason_about_components(self, hierarchy: Dict, 
                               design_system: Dict,
                               layout: Dict) -> Dict:
        """
        Apply AI reasoning to enhance component understanding
        
        Returns:
            Enhanced hierarchy with semantic information
        """
        if self.use_llm:
            return self._llm_reasoning(hierarchy, design_system, layout)
        else:
            return self._rule_based_reasoning(hierarchy, design_system, layout)
    
    def _llm_reasoning(self, hierarchy: Dict, 
                      design_system: Dict,
                      layout: Dict) -> Dict:
        """Use LLM for advanced reasoning"""
        try:
            # Prepare context for LLM
            context = self._prepare_context(hierarchy, design_system, layout)
            
            prompt = f"""
You are a frontend engineer analyzing a UI screenshot. Based on the detected components and layout, provide semantic understanding.

Context:
{json.dumps(context, indent=2)}

Tasks:
1. Suggest appropriate component names (e.g., "HeroSection", "PricingCard", "CTAButton")
2. Identify the purpose of each component
3. Suggest accessibility improvements (ARIA labels, alt text, etc.)
4. Recommend responsive behavior
5. Identify any missing semantic HTML elements

Respond with a JSON object containing enhanced component information.
"""
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert frontend engineer specializing in UI/UX and accessibility."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            # Parse LLM response
            llm_output = response.choices[0].message.content
            enhancements = json.loads(llm_output)
            
            # Apply enhancements to hierarchy
            enhanced = self._apply_enhancements(hierarchy, enhancements)
            return enhanced
            
        except Exception as e:
            print(f"LLM reasoning failed: {e}. Falling back to rule-based.")
            return self._rule_based_reasoning(hierarchy, design_system, layout)
    
    def _rule_based_reasoning(self, hierarchy: Dict,
                             design_system: Dict,
                             layout: Dict) -> Dict:
        """Rule-based reasoning without LLM"""
        enhanced = hierarchy.copy()
        
        # Apply naming conventions
        enhanced = self._apply_naming_conventions(enhanced)
        
        # Add accessibility attributes
        enhanced = self._add_accessibility(enhanced)
        
        # Add responsive hints
        enhanced = self._add_responsive_hints(enhanced, layout)
        
        # Infer component purposes
        enhanced = self._infer_purposes(enhanced)
        
        return enhanced
    
    def _prepare_context(self, hierarchy: Dict,
                        design_system: Dict,
                        layout: Dict) -> Dict:
        """Prepare context for LLM"""
        return {
            'layout_type': layout.get('type', 'unknown'),
            'num_components': self._count_components(hierarchy),
            'component_types': self._get_component_types(hierarchy),
            'has_navbar': self._has_component_type(hierarchy, 'navbar'),
            'has_footer': self._has_component_type(hierarchy, 'footer'),
            'color_scheme': {
                'primary': design_system['colors']['primary'],
                'background': design_system['colors']['background']
            }
        }
    
    def _apply_naming_conventions(self, hierarchy: Dict) -> Dict:
        """Apply semantic naming conventions"""
        if 'children' in hierarchy:
            for i, child in enumerate(hierarchy['children']):
                child_type = child.get('type', 'component')
                
                # Generate semantic name
                if child_type == 'navbar':
                    child['componentName'] = 'NavigationBar'
                elif child_type == 'hero':
                    child['componentName'] = 'HeroSection'
                elif child_type == 'cardGrid':
                    child['componentName'] = 'FeatureGrid'
                elif child_type == 'card':
                    child['componentName'] = f'Card{i+1}'
                elif child_type == 'button':
                    text = child.get('text', '')
                    if 'get started' in text.lower():
                        child['componentName'] = 'CTAButton'
                    elif 'sign' in text.lower() or 'log' in text.lower():
                        child['componentName'] = 'AuthButton'
                    else:
                        child['componentName'] = f'Button{i+1}'
                elif child_type == 'footer':
                    child['componentName'] = 'Footer'
                else:
                    child['componentName'] = f'{child_type.capitalize()}{i+1}'
                
                # Recursively apply to children
                if 'children' in child:
                    child = self._apply_naming_conventions(child)
        
        return hierarchy
    
    def _add_accessibility(self, hierarchy: Dict) -> Dict:
        """Add accessibility attributes"""
        if 'children' in hierarchy:
            for child in hierarchy['children']:
                child_type = child.get('type', '')
                
                # Add ARIA attributes
                if child_type == 'navbar':
                    child['a11y'] = {
                        'role': 'navigation',
                        'ariaLabel': 'Main navigation'
                    }
                elif child_type == 'button':
                    child['a11y'] = {
                        'role': 'button',
                        'ariaLabel': child.get('text', 'Button')
                    }
                elif child_type == 'image':
                    child['a11y'] = {
                        'alt': 'Descriptive image text',
                        'role': 'img'
                    }
                elif child_type == 'form':
                    child['a11y'] = {
                        'role': 'form',
                        'ariaLabel': 'Contact form'
                    }
                elif child_type in ['header', 'hero']:
                    child['a11y'] = {
                        'role': 'banner'
                    }
                elif child_type == 'footer':
                    child['a11y'] = {
                        'role': 'contentinfo'
                    }
                
                # Recursively apply to children
                if 'children' in child:
                    child = self._add_accessibility(child)
        
        return hierarchy
    
    def _add_responsive_hints(self, hierarchy: Dict, layout: Dict) -> Dict:
        """Add responsive behavior hints"""
        if 'children' in hierarchy:
            for child in hierarchy['children']:
                child_type = child.get('type', '')
                
                # Add responsive hints
                if child_type == 'cardGrid':
                    child['responsive'] = {
                        'mobile': 'grid-cols-1',
                        'tablet': 'grid-cols-2',
                        'desktop': 'grid-cols-3'
                    }
                elif child_type == 'navbar':
                    child['responsive'] = {
                        'mobile': 'hamburger-menu',
                        'desktop': 'horizontal-menu'
                    }
                elif child_type in ['hero', 'header']:
                    child['responsive'] = {
                        'mobile': 'stack-vertical',
                        'desktop': 'flex-horizontal'
                    }
                
                # Recursively apply to children
                if 'children' in child:
                    child = self._add_responsive_hints(child, layout)
        
        return hierarchy
    
    def _infer_purposes(self, hierarchy: Dict) -> Dict:
        """Infer component purposes"""
        if 'children' in hierarchy:
            for child in hierarchy['children']:
                child_type = child.get('type', '')
                text = child.get('text', '').lower()
                
                # Infer purpose
                if child_type == 'button':
                    if any(word in text for word in ['sign', 'log', 'register']):
                        child['purpose'] = 'authentication'
                    elif any(word in text for word in ['buy', 'purchase', 'checkout']):
                        child['purpose'] = 'commerce'
                    elif any(word in text for word in ['get started', 'try', 'demo']):
                        child['purpose'] = 'call-to-action'
                    elif any(word in text for word in ['submit', 'send']):
                        child['purpose'] = 'form-submission'
                    else:
                        child['purpose'] = 'action'
                elif child_type == 'card':
                    child['purpose'] = 'content-display'
                elif child_type == 'form':
                    child['purpose'] = 'data-collection'
                elif child_type == 'navbar':
                    child['purpose'] = 'navigation'
                
                # Recursively apply to children
                if 'children' in child:
                    child = self._infer_purposes(child)
        
        return hierarchy
    
    def _apply_enhancements(self, hierarchy: Dict, 
                           enhancements: Dict) -> Dict:
        """Apply LLM enhancements to hierarchy"""
        # This would merge LLM suggestions with the hierarchy
        # For now, return the hierarchy as-is
        return hierarchy
    
    def _count_components(self, hierarchy: Dict) -> int:
        """Count total components in hierarchy"""
        count = 1
        if 'children' in hierarchy:
            for child in hierarchy['children']:
                count += self._count_components(child)
        return count
    
    def _get_component_types(self, hierarchy: Dict) -> List[str]:
        """Get list of all component types"""
        types = [hierarchy.get('type', 'unknown')]
        if 'children' in hierarchy:
            for child in hierarchy['children']:
                types.extend(self._get_component_types(child))
        return list(set(types))
    
    def _has_component_type(self, hierarchy: Dict, 
                           component_type: str) -> bool:
        """Check if hierarchy contains a specific component type"""
        if hierarchy.get('type') == component_type:
            return True
        if 'children' in hierarchy:
            return any(self._has_component_type(child, component_type) 
                      for child in hierarchy['children'])
        return False
