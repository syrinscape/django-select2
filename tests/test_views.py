import json
import unittest

from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.test import RequestFactory

from django_select2.views import AutoResponseView, Select2View


class Select2ErrorTests(unittest.TestCase):
    def test_missing_field_returns_json_not_found(self):
        response = AutoResponseView.as_view()(RequestFactory().get("/"))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            json.loads(response.content.decode("utf-8")),
            {"err": "field_id not found or is invalid", "more": False, "results": []},
        )

    def test_exception_text_and_status_survive_json_serialisation(self):
        custom_error = Exception("Please retry")
        custom_error.status_code = 429
        for exception, status in [
            (Http404("Missing field"), 404),
            (PermissionDenied("Accès denied"), 400),
            (custom_error, 429),
        ]:
            with self.subTest(exception=exception):
                response = Select2View().respond_with_exception(exception)
                self.assertEqual(response.status_code, status)
                self.assertEqual(
                    json.loads(response.content.decode("utf-8")),
                    {"err": str(exception), "more": False, "results": []},
                )
