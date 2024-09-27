import unittest
from unittest.mock import patch, Mock
from oslo_api import OsloAPI


class TestOsloAPI(unittest.TestCase):

    def setUp(self):
        self.api = OsloAPI("https://app.oslo.vision/api/v1", "test_token")

    @patch("oslo_api.client.requests.request")
    def test_test_api(self, mock_request):
        # Set up the mock
        mock_response = Mock()
        mock_response.json.return_value = {"msg": "Hello World!"}
        mock_request.return_value = mock_response

        # Call the method
        result = self.api.test_api()

        # Assert the result
        self.assertEqual(result, {"msg": "Hello World!"})

        # Assert the mock was called correctly
        mock_request.assert_called_once_with(
            "GET",
            "https://app.oslo.vision/api/v1/",
            headers={"Authorization": "Bearer test_token"},
        )

    @patch("oslo_api.client.requests.request")
    def test_add_image(self, mock_request):
        # Set up the mock
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": "test_image_id",
            "url": "https://example.com/image.jpg",
            "split": "train",
            "status": "pending",
        }
        mock_request.return_value = mock_response

        # Call the method
        with open("test_image.jpg", "rb") as img_file:
            result = self.api.add_image("test_project", img_file)

        # Assert the result
        self.assertEqual(result["id"], "test_image_id")
        self.assertEqual(result["split"], "train")

        # Assert the mock was called correctly
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        self.assertEqual(call_args[0][0], "POST")
        self.assertEqual(call_args[0][1], "https://app.oslo.vision/api/v1/images")
        self.assertIn("files", call_args[1])
        self.assertIn("data", call_args[1])
        self.assertEqual(call_args[1]["data"]["project_identifier"], "test_project")

    @patch("oslo_api.client.requests.request")
    def test_create_annotation(self, mock_request):
        # Set up the mock
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": "test_annotation_id",
            "image_identifier": "test_image_id",
            "label": "cat",
            "x0": 10,
            "y0": 20,
            "width_px": 100,
            "height_px": 150,
        }
        mock_request.return_value = mock_response

        # Call the method
        result = self.api.create_annotation(
            "test_project", "test_image_id", "cat", 10, 20, 100, 150
        )

        # Assert the result
        self.assertEqual(result["id"], "test_annotation_id")
        self.assertEqual(result["label"], "cat")

        # Assert the mock was called correctly
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        self.assertEqual(call_args[0][0], "POST")
        self.assertEqual(call_args[0][1], "https://app.oslo.vision/api/v1/annotations")
        self.assertIn("json", call_args[1])
        self.assertEqual(call_args[1]["json"]["project_identifier"], "test_project")
        self.assertEqual(call_args[1]["json"]["image_identifier"], "test_image_id")

    @patch("oslo_api.client.requests.request")
    def test_download_export(self, mock_request):
        # Set up the mock
        mock_response = Mock()
        mock_response.status_code = 302
        mock_response.headers = {"Location": "https://example.com/download/export.zip"}
        mock_request.return_value = mock_response

        # Call the method
        result = self.api.download_export("test_project", 1)

        # Assert the result
        self.assertEqual(result, "https://example.com/download/export.zip")

        # Assert the mock was called correctly
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        self.assertEqual(call_args[0][0], "GET")
        self.assertEqual(call_args[0][1], "https://app.oslo.vision/api/v1/exports/1")
        self.assertIn("params", call_args[1])
        self.assertEqual(call_args[1]["params"]["project_identifier"], "test_project")


if __name__ == "__main__":
    unittest.main()
