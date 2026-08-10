def assert_no_edge_spaces(password: str, field_name: str = "password") -> None:

    if password != password.strip():
        raise ValueError(f"{field_name} cannot start or end with a space")