class ValidationError(Exception):
    pass

class MissingAttributeError(ValidationError):
    def __init__(self, slug: str):
        super().__init__(f"Missing required attribute '{slug}'")
        self.slug = slug

class UnexpectedAttributeError(ValidationError):
    def __init__(self, slug: str):
        super().__init__(f"Attribute '{slug}' is not allowed in this category")
        self.slug = slug

class WrongTypeError(ValidationError):
    def __init__(self, slug: str, expected: str):
        super().__init__(f"Attribute '{slug}' must be {expected}")
        self.slug = slug
        self.expected = expected
