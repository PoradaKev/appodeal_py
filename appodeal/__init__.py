import json
import pandas as pd
import requests
from datetime import datetime
from io import StringIO
from furl import furl
from tqdm import tqdm
from time import sleep
class Appodeal:
    
    DEFAULT_ENDPOINT = "https://api-services.appodeal.com/api/v2/stats_api?/"
    TASK_ENDPOINT = "https://api-services.appodeal.com/api/v2/check_status?/"
    OUTPUT_ENDPOINT = "https://api-services.appodeal.com/api/v2/output_result?/"

    DETALISATION = [
        "date",
        "country",
        "banner_type",
        "segment",
        "placement",
        "network",
        "app",
    ]

    def __init__(self, api_token, user_id):
        self.api_key = api_token
        self.user_id = user_id

    def __build_args(self, date_from, date_to, kwargs):
        args = {
            "api_key": self.api_key,
            "user_id": self.user_id,
            "date_from": date_from,
            "date_to": date_to,
        }

        if "country[]" in kwargs:
            args["country[]"] = kwargs.get("country[]")

        if "network[]" in kwargs:
            args["network[]"] = kwargs.get("network[]")

        if "app[]" in kwargs:
            args["app[]"] = kwargs.get("app[]")

        if "detalisation[]" in kwargs:
            args["detalisation[]"] = kwargs.get("detalisation[]")

        return args

    def __build_task_args(self, task_id):
        args = {"api_key": self.api_key, "user_id": self.user_id, "task_id": task_id}

        return args

    def __to_df(self, resp):
        import pandas as df

        if resp.status_code != requests.codes.ok:
            raise Exception(resp.text)

        return df.read_csv(StringIO(resp.text))

    def report(
        self,
        date_from,
        date_to,
        as_df=True,
        country=None,
        network=None,
        app=None,
        detalisation=None,
        report_waiting_time=3600,
        **kwargs
    ):
        f = furl(self.DEFAULT_ENDPOINT)

        if detalisation is None:
            kwargs["detalisation[]"] = self.DETALISATION
        else:
            kwargs["detalisation[]"] = detalisation

        if country is not None:
            kwargs["country[]"] = country
        else:
            pass

        if network is not None:
            kwargs["network[]"] = network
        else:
            pass

        if app is not None:
            kwargs["app[]"] = app
        else:
            pass

        f.args = self.__build_args(date_from, date_to, kwargs)
        request_get_task = requests.get(f.url)
        task_id = str(json.loads(request_get_task.text)["task_id"])
        print('TaskId {} obtained!'.format(task_id))
        f_task = furl(self.TASK_ENDPOINT)
        f_task.args = self.__build_task_args(task_id)
        print('Waiting for report... 5 second checks started!')
        starttime = datetime.now()
        diff = []
        diff = diff + [int((datetime.now() - starttime).seconds)] 
        
        with tqdm(total=report_waiting_time) as pbar:
            while diff[-1] < report_waiting_time:

                if json.loads(requests.get(f_task.url).text)["task_status"] == "0":

                    if diff[-1]>120:
                        sleep(10)
                        diff = diff + [int((datetime.now() - starttime).seconds)]
                        diff_sub = diff[-1]-diff[-2]
                        pbar.update(diff_sub) 

                    else:
                        sleep(5)
                        diff = diff + [int((datetime.now() - starttime).seconds)]
                        diff_sub = diff[-1]-diff[-2]
                        pbar.update(diff_sub) 

                elif json.loads(requests.get(f_task.url).text)["task_status"] == "1":
                    print("Report is ready!")
                    break

                elif diff.seconds>report_waiting_time:
                    print('Waiting time expired. Increase period!')

        f_report = furl(self.OUTPUT_ENDPOINT)
        f_report.args = self.__build_task_args(task_id)
        request_get_data = requests.get(f_report.url)
        report_data = json.loads(request_get_data.text)
        
        print('ReportData collected!')

        if 'data' not in report_data:
            report_data = requests.get(report_data['url']).json()
        else:
            report_data = report_data["data"]
        
        if as_df:
            return pd.json_normalize(report_data)
        else:
            return report_data
