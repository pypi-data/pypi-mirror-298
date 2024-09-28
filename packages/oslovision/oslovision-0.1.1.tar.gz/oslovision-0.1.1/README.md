# OsloVision Python Client

This Python package provides a client for interacting with the Oslo API, a platform for creating and managing datasets for machine learning projects. The client allows you to easily upload images, create annotations, and download dataset exports.

## Features

- Simple interface for interacting with the Oslo API
- Support for adding images to projects
- Creation of annotations for images
- Downloading of dataset exports
- Automatic handling of authentication

## Installation

You can install the Oslo API Python client using pip:

```bash
pip install oslovision
```

## Usage

Here's a quick example of how to use the Oslo API client:

```python
from oslovision import OsloVision

# Initialize the client
api = OsloVision("your_api_token_here")

# Test the API connection
print(api.test_api())

# Add an image to a project
with open("image.jpg", "rb") as img_file:
    image_data = api.add_image("your_project_identifier", img_file)
print(f"Added image: {image_data['id']}")

# Create an annotation
annotation = api.create_annotation(
    "your_project_identifier",
    image_data['id'],
    "cat",
    x0=10,
    y0=20,
    width_px=100,
    height_px=150
)
print(f"Created annotation: {annotation['id']}")

# Download an export
download_url = api.download_export("your_project_identifier", 1)
print(f"Export download URL: {download_url}")
```

## API Reference

### OsloVision(base_url: str, token: str)

Initialize the Oslo API client.

- `base_url`: The base URL of the Oslo API (e.g., "https://app.oslo.vision/api/v1")
- `token`: Your Oslo API authentication token

### Methods

#### test_api() -> Dict[str, str]

Test if the API is up and running and the token is valid.

#### add_image(project_identifier: str, image: Union[str, IOBase], split: str = "train", status: str = "pending") -> Dict

Add an image to a project.

- `project_identifier`: The ID of the project to add the image to
- `image`: Either a file object or a URL string of the image
- `split`: The dataset split for the image (default: "train")
- `status`: The status of the image (default: "pending")

Returns a dictionary with the added image's data.

#### create_annotation(project_identifier: str, image_identifier: str, label: str, x0: float, y0: float, width_px: float, height_px: float) -> Dict

Create a new annotation for an image.

- `project_identifier`: The ID of the project
- `image_identifier`: The ID of the image to annotate
- `label`: The label for the annotation
- `x0`, `y0`: The top-left coordinates of the bounding box
- `width_px`, `height_px`: The width and height of the bounding box in pixels

Returns a dictionary with the created annotation's data.

#### download_export(project_identifier: str, version: int) -> str

Get the download URL for a dataset export.

- `project_identifier`: The ID of the project
- `version`: The version number of the export

Returns the download URL as a string.

## Contributing

Contributions to the Oslo API Python client are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.