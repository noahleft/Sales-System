#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from config import SQL_path

import cgi
form=cgi.FieldStorage()
form_id=form.getvalue('form_id')
company_id=form.getvalue('company_id')
import sqlite3

from os.path import isfile

if not isfile(SQL_path):
  print("Can't detect SQL database at path:",SQL_path)
  from database import create_db
  conn=create_db(SQL_path)
else:
  from database import link_db
  conn=link_db(SQL_path)

def convertToDict(DataList):
  DataDict={}
  for item in DataList:
    DataDict[item[0]]=item[1]
  return DataDict

cursor=conn.cursor()
cursor.execute('SELECT NAME FROM form where id='+str(form_id))
formName=cursor.fetchall()[0][0]
cursor.execute('SELECT NAME FROM company where id='+str(company_id))
companyName=cursor.fetchall()[0][0]

print("Content-type: text/html",end='\n\n')
print("""
<!DOCTYPE html>
<html>
<head>
<title>紀錄</title>
<meta charset="UTF-8">
<link href="../Site.css" rel="stylesheet">
</head>
<body>""")

#(<nav id="nav01"></nav>""")
print("""
<div id="main">
  <h1>應收帳款 """+str(companyName)+' '+str(formName)+'</h1>')



showList=['COMP_ID','PROD_ID','DELIVER_DATE','UNIT_PRICE','QUANTITY']
cursor.execute('SELECT '+','.join(showList)+' FROM record WHERE form_id='+str(form_id)+' and comp_id='+str(company_id)+' and HIDE!=1 ORDER BY DELIVER_DATE')
data=cursor.fetchall()
cursor.execute('SELECT ID,NAME FROM product')
productList=cursor.fetchall()
productDict=convertToDict(productList)


def convertDate(date):
  return str(int(date[:4])-1911)+date[4:]

print('<table>')
print('<tr>')
showChList=[('class="dateTime"','日期'), \
            ('class="productName"','品項'), \
            ('class="quantity"','數量'), \
            ('class="price"','單價'), \
            ('class="price"','小計')]
print(''.join(list(map(lambda x:'<th '+x[0]+'>'+x[1]+'</th>',showChList))))
print('</tr>')
total_price=0
for row in data:
  unit_price=float(row[3])
  quantity=float(row[4])
  price=unit_price*quantity
  total_price+=price
  rowStrings=['<tr>']
  rowStrings+=['<td class="dateTime">'+str(convertDate(row[2]))+'</td>']
  rowStrings+=['<td class="productName">'+str(productDict[row[1]])+'</td>']
  rowStrings+=['<td class="quantity">'+str(row[4])+'y</td>']
  rowStrings+=['<td class="price">'+str(row[3])+'</td>']
  rowStrings+=['<td class="price">'+str(price)+'</td>']
  rowStrings+=['</tr>']
  print(''.join(rowStrings))
print('</table>')

print('總計:',int(total_price))

############################

print("""<footer id="foot01"></footer>
</div>

<script src="../Script.js"></script>

</body>
</html>""")



