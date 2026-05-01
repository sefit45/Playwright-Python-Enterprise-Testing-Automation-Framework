# =========================================================
# Assertion utilities for API validation
# ספריית בדיקות ואימותים עבור API
# =========================================================


# Validate HTTP status code
def validate_status_code(response, expected_status):

    # Get actual status code from response
    actual_status = response.status

    # Assert with clear error message
    assert actual_status == expected_status, (
        f"Expected status code {expected_status}, "
        f"but got {actual_status}"
    )


# Validate field value inside JSON response
def validate_json_field(response_body, field_name, expected_value):

    # Get actual field value
    actual_value = response_body.get(field_name)

    # Assert with detailed message
    assert actual_value == expected_value, (
        f"Field '{field_name}' validation failed: "
        f"expected '{expected_value}', got '{actual_value}'"
    )


# Validate field exists and is not empty
def validate_field_exists(response_body, field_name):

    # Check if field exists
    assert field_name in response_body, (
        f"Field '{field_name}' is missing in response"
    )

    # Check if field has value
    assert response_body[field_name] is not None, (
        f"Field '{field_name}' is None"
    )