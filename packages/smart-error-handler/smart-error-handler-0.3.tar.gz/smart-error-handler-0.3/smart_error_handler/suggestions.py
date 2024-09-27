def get_suggestions(error_type):
    suggestions={
        "Syntax Error": [
            "Check for missing parentheses or unmatched qotes.",
            "Ensure that indentation is consistent"
        ],
        "TypeError": [
            "Check if you are using the correct data type.",
            "Ensure that you are not trying to concatenate incompatible types."
        ],
        "ValueError": [
            "Check if the function arguments are valid.",
            "Verify that you are passing the expected range of values."

        ]
    }
    return suggestions.get(error_type, ["No suggestions available."])