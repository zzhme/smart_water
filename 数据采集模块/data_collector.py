import requests
from pymodbus.client import ModbusTcpClient
import yaml
from typing import Dict, Any
import logging
from retrying import retry

class DataCollector:
    def __init__(self, config_path: str):
        """
        增强版数据采集模块
        :param config_path: 配置文件路径
        """
        self.config = self._load_config(config_path)
        self.logger = logging.getLogger('hydro.data_collector')
        
    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def collect_data(self, sensor_id: str) -> Dict[str, Any]:
        """
        增强数据采集方法，支持重试机制
        :param sensor_id: 传感器唯一标识
        :return: 采集数据字典
        """
        sensor_info = self._get_sensor_config(sensor_id)
        protocol = sensor_info['protocol'].lower()
        
        try:
            if protocol == 'modbus':
                return self._read_modbus(sensor_info)
            elif protocol == 'http':
                return self._fetch_http(sensor_info)
            elif protocol == 'mock':  # 新增mock协议用于测试
                return self._generate_mock_data(sensor_info)
            else:
                raise ValueError(f"不支持的协议类型: {protocol}")
        except Exception as e:
            self.logger.error(f"采集{sensor_id}数据失败: {str(e)}")
            raise

    def _read_modbus(self, config: Dict) -> Dict:
        """增强Modbus采集实现"""
        client = ModbusTcpClient(
            host=config['host'],
            port=config.get('port', 502),
            timeout=config.get('timeout', 5)
        )
        
        try:
            client.connect()
            results = {}
            for param, reg in config['register_map'].items():
                response = client.read_holding_registers(reg['address'], reg['count'])
                results[param] = self._transform_value(response.registers, reg.get('scale', 1))
            return results
        finally:
            client.close()

    def _fetch_http(self, config: Dict) -> Dict:
        """增强HTTP采集实现"""
        response = requests.get(
            config['endpoint'],
            headers=config.get('headers', {}),
            timeout=config.get('timeout', 10)
        )
        response.raise_for_status()
        return response.json()

    def _generate_mock_data(self, config: Dict) -> Dict:
        """测试用mock数据生成"""
        from faker import Faker
        fake = Faker()
        return {
            'water_level': fake.pyfloat(min_value=0, max_value=20),
            'flow_rate': fake.pyfloat(min_value=0, max_value=10),
            'timestamp': fake.unix_time()
        }

def test_modbus_connection():
        """测试Modbus连接和读取"""
        config = {
            'protocol': 'modbus',
            'host': '192.168.1.100',
            'port': 502,
            'register_map': {
                'water_level': {'address': 0x01, 'count': 2, 'scale': 0.1}
            }
        }
        collector = DataCollector("config/sensor_config.yaml")
        result = collector._read_modbus(config)
        assert 'water_level' in result
        assert isinstance(result['water_level'], float)