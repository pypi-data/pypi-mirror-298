import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.main import app
from unittest.mock import patch, MagicMock
from app.models.models import OriginData
from app.router.origin_data import  upload_raw_data_endpoint
from app.services.services import process_raw_data
client = TestClient(app)


def test_origin_data_validation():
    valid_json = {
  "uid": "string",
  "parentId": "string",
  "fileMeta": {
    "resolution": {
      "width": 1280,
      "height": 720
    },
    "tokenLenght": 80,
    "duration": 80
  },
  "type": "video",
  "region": "string",
  "securityLevel": "low",
  "storage": {
    "storageId": "ivstorage1",
    "bucket": "datavault-12",
    "objectName": "image/121/cat.png"
  },
  "bg": "ap",
  "owner": "shimei.xie",
  "extra": {
    "homebaseSn": "string",
    "deviceSn": "string",
    "projectId": "string",
    "userId": "string",
    "donateTimestamp": 0,
    "generateTimestamp": 0,
    "videoType": [
      "string"
    ],
    "comments": "string",
    "originalVideoType": "string",
    "caseId": "string",
    "donationId": "string",
    "localEventTime": "string",
    "videoTypeName": [],
    "donationType": "string",
    "feedbackVideoType": "string"
  },
  "sourceInfo": {
    "type": "trigger",
    "caseId": "string",
    "logUrl": "string",
    "collectReason": "string",
    "parameter": "string",
    "genReason": "string",
    "donateReason": "string",
    "donateSource": "string",
    "complaint": "string",
    "donateComment": "string",
    "triggerReason": "string",
    "model": [
      {
        "modelName": "modelname1",
        "modelVersion": "v1",
        "modelLocation": "homebase"
      }
    ],
    "uid": "string",
    "service": "string",
    "remark": "string"
  },
  "soundCoreField": {
    "content": "string",
    "space": "string",
    "noiseLevel": "string",
    "language": "string",
    "length": "string",
    "score": "string",
    "startIndex": "string",
    "endIndex": "string"
  }
}
    try:
        origin_data = OriginData(**valid_json)
    except ValidationError as e:
        pytest.fail(f"Validation failed: {e}")

    assert origin_data.uid == "string"
    assert origin_data.soundCoreField.content == "string"
    # 继续添加其他字段的断言