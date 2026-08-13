import os, time

from pydexcom import Dexcom
from dotenv import load_dotenv
from dexcom_paper_display.utils import Display

UNICODE_ARROWS_MAP = {
    # If pydexcom returns string names
    "DoubleUp": "\uf062\uf062",
    "SingleUp": "\uf062",
    "FortyFiveUp": "\uf176",
    "Flat": "\uf061",
    "FortyFiveDown": "\uf175",
    "SingleDown": "\uf063",
    "DoubleDown": "\uf063\uf063",
}

class Credentials:
    def __init__(self):
        self.username = os.getenv("USERNAME")
        self.password = os.getenv("PASSWORD")

def get_dexcom_data() -> dict:
    credentials = Credentials()
    dexcom = Dexcom(
        username=credentials.username,
        password=credentials.password,
        region="ous"
        )
    current_reading = dexcom.get_current_glucose_reading()
    # TODO: Error handling, if return trend name doesn't fit mapping...
    trend_arrow_unicode = UNICODE_ARROWS_MAP[current_reading.trend_direction] if current_reading.trend_direction in UNICODE_ARROWS_MAP else "\uf128"
    return {
        "glucose_reading": str(current_reading.value),
        "trend_arrow": str(trend_arrow_unicode)
    }

def main():
    print("Startup")
    load_dotenv()
    epd = Display(os.getenv("DISPLAYTYPE"))
    while(True):
        data = get_dexcom_data()
        print("Latest data: {0} {1}".format(data["glucose_reading"],data["trend_arrow"]))
        epd.display_image("{0} {1}".format(data["glucose_reading"],data["trend_arrow"]))
        print("Start-Sleep 300")
        time.sleep(300)

if __name__ == "__main__":
    main()