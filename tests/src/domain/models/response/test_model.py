from unittest.mock import patch, MagicMock
from src.domain.models.response.model import ResponseModel


@patch.object(ResponseModel, "to_dumps")
def test_return_none_result_if_not_passed_in_args(mocked_dumps):
    response_model = ResponseModel(MagicMock(), MagicMock())
    assert response_model.message is None
    assert response_model.result is None
