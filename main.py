import argparse
import json
import datetime
from tabulate import tabulate

#Список, в котором содержатся обрабатываемые типы отчёта, при добавлении нового типа, его необходимо указать в списке
list_of_reports = ["average"]
def valid_report(report_type:str,lst_of_valid_reports:list):
    if report_type not in lst_of_valid_reports:
        raise ValueError("Данный тип отчёта не входит в список обрабатываемых:"+str(lst_of_valid_reports))

def valid_date (date: str):
    if date != "none":
        try:
            datetime.date.fromisoformat(date)
        except ValueError:
            raise ValueError("Неправильный формат даты, должен быть YYYY-MM-DD")

def read_files (files: list):
    temp_json_objects = []
    for i in range(0, len(files)):
        with open(files[i], 'r') as f:
            lines = f.readlines()
            temp_json_objects = temp_json_objects + [json.loads(line) for line in lines]
    return temp_json_objects

def Handling (objects:list,report_type:str, date:str):
    report = []
    match report_type:
        case "average":
            for i in range(0, len(objects)):
                exist = False
                if date == "none" or date in objects[i]["@timestamp"]:
                    for handl in report:
                        if  objects[i]["url"] == handl["handler"]:
                            handl["total"] = handl["total"] + 1
                            handl["avg_response_time"] = handl["avg_response_time"] + objects[i]["response_time"]
                            exist = True
                    if not exist:
                        report.append({"handler": objects[i]["url"], "total": 1,
                                       "avg_response_time": objects[i]["response_time"]})
            for handl in report:
                handl["avg_response_time"] = handl["avg_response_time"] / handl["total"]
    return report

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Обработчик логов")
    parser.add_argument("-f", "--file", action="extend", nargs="+", help="Файлы логов", required=True)
    parser.add_argument("-r", "--report", help="Тип отчёта", required=True)
    parser.add_argument("-d", "--date", nargs='?', default='none', help="Дата записей")
    args = parser.parse_args()
    valid_report(args.report, list_of_reports)
    valid_date(args.date)
    json_objects = read_files(args.file)
    report = Handling(json_objects,args.report,args.date)
    print(tabulate(report, headers='keys', showindex="always"))