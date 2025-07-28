import re
import hashlib

def extract_and_replace_strings(js_code):
    # Regex pattern to match strings in single, double, or backtick quotes
    pattern = r'(?:\'\'\'(?:[^\'\\]*(?:\\.|\'[^\']|\'\'[^\'])?)+\'\'\'|\'(?:[^\'\\]*(?:\\.)?)+\'|`(?:[^`\\]*(?:\\.)?)+`|"(?:[^"\\]*(?:\\.)?)+")'
    # List to store extracted strings
    extracted_strings = []
    
    # Function to replace strings with hashed placeholders
    def replace_with_placeholder(match):
        string = match.group(0)
        extracted_strings.append(string)  # Add the string to the list
        # Generate a hash of the string and use it as the placeholder
        hash_placeholder = hashlib.md5(string.encode('utf-8')).hexdigest()
        return f'{hash_placeholder}'

    # Replace strings in the JavaScript code with hashed placeholders
    modified_js = re.sub(pattern, replace_with_placeholder, js_code)

    return modified_js, extracted_strings


def restore_strings(modified_js, extracted_strings):
    # Replace placeholders back with the original strings
    for i, placeholder in enumerate(extracted_strings):
        # Generate the hash of the string
        hash_placeholder = hashlib.md5(placeholder.encode('utf-8')).hexdigest()
        modified_js = modified_js.replace(f'{hash_placeholder}', placeholder)
    
    return modified_js


# Example usage
js_code = '''
const name = "Alice";
let greeting = 'Hello, world!';
const multiLine = `This is
a string with multiple lines`;
const escapedString = 'This has a \\ backslash';
'''

modified_js, extracted_strings = extract_and_replace_strings(js_code)

print("Modified JavaScript Code with Placeholders:")
print(modified_js)

print("\nExtracted Strings:")
print(extracted_strings)

# Restoring the strings back into the code
restored_js = restore_strings(modified_js, extracted_strings)

print("\nRestored JavaScript Code:")
print(restored_js)