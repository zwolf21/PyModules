from collections import OrderedDict
from io import BytesIO
import os, re
import xlrd, xlsxwriter

def to_num(val):
	try:
		ret = float(val)
	except:
		return val
	else:
		return ret


class ExcelWork:

	def __init__(self, excel_path=None, excel_contents=None, records=None, sheet_index=0, toNumber=True):
		if records:
			self.records = records
			self.header = list(records[0].keys())
		else:
			wb = xlrd.open_workbook(excel_path or excel_contents) if excel_path else xlrd.open_workbook(file_contents=excel_contents)
			ws = wb.sheet_by_index(sheet_index)
			self.header = ws.row_values(0)
			if toNumber:
				self.records = [OrderedDict(zip(self.header, map(to_num , ws.row_values(row)))) for row in range(1, ws.nrows)]
			else:
				self.records = [OrderedDict(zip(self.header, ws.row_values(row))) for row in range(1, ws.nrows)]

	def __getitem__(self, index):
		return self.records[index]

	def __iter__(self):
		return iter(self.records)

	@property
	def header_row(self):
		return OrderedDict(zip(self.header, self.header))

	def get_output(self, body=None, title=None, start_row=0, start_col=0, 
			header=True, colwidths=[], selects=[], excludes=[], formats=None, output_to_file=""):
		if selects:
			queryset = [OrderedDict((k, row[k]) for k in selects if k in row) for row in body or self.records]
		else:
			queryset = body or self.records
		output = BytesIO()
		wb = xlsxwriter.Workbook(output, {'inmemory': True, 'remove_timezone': True})
		ws = wb.add_worksheet()
		format_cache = {}
		
		if header:
			queryset = [OrderedDict(zip(queryset[0].keys(), queryset[0].keys()))] + queryset

		for width in colwidths:
			ws.set_column(*width)
		
		if title:
			title_format = wb.add_format({'align': 'center', 'bold': True, 'font_size':20})
			ws.merge_range(start_row, 0, start_row, len(records[0]), title, title_format)
			start_row +=1

		for r, row in enumerate(queryset):
			nShift =0
			for c, (key, value) in enumerate(row.items()):
				if key in excludes:
					nShift+=1
					continue
				fmt = None
				col_format = formats.get(key) if formats else None
				if col_format:
					try:
						fmt_kv = col_format(row) if callable(col_format) else col_format
					except Exception as e:
						fmt = None
					else:	
						if fmt_kv:
							k, v = fmt_kv
							if not tuple(fmt_kv) in format_cache:
								format_cache[fmt_kv] = wb.add_format({k: v})
							fmt = format_cache[fmt_kv]
							if k == 'num_format':
								value = to_num(value)
				ws.write(r+start_row, c+start_col-nShift, value, fmt)
		wb.close()

		if output_to_file:
			with open(output_to_file, 'wb') as fp:
				fp.write(output.getvalue())
		else:
			return output.getvalue() 


	def ext_pattern(self, reg_pattern):
		p = re.compile(reg_pattern)
		ret = []
		for rec in self.records:
			for key, val in rec.items():
				ret += p.findall(val)
		return ret





