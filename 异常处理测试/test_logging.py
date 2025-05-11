import logging
from io import StringIO


def test_error_logging():
    """测试错误日志记录"""
    log_stream = StringIO()
    handler = logging.StreamHandler(log_stream)
    logger = logging.getLogger('hydro.detector')
    logger.addHandler(handler)

    # 触发一个错误
    detector = AnomalyDetector("invalid_path.trt", {"window_size": 10, "quantile": 0.95})
    detector.detect(np.random.randn(1, 10))

    logs = log_stream.getvalue()
    assert "加载模型失败" in logs