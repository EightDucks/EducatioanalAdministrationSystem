from openpyxl import workbook
from openpyxl import load_workbook
from openpyxl import worksheet

def readFromXLSX(path):
    wb = load_workbook(path)
    ws = wb.active

    ws_rows = tuple(ws.rows)
    rows_len = len(ws_rows)

    return rows_len-1, ws_rows[1:rows_len]

if __name__ == '__main__':
    r_len, r = readFromXLSX(path='test.xlsx')

    print(r_len)

    print(r[0], r[1])

    print(r[0][0].value, r[0][1].value, r[0][2].value)
    print(r[1][0].value, r[1][1].value, r[1][2].value)