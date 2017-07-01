from openpyxl import workbook
from openpyxl import load_workbook
from openpyxl import worksheet

def readFromXLSX(path):
    wb = load_workbook(path)
    ws = wb.active

    ws_rows = tuple(ws.rows)
    rows_len = len(ws_rows)

    return rows_len-1, ws_rows[1:rows_len]

def fileSystemResponse(Resources, Folders):
    R1 = '<li class="myfile"><input type="text" class="changename" name="1" value="'
    R2 = '"/><input class="checkbox" name="'
    R3 = '" type="checkbox" value="" /></li>'
    R_str = []
    for res in Resources:
        R_str.append(R1 + res.name + R2 + str(res.id) + R3 + '\n')

    F1 = '<li class="myfolder"><input type="text" class="changename" name="1" value="'
    F2 = '"/><input class="checkbox" name="'
    F3 = '" type="checkbox" value="" /></li>'
    F_str = []
    for f in Folders:
        F_str.append(F1 + f.name + F2 + str(f.id) + F3 + '\n')

    ret_str = ''
    for res in R_str:
        ret_str = ret_str + res
    for f in F_str:
        ret_str = ret_str + f

    return ret_str

if __name__ == '__main__':
    r_len, r = readFromXLSX(path='test.xlsx')

    print(r_len)

    print(r[0], r[1])

    print(r[0][0].value, r[0][1].value, r[0][2].value)
    print(r[1][0].value, r[1][1].value, r[1][2].value)