from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    full_name = fields.Str(validate=validate.Length(min=1, max=64), required=True)
    login = fields.Str(validate=validate.Length(min=5, max=24), required=True)
    password = fields.Str(validate=validate.Length(min=5, max=80), required=True)
    email = fields.Email(required=True)

class LoginSchema(Schema):
    login = fields.Str(validate=validate.Length(min=5, max=24), required=True)
    password = fields.Str(validate=validate.Length(min=5, max=80), required=True)

class ValidateUserFieldsSchema(Schema):
    full_name = fields.Str(validate=validate.Length(min=1, max=64))
    login = fields.Str(validate=validate.Length(min=5, max=24))
    password = fields.Str(validate=validate.Length(min=5, max=48))
    email = fields.Email()

class MajorSchema(Schema):
    name = fields.Str(validate=validate.Length(min=1, max=80), required=True)

class SubjectSchema(Schema):
    name = fields.Str(validate=validate.Length(min=1, max=80), required=True)

class MarkSchema(Schema):
    subject = fields.Nested(SubjectSchema, required=True)
    grade = fields.Integer(required=True)

class StudentSchema(Schema):
    name = fields.Str(validate=validate.Length(min=1, max=64), required=True)
    major = fields.Nested(MajorSchema, required=True)
    rating = fields.Integer(required=True)
    marks = fields.List(fields.Nested(MarkSchema))

class ValidateStudentFieldsSchema(Schema):
    id = fields.Integer()
    name = fields.Str(validate=validate.Length(min=1, max=64))
    major = fields.Nested(MajorSchema)
    rating = fields.Integer()
    marks = fields.List(fields.Nested(MarkSchema))