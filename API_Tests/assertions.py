# Validate HTTP status code
def validate_status_code(response, expected_status):

    # Verify response status code
    assert response.status == expected_status


# Validate field value inside JSON response
def validate_json_field(response_body, field_name, expected_value):

    # Verify field value matches expected value
    assert response_body[field_name] == expected_value


# Validate field exists and is not empty
def validate_field_exists(response_body, field_name):

    # Verify field exists and has value
    assert response_body[field_name] is not None