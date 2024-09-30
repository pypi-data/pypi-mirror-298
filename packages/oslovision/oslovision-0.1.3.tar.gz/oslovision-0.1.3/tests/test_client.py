import unittest
from unittest.mock import patch, Mock
import os
import sys
import io
import zipfile
import tempfile


# Add the src directory to the Python path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)
from oslovision import OsloVision


class TestOsloVision(unittest.TestCase):

    def setUp(self):
        self.api = OsloVision("test_token")

    @patch("oslovision.client.requests.request")
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

    @patch("oslovision.client.requests.request")
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
        with open("./test_image.jpg", "rb") as img_file:
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

    @patch("oslovision.client.requests.request")
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

    @patch("oslovision.client.requests.request")
    def test_download_export(self, mock_request):
        # Create a mock zip file
        mock_zip_content = io.BytesIO()
        with zipfile.ZipFile(mock_zip_content, "w") as mock_zip:
            mock_zip.writestr("test_file.txt", "This is a test file")

        # Set up the mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/zip"}
        mock_response.content = mock_zip_content.getvalue()
        mock_request.return_value = mock_response

        # Create a temporary directory for the test
        with tempfile.TemporaryDirectory() as temp_dir:
            # Call the method
            output_path = self.api.download_export("test_project", 1, temp_dir)

            # Assert the mock was called correctly
            mock_request.assert_called_once_with(
                "GET",
                "https://app.oslo.vision/api/v1/exports/1",
                params={"project_identifier": "test_project"},
                headers={"Authorization": "Bearer test_token"},
                allow_redirects=True,
                stream=True,
            )

            # Check if the file was "unzipped"
            extracted_file_path = os.path.join(temp_dir, "test_file.txt")
            self.assertTrue(os.path.exists(extracted_file_path))

            # Check the content of the "unzipped" file
            with open(extracted_file_path, "r") as f:
                content = f.read()
                self.assertEqual(content, "This is a test file")

    @patch("oslovision.client.requests.request")
    def test_download_export_not_zip(self, mock_request):
        # Set up the mock response for a non-zip file
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "text/plain"}
        mock_response.content = b"This is not a zip file"
        mock_request.return_value = mock_response

        # Create a temporary directory for the test
        with tempfile.TemporaryDirectory() as temp_dir:
            # Call the method and expect a ValueError
            with self.assertRaises(ValueError) as context:
                self.api.download_export("test_project", 1, temp_dir)

            self.assertTrue(
                "The downloaded content is not a zip file" in str(context.exception)
            )

    @patch("oslovision.client.requests.request")
    def test_download_export_http_error(self, mock_request):
        # Set up the mock response for an HTTP error
        mock_response = Mock()
        mock_response.status_code = 404
        mock_request.return_value = mock_response

        # Create a temporary directory for the test
        with tempfile.TemporaryDirectory() as temp_dir:
            # Call the method and expect an Exception
            with self.assertRaises(Exception) as context:
                self.api.download_export("test_project", 1, temp_dir)

            self.assertTrue(
                "Failed to download export: HTTP 404" in str(context.exception)
            )


if __name__ == "__main__":
    unittest.main()
