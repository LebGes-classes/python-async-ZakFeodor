import pandas as pd
from DfOperate import DfOperate
import time


def excel_processing(file_name):
    """Считывание файл Excel, обработка его и возврат результатирующей таблицы

    Args:
        file_name: имя файла для считывания
    """
    
    try:
        df = pd.read_excel(file_name)
    except Exception as e:

        print(f'Ошибка при считывании файла {file_name}: {e}')

    status_mapping = {
        'OK': 'operational',
        'op': 'operational',
        'broken': 'faulty',
        'planned_installation': 'planned_installation',
        'maintenance_scheduled': 'maintenance_scheduled',
        'operational': 'operational',
        'faulty': 'faulty'
    }

    df['status'] = df['status'].astype(str).str.lower().str.strip()
    df['status'] = df['status'].map(status_mapping).fillna(df['status'])

    data = DfOperate(df)

    table_filter_warranty = data.get_tables_by_warranty_status()
    problem_clinics = data.find_problem_clinics()
    calibration_statuses = data.get_calibration_statuses()
    pivot_table_clinics = data.create_pivot_table()
    with pd.ExcelWriter(f'{file_name}_solution.xlsx', engine='openpyxl') as writer:
        table_filter_warranty['Гарантия истекла'].to_excel(writer, sheet_name='Гарантия истекла', index=False)
        table_filter_warranty['Истечет менее чем через месяц'].to_excel(writer,
                                                                        sheet_name='Гарантия менее месяца',
                                                                        index=False)
        table_filter_warranty['Истечет менее чем через полгода'].to_excel(writer,
                                                                          sheet_name='Гарантия менее полугода',
                                                                          index=False)
        table_filter_warranty['Истечет более чем через полгода'].to_excel(writer,
                                                                          sheet_name='Гарантия более полугода',
                                                                          index=False)
        problem_clinics.to_excel(writer, sheet_name='Наиболее проблемные клиники', index=False)
        calibration_statuses.to_excel(writer, sheet_name='Статусы калибровки', index=False)
        pivot_table_clinics.to_excel(writer, sheet_name='Сводная таблица по клиникам', index=False)


def main():
    """Функция выполнения задач с синхронной записью

    Returns:
        float: Время работы синхронно выполняемого кода
    """

    start_time = time.time()
    excel_processing('medical_diagnostic_devices_1.xlsx')
    excel_processing('medical_diagnostic_devices_2.xlsx')
    excel_processing('medical_diagnostic_devices_3.xlsx')
    excel_processing('medical_diagnostic_devices_4.xlsx')
    excel_processing('medical_diagnostic_devices_5.xlsx')
    excel_processing('medical_diagnostic_devices_6.xlsx')
    excel_processing('medical_diagnostic_devices_7.xlsx')
    excel_processing('medical_diagnostic_devices_8.xlsx')
    excel_processing('medical_diagnostic_devices_9.xlsx')
    excel_processing('medical_diagnostic_devices_10.xlsx')
    return f'Время работы синхронно выполняемого кода = {time.time()-start_time}'


if __name__ == '__main__':
    print(main())
