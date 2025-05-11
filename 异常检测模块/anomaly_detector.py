import numpy as np
from collections import deque
import logging
import tensorrt as trt
import pycuda.driver as cuda

class AnomalyDetector:
    def __init__(self, model_path: str, threshold_config: dict):
        """
        增强版异常检测模块
        :param model_path: TensorRT引擎文件路径
        :param threshold_config: 阈值配置
        """
        self.logger = logging.getLogger('hydro.detector')
        self.model = self._load_trt_engine(model_path)
        self.threshold_calculator = DynamicThreshold(
            window_size=threshold_config['window_size'],
            quantile=threshold_config['quantile']
        )
        self.context = self.model.create_execution_context()
        
    def detect(self, data_window: np.ndarray) -> dict:
        """
        增强检测方法，支持批量处理
        :param data_window: 输入数据窗口 (shape: [batch_size, seq_len, features])
        :return: 检测结果列表
        """
        if len(data_window.shape) == 2:
            data_window = np.expand_dims(data_window, axis=0)
            
        batch_results = []
        for i in range(data_window.shape[0]):
            try:
                pred = self._infer(data_window[i])
                anomaly_prob = self._calc_anomaly_score(data_window[i], pred)
                threshold = self.threshold_calculator.update(anomaly_prob)
                
                batch_results.append({
                    'index': i,
                    'probability': float(anomaly_prob),
                    'threshold': float(threshold),
                    'is_anomaly': anomaly_prob > threshold
                })
            except Exception as e:
                self.logger.error(f"检测第{i}个样本失败: {str(e)}")
                batch_results.append({
                    'index': i,
                    'error': str(e)
                })
                
        return batch_results

    def _load_trt_engine(self, engine_path):
        """加载TensorRT引擎"""
        logger = trt.Logger(trt.Logger.WARNING)
        with open(engine_path, 'rb') as f, trt.Runtime(logger) as runtime:
            return runtime.deserialize_cuda_engine(f.read())

def test_threshold_calculation():
            """测试动态阈值计算"""
            detector = AnomalyDetector("models/bilstm_v2.trt",
                                       {"window_size": 100, "quantile": 0.98})
            # 模拟100个正常数据点
            normal_scores = np.random.normal(0.2, 0.05, 100)
            for score in normal_scores:
                detector.threshold_calculator.update(score)
            # 测试异常点检测
            assert detector.threshold_calculator.update(0.8) > 0.5