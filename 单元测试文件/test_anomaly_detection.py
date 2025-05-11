import pytest
import numpy as np
from unittest.mock import MagicMock
from core.anomaly_detector import AnomalyDetector

@pytest.fixture
def mock_detector():
    return AnomalyDetector(
        model_path="tests/mock_model.trt",
        threshold_config={
            "window_size": 50,
            "quantile": 0.95
        }
    )

def test_normal_detection(mock_detector):
    # 生成正常测试数据
    normal_data = np.random.normal(0, 0.1, (10, 6))
    results = mock_detector.detect(normal_data)
    
    assert len(results) == 10
    assert sum(res["is_anomaly"] for res in results) < 2  # 异常点不超过2个

def test_batch_processing(mock_detector):
    # 测试批量处理能力
    batch_data = np.random.randn(32, 10, 6)  # 批量32个样本
    results = mock_detector.detect(batch_data)
    
    assert len(results) == 32
    assert all(isinstance(res["probability"], float) for res in results)

def test_error_handling(mock_detector):
    # 测试异常输入处理
    invalid_data = np.array([[[np.nan]]])  # 包含NaN的数据
    results = mock_detector.detect(invalid_data)
    
    assert "error" in results[0]