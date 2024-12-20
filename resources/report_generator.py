import datetime
import pandas as pd
import sys
import os


class ReportGenerator():

    def __init__(self) -> None:
        pass

    @staticmethod
    def create_dataframe(data: dict) -> pd.DataFrame:
        """
        Which dictionary keys will be the header of column and the data of
        dictionary keys will be the data of columns
        """
        report = pd.DataFrame(data)

        return report

    @staticmethod
    def generate_report_filename(report_name) -> str:
        date_today = datetime.datetime.now().strftime("%d%m%y_%H%M%S")
        report_filename = f"report_performance_{report_name}_{date_today}"
        return report_filename

    @staticmethod
    def transform_data(
            sheet: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
        dictionary = {
            "Descrição": [],
            "Valores": [],
        }
        for description, value in sheet.items():
            dictionary["Descrição"].append(description)
            dictionary["Valores"].append(value)

        return dictionary

    @staticmethod
    def create_workbook(sheets: dict,
                        report_name,
                        transform_data=False,
                        path: str = "") -> None:
        """
        sheets -> It's a dictionary that the key is the name of sheet and value is the data
        report_name -> It's the name of report like VSMBB or ATLAS
        transform_data -> If True it will to change title of columns to lines
        path -> It's the file name or path to save adding file name

        """
        report_filename = ReportGenerator.generate_report_filename(report_name)

        # full_path = sys.path + report_filename + ".xlsx"
        # full_path = report_filename + ".xlsx"
        user_profile = os.getenv("USERPROFILE")
        onedrive = os.getenv("ONEDRIVE")
        full_path = os.path.join(onedrive, "Documentos", "3. RELATÓRIOS",
                                 f"{report_filename}.xlsx")

        directory = os.path.dirname(full_path)
        os.makedirs(directory, exist_ok=True)

        with pd.ExcelWriter(full_path) as writer:

            for sheet, data in sheets.items():

                if transform_data:
                    data = ReportGenerator.transform_data(data)

                data = ReportGenerator.create_dataframe(data)
                data.to_excel(excel_writer=writer,
                              sheet_name=sheet,
                              index=False)
