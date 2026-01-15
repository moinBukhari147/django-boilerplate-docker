from rest_framework.renderers import JSONRenderer


class SuccessJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get("response")

        # If error, return as-is (your custom_exception_handler already wrapped it)
        if not response or not 200 <= response.status_code < 300:  # noqa: PLR2004
            return super().render(data, accepted_media_type, renderer_context)

        # Already wrapped manually? Skip
        if isinstance(data, dict) and "success" in data and "data" in data:
            return super().render(data, accepted_media_type, renderer_context)

        # Wrap success payload
        standard = {
            "success": True,
            "status_code": response.status_code,
            "message": "Request processed successfully.",
            "data": data,
        }
        return super().render(standard, accepted_media_type, renderer_context)
