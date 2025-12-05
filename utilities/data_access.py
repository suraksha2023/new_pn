import openpyxl

def read_pn_data(filepath):
    workbook = openpyxl.load_workbook(filepath)
    sheet = workbook.active
    data = []

    for row in sheet.iter_rows(min_row=2, values_only=True):
        role, username, password, sop_title, file_path = row
        data.append({
            "role": role,
            "username": username,
            "password": password,
            "sop_title": sop_title,
            "file_path": file_path
        })
    return data


