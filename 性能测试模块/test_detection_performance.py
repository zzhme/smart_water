def test_detection_performance():
    """测试异常检测性能"""
    detector = AnomalyDetector("models/bilstm_v2.trt",
                               {"window_size": 100, "quantile": 0.98})
    large_data = np.random.randn(1000, 10, 6)  # 1000个样本

    start = time.time()
    results = detector.detect(large_data)
    duration = time.time() - start

    assert duration < 2.0  # 要求1000个样本处理时间<2秒
    assert len(results) == 1000