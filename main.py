import os

import pandas as pd

from dotenv import load_dotenv

from freelancers_service import FreelancerInfoService

load_dotenv()


if __name__ == "__main__":
    csv_path = "data/freelancer_earnings_bd.csv"

    if not os.path.isfile(csv_path):
        print(f"Ошибка: CSV-файл не найден по пути {csv_path}")
        exit(1)

    df = pd.read_csv(csv_path)

    freelancer_service = FreelancerInfoService(df)

    print("Введите запросы к данным (exit для выхода):")
    while True:
        request = input(">> ").strip()
        if request.lower() in {"exit", "quit"}:
            break

        result = freelancer_service.on_request(request)
        print(result)
