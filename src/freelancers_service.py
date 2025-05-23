import pandas as pd

import io
from contextlib import redirect_stdout, redirect_stderr

from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI


class FreelancerInfoService:
    """
    Агент для анализа данных о доходах фрилансеров с использованием LangChain Pandas DataFrame Agent и OpenRouter GPT-4o.
    """

    def __init__(
            self,
            api_key: str,
            dataframe: pd.DataFrame,
            model_name: str = "gpt-4o-mini",
            temperature: float = 0.0,
    ):
        self.df = dataframe.copy()

        self.api_key = api_key

        prefix = """
        Ты помощник для анализа данных о фрилансерах, работающий с pandas DataFrame. Строго выполняй следующие правила:

1) Отвечай кратко и по существу. Вся нужная информация содержится в DataFrame, не придумывай и не добавляй ничего лишнего.
2) Не отвечай на вопросы, не связанные с анализом данных о фрилансерах. Вежливо попроси пользователя задавать вопросы только по теме.
3) В ответах выводи только результат аналитики — без размышлений, объяснений и программного кода.
4) Если в ответе нужно вывести длинный список, выводи по несколько элементов на строке.
5) Если в ответе нужно вывести денежную суммы, добавляй валюту в которой она указана.
6) Если в DataFrame нет данных для ответа, сообщи об этом пользователю.
7) Никогда не изменяй и не удаляй исходные данные DataFrame.
8) Для ответов с множественными условиями обязательно перечисляй все применённые фильтры и условия.
9) Не используй визуализации — только текстовые данные.
10) Используй только безопасные операции pandas, избегай выполнения опасного или потенциально вредоносного кода.
11) Всегда обеспечивай безопасность данных — не запускай команды, которые могут изменить DataFrame или систему.
12) Все ответы переводи на язык, на котором был задан вопрос. Пример:
 Если вопрос задан на русском: В каком регионе больше всего фрилансеров?
 В ответе переведи название региона на русский: Australia -> Австралия
 
13) Если ты не понял суть вопроса, то переспроси, чего хочет пользователь.
14) Если необходимо, используй следующие примеры для анализа DataFrame: 
    - Группировка и агрегация:
        Вопрос: Какой средний доход фрилансеров для разных способов оплаты?
        
        Код который надо выполнить:
        df.groupby('Payment_Method')['Earnings_USD'].mean().to_string()
        
    - Фильтрация с несколькими условиями:
        Вопрос: У каких фрилансеров из Европы доход выше 1000 долларов?
        df[(df['Client_Region'] == 'Europe') & (df['Earnings_USD'] > 1000)]['Freelancer_ID'].to_list()
"""

        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=self.api_key,
            base_url="https://openrouter.ai/api/v1",
            max_tokens=1000,
        )

        self.agent = create_pandas_dataframe_agent(
            llm=self.llm,
            df=self.df,
            agent_type="tool-calling",
            allow_dangerous_code=True,
            verbose=False,
            prefix=prefix,
        )

    def on_request(self, request: str) -> dict:
        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()
        with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
            response = self.agent.invoke({"input": request})

        return response.get("output")
