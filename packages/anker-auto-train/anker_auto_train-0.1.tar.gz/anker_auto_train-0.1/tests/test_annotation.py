from fastapi.testclient import TestClient
from app.router.annotation import router
from app.main import app
from unittest.mock import patch, MagicMock
from app.services.services import process_annotation_data

client = TestClient(app)

app.include_router(router)


def process_annotation_data_mock(data):
    return 1


def process_annotation_data_invalid_mock(data):
    return None


def process_annotation_data_error_mock(data):
    raise Exception("Mock error")


@patch('app.services.services.process_annotation_data', side_effect=process_annotation_data_mock)
def test_upload_annotation_success(mock_process_annotation_data):
    response = client.post("/data/annotation", json={
        "annotationType": "object",
        "annotationVersionId": "",
        "bg": "zx",
        "dataId": [
            "60f7e74e0c1c9e17alfle8b7"
        ],
        "labelInfo": [
            {
                "bbox_xyxy": [
                    100,
                    200,
                    150,
                    300
                ],
                "label": "wire",
                "labelType": 0,
                "score": 0.9
            }
        ],
        "labelMethod": "auto",
        "labelScope": [
            "wire",
            "pop"
        ],
        "modelName": "YOLOv5",
        "modelVersion": "1.0.0",
        "others": {
            "anything": "is ok"
        },
        "owner": "eric.nan",
        "bg": "zx",
        "reviewed": 0,
        "reviewedBy": ""
    })
    print(response.content)
    assert response.status_code == 200


