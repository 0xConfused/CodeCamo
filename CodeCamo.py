import re
import random

# Define the variations for transforming object.property references
variations = [
    lambda obj, prop, a, b, c, d, vc, vc1, vc2: f"{obj}.{prop}",
    lambda obj, prop, a, b, c, d, vc, vc1, vc2: f"(function(){{{vc} {a}=\"{prop}\";return {obj}[{a}]}})()",
    lambda obj, prop, a, b, c, d, vc, vc1, vc2: f"{obj}[\"{prop}\"]",
    lambda obj, prop, a, b, c, d, vc, vc1, vc2: f"(function(){{with({obj}){{return {prop};}}}})()",
    lambda obj, prop, a, b, c, d, vc, vc1, vc2: f"(()=>{{{vc} {a}=new Proxy({obj},{{get:({b},{c})=>{c}==='{prop}'?{b}[{c}]:Reflect.get({b},{c})}});return {a}}})()['{prop}']",
    lambda obj, prop, a, b, c, d, vc, vc1, vc2: f"(()=>{{{vc}{{{prop}:l}}={obj};return l}})()",
    lambda obj, prop, a, b, c, d, vc, vc1, vc2: f"(function(){{{vc} {a}=Symbol();{vc1} {b}=new Proxy({obj},{{get:({c},prop)=>prop==={a}?{c}.{prop}:{c}[prop]}});{vc} {d}={b}[{a}];return {d}}})()"
]

# List of reserved JavaScript keywords
reserved_keywords = {
    'break', 'case', 'catch', 'class', 'const', 'continue', 'debugger', 'default', 'delete', 'do', 'else', 'enum', 'export', 'extends', 'false',
    'finally', 'for', 'function', 'if', 'import', 'in', 'instanceof', 'let', 'new', 'null', 'return', 'super', 'switch', 'this', 'throw', 'true',
    'try', 'typeof', 'var', 'void', 'while', 'with', 'yield'
}

# List of words related to front-end GUI development
words = [
    'component', 'render', 'state', 'props', 'context', 'hook', 'element', 'event', 'view', 'layout',
    'style', 'theme', 'route', 'navigation', 'animation', 'form', 'input', 'button', 'card', 'modal',
    'dropdown', 'tab', 'tooltip', 'header', 'footer', 'sidebar', 'grid', 'container', 'menu', 'list',
    'card', 'tooltip', 'dialog', 'carousel', 'badge', 'progress', 'spinner', 'image', 'icon', 'badge',
    'link', 'table', 'row', 'column', 'checkbox', 'radio', 'switch', 'pagination', 'breadcrumb', 'breadcrumb',
    'overlay', 'drawer', 'accordion', 'popover', 'file', 'upload', 'dialog', 'tooltip', 'badge', 'slider'
]

# List of short modifiers to append
mods = [
    'Add', 'Placement', 'Id', 'Handler', 'Manager', 'Controller', 'Service', 'Factory', 'Provider', 'Component'
]

# List of short words to prepend (all in lowercase)
pre_mods = [
    'base', 'core', 'main', 'primary', 'default', 'initial', 'new', 'custom', 'standard'
]

def generate_variable_name():
    base = random.choice([w for w in words if w not in reserved_keywords])
    pre = random.choice(pre_mods) if random.choice([True, False]) else ''
    post = random.choice(mods) if random.choice([True, False]) else ''
    return f"{pre}{base.capitalize() if pre else base}{post}"

def random_keyword():
    return random.choice(['var', 'const'])

# Function to apply a random transformation variation with constraint on eval chaining
def apply_transformation(obj, prop, last_variation):
    # Filter out variations that chain evals consecutively
    filtered_variations = [v for v in variations if not (last_variation and v.__code__.co_code == last_variation.__code__.co_code)]
    variation = random.choice(filtered_variations)
    result = variation(obj, prop, generate_variable_name(), generate_variable_name(), generate_variable_name(), generate_variable_name(), random_keyword(), random_keyword(), random_keyword())
    return result, variation

# Function to transform JS code
def transform_js_code(js_code):
    # Define the regex pattern for matching object.property chains
    pattern = re.compile(r'(?P<obj>(?:\w+\.)+)(?P<prop>\w+)')

    last_variation = None

    # Function to replace matches with transformed patterns
    def replace_match(match):
        nonlocal last_variation
        obj = match.group('obj')[:-1]  # Remove trailing dot
        prop = match.group('prop')
        transformed, last_variation = apply_transformation(obj, prop, last_variation)
        return transformed

    # Apply the transformation
    return pattern.sub(replace_match, js_code)

# Function to repeatedly transform JS code until no more patterns are found
def repeatedly_transform_js_code(js_code):
    prev_code = None
    current_code = js_code

    while current_code != prev_code:
        prev_code = current_code
        current_code = transform_js_code(current_code)

    return current_code

# Function to write transformed code to a file
def write_transformed_code(output_file, transformed_code):
    with open(output_file, 'w') as file:
        file.write(transformed_code)

# Function to transform the input JS file and write to the output file
def transform_js_file(input_file, output_file):
    # Read the input JS file
    with open(input_file, 'r') as file:
        js_code = file.read()

    # Repeatedly transform the JS code
    transformed_code = repeatedly_transform_js_code(js_code)

    # Write the transformed code to the output file
    write_transformed_code(output_file, transformed_code)

# Example usage
input_file = 'input.js'
output_file = 'output.js'
transform_js_file(input_file, output_file)
