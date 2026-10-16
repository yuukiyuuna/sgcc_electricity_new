import os

# 国网电力官网
LOGIN_URL = "https://www.95598.cn/osgweb/login"
ELECTRIC_USAGE_URL = "https://www.95598.cn/osgweb/electricityCharge"
BALANCE_URL = "https://www.95598.cn/osgweb/userAcc"
BILL_SUMMARY_URL = "https://www.95598.cn/osgweb/electricityCharge"
STEP_ELECTRICITY_URL = "https://www.95598.cn/osgweb/stepElectricityConsumption"
ELECTRIC_BILL_SUMMARY_URL = (
    "https://www.95598.cn/osgweb01/electricityChargeQuery/queryElectricBillSummary"
)

# Home Assistant
SUPERVISOR_URL = "http://supervisor/core"
API_PATH = "/api/states/"

BALANCE_SENSOR_NAME = "sensor.electricity_charge_balance"
DAILY_USAGE_SENSOR_NAME = "sensor.last_electricity_usage"
YEARLY_USAGE_SENSOR_NAME = "sensor.yearly_electricity_usage"
YEARLY_CHARGE_SENSOR_NAME = "sensor.yearly_electricity_charge"
MONTH_USAGE_SENSOR_NAME = "sensor.month_electricity_usage"
MONTH_CHARGE_SENSOR_NAME = "sensor.month_electricity_charge"
MONTH_VALLEY_SENSOR_NAME = "sensor.month_valley_usage"
MONTH_FLAT_SENSOR_NAME = "sensor.month_flat_usage"
MONTH_PEAK_SENSOR_NAME = "sensor.month_peak_usage"
MONTH_TIP_SENSOR_NAME = "sensor.month_tip_usage"
PREPAY_BALANCE_SENSOR_NAME = "sensor.prepay_balance"
BALANCE_UNIT = "CNY"
USAGE_UNIT = "KWH"

LLM_API_KEY = os.getenv('LLM_API_KEY', '').strip()
LLM_BASE_URL = os.getenv('LLM_BASE_URL', 'https://api.siliconflow.cn/v1')
LLM_MODEL = os.getenv('LLM_MODEL', 'Qwen/Qwen3.5-35B-A3B')


def get_data_dir() -> str:
    """获取数据存储目录：Docker 用 /data，本地用项目下的 data/"""
    if 'PYTHON_IN_DOCKER' in os.environ:
        return '/data'
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


def build_llm_extra_kwargs() -> dict:
    """构建各家 LLM 所需的额外请求参数。

    DeepSeek 思考模式默认开启，思维链(reasoning_content)与最终回答(content)
    共用 max_tokens 预算，容易导致 content 返回空字符串、验证码识别失败。
    因此仅针对 DeepSeek 关闭思考模式；其他 OpenAI 兼容服务商（如硅基流动 Qwen）
    不认识该参数，故不下发，避免报错。
    """
    base_url = (os.getenv('LLM_BASE_URL') or LLM_BASE_URL or '').lower()
    if 'deepseek' in base_url:
        return {"extra_body": {"thinking": {"type": "disabled"}}}
    return {}

