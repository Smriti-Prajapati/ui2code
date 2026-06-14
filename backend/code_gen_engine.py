"""
Code Generation Engine
Generates production-ready React, Next.js, HTML/CSS/JS, and Tailwind code
"""
from typing import Dict, List, Optional
import os

class CodeGenerator:
    """
    Generates code from component hierarchy and design system
    Supports: React, Next.js, HTML/CSS/JS, Tailwind CSS
    """
    
    def __init__(self, framework: str = 'react', styling: str = 'tailwind'):
        """
        Initialize code generator
        
        Args:
            framework: 'react', 'nextjs', 'html', 'vue'
            styling: 'tailwind', 'css', 'styled-components'
        """
        self.framework = framework
        self.styling = styling
    
    def generate_code(self, hierarchy: Dict, 
                     design_system: Dict,
                     layout: Dict) -> Dict:
        """
        Generate complete code from hierarchy
        
        Returns:
            Dictionary with generated files
        """
        if self.framework == 'react':
            return self._generate_react(hierarchy, design_system, layout)
        elif self.framework == 'nextjs':
            return self._generate_nextjs(hierarchy, design_system, layout)
        elif self.framework == 'html':
            return self._generate_html(hierarchy, design_system, layout)
        else:
            return self._generate_react(hierarchy, design_system, layout)
    
    def _generate_react(self, hierarchy: Dict,
                       design_system: Dict,
                       layout: Dict) -> Dict:
        """Generate React + Tailwind code"""
        files = {}
        
        # Generate main component
        files['App.jsx'] = self._generate_react_component(
            hierarchy, design_system, 'App'
        )
        
        # Generate individual components
        components = self._extract_components(hierarchy)
        for comp_name, comp_data in components.items():
            files[f'components/{comp_name}.jsx'] = self._generate_react_component(
                comp_data, design_system, comp_name
            )
        
        # Generate Tailwind config
        files['tailwind.config.js'] = self._generate_tailwind_config(design_system)
        
        # Generate CSS
        files['styles/globals.css'] = self._generate_global_css(design_system)
        
        # Generate package.json
        files['package.json'] = self._generate_package_json('react')
        
        return files
    
    def _generate_react_component(self, hierarchy: Dict,
                                  design_system: Dict,
                                  component_name: str) -> str:
        """Generate a React component"""
        imports = "import React from 'react';\n"
        
        # Generate component body
        jsx = self._hierarchy_to_jsx(hierarchy, design_system)
        
        component = f"""{imports}
export default function {component_name}() {{
  return (
{self._indent(jsx, 2)}
  );
}}
"""
        return component
    
    def _hierarchy_to_jsx(self, node: Dict, design_system: Dict, 
                         level: int = 0) -> str:
        """Convert hierarchy node to JSX"""
        node_type = node.get('type', 'div')
        text = node.get('text', '')
        children = node.get('children', [])
        
        # Map component types to JSX elements
        jsx_element = self._map_to_jsx_element(node_type)
        
        # Generate Tailwind classes
        classes = self._generate_tailwind_classes(node, design_system)
        
        # Generate accessibility attributes
        a11y_attrs = self._generate_a11y_attributes(node)
        
        # Build opening tag
        attrs = f'className="{classes}"'
        if a11y_attrs:
            attrs += ' ' + a11y_attrs
        
        opening = f"<{jsx_element} {attrs}>"
        closing = f"</{jsx_element}>"
        
        # Generate content
        if text and not children:
            return f"{opening}{text}{closing}"
        elif children:
            child_jsx = '\n'.join([
                self._hierarchy_to_jsx(child, design_system, level + 1)
                for child in children
            ])
            return f"{opening}\n{self._indent(child_jsx, 1)}\n{closing}"
        else:
            return f"{opening}{closing}"
    
    def _map_to_jsx_element(self, component_type: str) -> str:
        """Map component type to JSX element"""
        mapping = {
            'page': 'div',
            'navbar': 'nav',
            'header': 'header',
            'footer': 'footer',
            'main': 'main',
            'section': 'section',
            'hero': 'section',
            'cardGrid': 'div',
            'card': 'div',
            'button': 'button',
            'text': 'p',
            'image': 'img',
            'container': 'div',
            'form': 'form',
            'input': 'input'
        }
        return mapping.get(component_type, 'div')
    
    def _generate_tailwind_classes(self, node: Dict, 
                                   design_system: Dict) -> str:
        """Generate Tailwind CSS classes for a node"""
        classes = []
        node_type = node.get('type', 'div')
        responsive = node.get('responsive', {})
        
        # Base classes by type
        if node_type == 'navbar':
            classes.extend(['flex', 'items-center', 'justify-between', 
                          'px-6', 'py-4', 'bg-white', 'shadow-md'])
        elif node_type == 'hero':
            classes.extend(['flex', 'flex-col', 'items-center', 
                          'justify-center', 'py-20', 'px-6', 'text-center'])
        elif node_type == 'cardGrid':
            classes.extend(['grid', 'gap-6', 'px-6', 'py-12'])
            if responsive:
                classes.append('grid-cols-1')
                classes.append('md:grid-cols-2')
                classes.append('lg:grid-cols-3')
            else:
                classes.append('grid-cols-3')
        elif node_type == 'card':
            classes.extend(['p-6', 'bg-white', 'rounded-lg', 
                          'shadow-md', 'hover:shadow-lg', 'transition'])
        elif node_type == 'button':
            purpose = node.get('purpose', 'action')
            if purpose == 'call-to-action':
                classes.extend(['px-6', 'py-3', 'bg-blue-600', 
                              'text-white', 'rounded-lg', 'font-semibold',
                              'hover:bg-blue-700', 'transition'])
            else:
                classes.extend(['px-4', 'py-2', 'bg-gray-200', 
                              'rounded', 'hover:bg-gray-300', 'transition'])
        elif node_type == 'footer':
            classes.extend(['py-8', 'px-6', 'bg-gray-900', 
                          'text-white', 'text-center'])
        elif node_type == 'section':
            classes.extend(['py-12', 'px-6'])
        
        # Text styling
        text_type = node.get('textType', '')
        if text_type == 'heading':
            classes.extend(['text-4xl', 'font-bold', 'mb-4'])
        elif text_type == 'subheading':
            classes.extend(['text-2xl', 'font-semibold', 'mb-3'])
        elif text_type == 'paragraph':
            classes.extend(['text-base', 'text-gray-600', 'mb-2'])
        
        return ' '.join(classes)
    
    def _generate_a11y_attributes(self, node: Dict) -> str:
        """Generate accessibility attributes"""
        a11y = node.get('a11y', {})
        attrs = []
        
        if 'role' in a11y:
            attrs.append(f'role="{a11y["role"]}"')
        if 'ariaLabel' in a11y:
            attrs.append(f'aria-label="{a11y["ariaLabel"]}"')
        if 'alt' in a11y:
            attrs.append(f'alt="{a11y["alt"]}"')
        
        return ' '.join(attrs)
    
    def _generate_html(self, hierarchy: Dict,
                      design_system: Dict,
                      layout: Dict) -> Dict:
        """Generate HTML/CSS/JS code"""
        files = {}
        
        # Generate HTML
        html_body = self._hierarchy_to_html(hierarchy, design_system)
        files['index.html'] = self._wrap_html(html_body, design_system)
        
        # Generate CSS
        files['style.css'] = self._generate_css(hierarchy, design_system)
        
        # Generate JavaScript
        files['script.js'] = self._generate_javascript(hierarchy)
        
        return files
    
    def _hierarchy_to_html(self, node: Dict, design_system: Dict) -> str:
        """Convert hierarchy to HTML"""
        node_type = node.get('type', 'div')
        text = node.get('text', '')
        children = node.get('children', [])
        component_name = node.get('componentName', '')
        
        # Map to HTML element
        html_element = self._map_to_html_element(node_type)
        
        # Generate CSS class
        css_class = self._generate_css_class(node, component_name)
        
        # Generate attributes
        attrs = f'class="{css_class}"'
        a11y_attrs = self._generate_a11y_attributes(node)
        if a11y_attrs:
            attrs += ' ' + a11y_attrs
        
        # Build HTML
        opening = f"<{html_element} {attrs}>"
        closing = f"</{html_element}>"
        
        if text and not children:
            return f"{opening}{text}{closing}"
        elif children:
            child_html = '\n'.join([
                self._hierarchy_to_html(child, design_system)
                for child in children
            ])
            return f"{opening}\n{self._indent(child_html, 1)}\n{closing}"
        else:
            return f"{opening}{closing}"
    
    def _map_to_html_element(self, component_type: str) -> str:
        """Map component type to HTML element"""
        mapping = {
            'navbar': 'nav',
            'header': 'header',
            'footer': 'footer',
            'main': 'main',
            'section': 'section',
            'button': 'button',
            'image': 'img',
            'form': 'form',
            'input': 'input'
        }
        return mapping.get(component_type, 'div')
    
    def _generate_css_class(self, node: Dict, component_name: str) -> str:
        """Generate CSS class name"""
        if component_name:
            return self._to_kebab_case(component_name)
        return node.get('type', 'component')
    
    def _wrap_html(self, body: str, design_system: Dict) -> str:
        """Wrap HTML body in complete document"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated UI</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
{self._indent(body, 1)}
    <script src="script.js"></script>
</body>
</html>"""
    
    def _generate_css(self, hierarchy: Dict, design_system: Dict) -> str:
        """Generate CSS from design system"""
        css = f"""/* Generated CSS */
:root {{
{self._generate_css_variables(design_system)}
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: {design_system['typography']['font_family']};
    line-height: {design_system['typography']['line_height']};
    color: {design_system['colors']['text']};
    background: {design_system['colors']['background']};
}}

/* Component Styles */
{self._generate_component_css(hierarchy, design_system)}
"""
        return css
    
    def _generate_css_variables(self, design_system: Dict) -> str:
        """Generate CSS custom properties"""
        tokens = design_system.get('design_tokens', {})
        lines = []
        
        for category, props in tokens.items():
            for prop, value in props.items():
                lines.append(f"    {prop}: {value};")
        
        return '\n'.join(lines)
    
    def _generate_component_css(self, hierarchy: Dict, 
                               design_system: Dict) -> str:
        """Generate CSS for components"""
        # Simplified CSS generation
        return """.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    background: white;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.hero {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 5rem 2rem;
    text-align: center;
}

.card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    padding: 3rem 2rem;
}

.card {
    padding: 2rem;
    background: white;
    border-radius: 0.5rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    transition: transform 0.3s, box-shadow 0.3s;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 12px rgba(0,0,0,0.15);
}

button {
    padding: 0.75rem 1.5rem;
    background: var(--color-primary, #0066cc);
    color: white;
    border: none;
    border-radius: 0.5rem;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.3s;
}

button:hover {
    background: var(--color-accent, #0052a3);
}

.footer {
    padding: 2rem;
    background: #1a1a1a;
    color: white;
    text-align: center;
}

@media (max-width: 768px) {
    .card-grid {
        grid-template-columns: 1fr;
    }
}"""
    
    def _generate_javascript(self, hierarchy: Dict) -> str:
        """Generate JavaScript for interactivity"""
        return """// Generated JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Add button click handlers
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            console.log('Button clicked:', this.textContent);
        });
    });
    
    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
});"""
    
    def _generate_nextjs(self, hierarchy: Dict,
                        design_system: Dict,
                        layout: Dict) -> Dict:
        """Generate Next.js code"""
        files = self._generate_react(hierarchy, design_system, layout)
        
        # Add Next.js specific files
        files['pages/index.js'] = files.pop('App.jsx')
        files['pages/_app.js'] = self._generate_nextjs_app()
        
        return files
    
    def _generate_nextjs_app(self) -> str:
        """Generate Next.js _app.js"""
        return """import '../styles/globals.css'

export default function App({ Component, pageProps }) {
  return <Component {...pageProps} />
}"""
    
    def _generate_tailwind_config(self, design_system: Dict) -> str:
        """Generate Tailwind configuration"""
        colors = design_system.get('colors', {})
        typography = design_system.get('typography', {})
        
        return f"""module.exports = {{
  content: [
    './pages/**/*.{{js,jsx}}',
    './components/**/*.{{js,jsx}}',
  ],
  theme: {{
    extend: {{
      colors: {{
        primary: '{colors.get("primary", "#0066cc")}',
        secondary: '{colors.get("secondary", "#666666")}',
        accent: '{colors.get("accent", "#0066cc")}',
      }},
      fontFamily: {{
        sans: ['{typography.get("font_family", "Inter, sans-serif")}'],
      }},
    }},
  }},
  plugins: [],
}}"""
    
    def _generate_global_css(self, design_system: Dict) -> str:
        """Generate global CSS"""
        return """@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply antialiased;
  }
}"""
    
    def _generate_package_json(self, framework: str) -> str:
        """Generate package.json"""
        if framework == 'react':
            return """{
  "name": "ui2code-generated",
  "version": "1.0.0",
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "tailwindcss": "^3.3.0",
    "autoprefixer": "^10.4.14",
    "postcss": "^8.4.24"
  },
  "scripts": {
    "dev": "vite",
    "build": "vite build"
  }
}"""
        return "{}"
    
    def _extract_components(self, hierarchy: Dict) -> Dict:
        """Extract reusable components from hierarchy"""
        components = {}
        
        if 'children' in hierarchy:
            for child in hierarchy['children']:
                comp_name = child.get('componentName', '')
                if comp_name and child.get('type') not in ['page', 'main']:
                    components[comp_name] = child
                
                # Recursively extract
                components.update(self._extract_components(child))
        
        return components
    
    def _indent(self, text: str, levels: int = 1) -> str:
        """Indent text by specified levels"""
        indent = '  ' * levels
        return '\n'.join([indent + line if line.strip() else line 
                         for line in text.split('\n')])
    
    def _to_kebab_case(self, text: str) -> str:
        """Convert text to kebab-case"""
        import re
        text = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', text)
        text = re.sub('([a-z0-9])([A-Z])', r'\1-\2', text)
        return text.lower()
