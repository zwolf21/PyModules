__all__ = ['ExcelWork', 'RecordParser']
__version__ = '1.0.0'

'''
Useage

def getNumFormat(rec):
	code = rec['약품코드']
	fmt = drugDB[code]['amount_unit']
	return 'num_format', '0.00 "{}"'.format(fmt)


exl = ExcelWork(path)[:]
rec = RecordParser(exl, drop_row_criteria=lambda row: row['불출일자']=="")
rec.add_column([('잔량', 0), ('폐기량', 0), ('폐기단위', ''),('폐기약품명', '')])
ret = rec.select(
	# fields = ['불출일자', '병동', '환자번호', '환자명', '폐기약품명', '처방량(규격단위)', '잔량', '규격단위', '폐기량', '약품코드', '총량','집계량', '폐기단위'],
	where = lambda row: row['반납구분'] not in ('D/C', '반납', '수납취소') and row['약품코드'] in drugDB
)

ret = rec.update(
		bootstrap= [
			('병동', lambda row: str(row['병동'])),
			('잔량', lambda row: row['집계량']-row['처방량(규격단위)']), 
			('폐기량', lambda row: row['잔량'] * drugDB[row['약품코드']]['amount']),
			('폐기단위', lambda row: drugDB[row['약품코드']]['amount_unit']),
			('폐기약품명', lambda row: drugDB[row['약품코드']]['name']),
	])

ret = rec.select(where = lambda row: row['폐기량'] > 0).order_by('폐기약품명', '불출일자', '병동')
grp = rec.group_by(
	annotations = {'폐기약품명':[('앰플수', '폐기약품명', len), ('폐기량종합','폐기량',sum)]},
	selects=['불출일자', '병동','환자번호', '환자명', '폐기약품명','처방량(규격단위)', '앰플수','규격단위','폐기량종합','약품코드'], 
	dummy=['불출일자', '병동','환자번호', '환자명', '처방량(규격단위)']
)
print(grp)
exl = ExcelWork(records=ret.records+grp)

with open('text.xlsx', 'wb') as fp:
	fp.write(exl.get_output(
		selects=['불출일자', '병동', '환자번호', '환자명', '폐기약품명', '처방량(규격단위)', '앰플수','잔량', '규격단위', '폐기량','약품코드','폐기량종합',],
		excludes = ['약품코드'], 
		formats={'폐기량': getNumFormat, '폐기량종합': getNumFormat}
	))
os.startfile('text.xlsx')

'''