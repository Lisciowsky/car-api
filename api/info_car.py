import requests


def car_info(model, make):
    base_url = f"https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{model.upper()}?format=json"
    try:
        x = requests.get(base_url)
        for i in range(len(x.json()["Results"])):
            if x.json()["Results"][i]["Model_Name"] == f"{make.upper()}":
                return True
    except Exception:
        pass

    return False
