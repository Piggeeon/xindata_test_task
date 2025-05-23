import pandas as pd

from src.freelancers_service import FreelancerInfoService
from src.config import OPENAI_API_KEY, PATH_TO_FREELANCERS_DATA


if __name__ == "__main__":
    csv_path = PATH_TO_FREELANCERS_DATA

    df = pd.read_csv(csv_path)

    freelancer_service = FreelancerInfoService(dataframe=df, api_key=OPENAI_API_KEY)

    print("Введите запросы к данным (exit для выхода):")
    while True:
        request = input(">> ").strip()
        request = request.encode('utf-8', 'replace').decode('utf-8')
        if request.lower() == 'exit':
            break

        result = freelancer_service.on_request(request)
        print(result)
