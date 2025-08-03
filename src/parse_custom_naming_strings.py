"""Extract column names from CL-passed arg of a file naming template."""


import re


def validate_template_syntax(template_string: str) -> None:
    """
    Checks a template string for syntax errors and provides specific feedback.

    Args:
        template_string: The raw template string from the user.

    Raises:
        ValueError: If a syntax error is found.
    """
    # Check for an equal number of opening and closing braces
    if template_string.count('{') != template_string.count('}'):
        raise ValueError(
            f"Syntax error in template '{template_string}': Mismatched curly braces."
        )

    # Find all potential placeholders and check for invalid characters
    # This pattern is loose and captures anything between braces
    potential_keys = re.findall(r'\{([^\}]+)\}', template_string)
    
    for key in potential_keys:
        # Check if the captured key contains anything other than word characters or dots
        if not re.fullmatch(r'[\w.]+', key):
            raise ValueError(
                f"Syntax error in template '{template_string}': "
                f"Placeholder '{{{key}}}' contains invalid characters. "
                "Only letters, numbers, underscores, and periods are allowed."
            )


def extract_template_keys(template_string: str) -> list[str]:
    """
    Extracts all column names cited in the file-naming or output-grouping template.
    
    Args:
        template_string: The template passed through the CL arg.custom_filename_template.
        
    Returns:
        A list of strings, where each string is a column name.
    """
    pattern = r'\{([\w.]+)\}' # anything in '{}_{}' or '{}/{}'
    return re.findall(pattern, template_string)




