from marshmallow import Schema, fields
from flask import abort

class LLMRequestSchema(Schema):
    prompt = fields.Str(required=True)

class LLMRequestSchemaForImagePrompt(LLMRequestSchema):
    theme = fields.Str(required=True)

def validate_request_schema(request):
    validation_error = None
    match request.path:
        case '/llm-json-response':
            payload = request.json
            validation_error = LLMRequestSchema().validate(payload)
        case '/layout-from-pdf':
            # check if file has been uploaded
            file = request.files['file']
            if not file:
                # raise error
                validation_error = "File not sent in request"
        case '/llm-image-prompt':
            payload = request.json
            validation_error = LLMRequestSchemaForImagePrompt().validate(payload)
    if validation_error:
        abort(400, description=str(validation_error))
