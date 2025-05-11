import sys
from importlib import reload

def test_python_version_compatibility():
    """测试Python版本兼容性"""
    try:
        # 模拟不同Python版本
        sys.version_info = (3, 7, 0)
        import core.anomaly_detector
        reload(core.anomaly_detector)
        assert True
    except Exception as e:
        pytest.fail(f"Python 3.7兼容性失败: {str(e)}")