import openpyxl
from openpyxl.worksheet.worksheet import Worksheet
# 第一步：打开 excel 文件
wb = openpyxl.load_workbook('cases.xlsx')
print(wb)

# 获取表格
#sheet= wb['Sheet1']
#增加sheet.后面内容提示
sheet: Worksheet = wb['Sheet1']
print(sheet)

# 获取表格中的数据
# print(sheet.cell(2,3).value)

# 获取所有的行数据
rows = list(sheet.values)
for row in rows:
    print(row)