def test_batch_processing_perf():
    # 生成1000个测试样本
    test_data = np.random.randn(1000, 10, 6)  
    
    start = time.time()
    results = detector.detect(test_data)
    elapsed = time.time() - start
    
    assert elapsed < 2.0  # 性能阈值
    assert len(results) == 1000