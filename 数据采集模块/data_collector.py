import os
import requests
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException
from retrying import retry
import logging
from typing import Dict, Any

class DataCollector:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.logger = logging.getLogger('hydro.data_collector')

    @retry(
        stop_max_attempt_number=5,
        wait_exponential_multiplier=1000,
        retry_on_exception=lambda e: isinstance(e, (ModbusIOException, requests.Timeout))
    def collect_data(self, sensor_id: str) -> Dict[str, Any]:
        sensor_info = self._get_sensor_config(sensor_id)
        protocol = sensor_info['protocol'].lower()
        
        try:
            if protocol == 'modbus':
                return self._read_modbus(sensor_info)
            elif protocol == 'http':
                return self._fetch_http(sensor_info)
            elif protocol == 'mock':
                return self._generate_mock_data(sensor_info)
            else:
                raise ValueError(f"Unsupported protocol: {protocol}")
        except Exception as e:
            self.logger.error(f"Failed to collect {sensor_id}: {str(e)}")
            raise

    def _read_modbus(self, config: Dict) -> Dict:
        client = ModbusTcpClient(
            host=os.getenv('MODBUS_HOST', config['host']),
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