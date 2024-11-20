from marshmallow import Schema, fields, validate, ValidationError

# Schema for user registration
class UserRegistrationSchema(Schema):
    firstName = fields.String(required=True, validate=validate.Length(min=2, max=80))
    lastName = fields.String(required=True, validate=validate.Length(min=2, max=80))
    email = fields.Email(required=True)
    password = fields.String(
        required=True,
        validate=validate.Regexp(
            r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$',
            error="Password must have at least 8 characters, one uppercase letter, one digit, and one special character."
        )
    )
    phoneNumber = fields.String(
        required=True,
        validate=validate.Regexp(r'^\d{10,15}$', error="Phone number must be numeric and 10-15 digits long.")
    )
    address = fields.String(validate=validate.Length(max=255))

# Schema for user login
class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

# Schema for updating user details
class UserUpdateSchema(Schema):
    email = fields.Email(required=True)
    firstName = fields.String(validate=validate.Length(min=2, max=80))
    lastName = fields.String(validate=validate.Length(min=2, max=80))
    phoneNumber = fields.String(
        validate=validate.Regexp(r'^\d{10,15}$', error="Phone number must be numeric and 10-15 digits long.")
    )
    address = fields.String(validate=validate.Length(max=255))
    password = fields.String(
        validate=validate.Regexp(
            r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$',
            error="Password must have at least 8 characters, one uppercase letter, one digit, and one special character."
        )
    )

# Schema for password verification and update
class PasswordChangeSchema(Schema):
    currentPassword = fields.String(required=True)
    newPassword = fields.String(
        required=True,
        validate=validate.Regexp(
            r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$',
            error="Password must have at least 8 characters, one uppercase letter, one digit, and one special character."
        )
    )