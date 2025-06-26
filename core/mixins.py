from django.db.models import ProtectedError
from rest_framework import status
from rest_framework.response import Response


class DestroyProtectedMixin:
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError as protected_error:
            protected_elements = [
                {
                    "model": obj.__class__.__name__,
                    "id": str(obj.id),
                    "label": getattr(obj, "name", getattr(obj, "title", str(obj))),
                }
                for obj in protected_error.protected_objects
            ]
            response_data = {
                "detail": "Item cannot be deleted, it is referenced by other records.",
                "protected_elements": protected_elements,
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
