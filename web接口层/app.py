from flask import Flask, jsonify
from core.data_collector import DataCollector
from core.anomaly_detector import AnomalyDetector

app = Flask(__name__)

# 初始化核心组件
data_collector = DataCollector("config/sensor_config.yaml")
anomaly_detector = AnomalyDetector(
    model_path="models/bilstm_v2.trt",
    threshold_config={"window_size": 100, "quantile": 0.98}
)

@app.route('/api/sensor/<sensor_id>', methods=['GET'])
def get_sensor_data(sensor_id):
    try:
        raw_data = data_collector.collect_data(sensor_id)
        processed = preprocess_data(raw_data)
        return jsonify(processed)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/detect', methods=['POST'])
def detect_anomalies():
    data = request.get_json()
    window = np.array(data['values'])
    results = anomaly_detector.detect(window)
    return jsonify({"results": results})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


    def test_api_authentication():
        """测试API接口认证"""
        with app.test_client() as client:
            response = client.post('/api/detect', json={'values': [[1.0, 2.0]]})
            assert response.status_code == 401  # 应添加认证