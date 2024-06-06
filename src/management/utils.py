from dotenv import load_dotenv
from eskiz_sms import EskizSMS


load_dotenv()

eskiz = EskizSMS(
    "doossee.me@gmail.com",
    "V2gADtpVSPTCuIbAPKYtaHylyTtS0ZRXuNBmxR8Y",
    save_token=True,
    env_file_path=".env",
)


def send_sms(phone_number, message) -> bool:
    response = eskiz.send_sms(mobile_phone=phone_number, message=message)
    return response.status
