import sqlalchemy as db
from docx import Document
from docx.shared import Cm, Pt
import datetime

engine = db.create_engine('mysql://root:''@localhost/Plan_IM')
connection = engine.connect()
metadata = db.MetaData()

user = db.Table('user', metadata, autoload=True, autoload_with=engine)
query = db.select(user)
users = connection.execute(query).fetchall()

data = db.Table('data', metadata, autoload=True, autoload_with=engine)
query = db.select(data)
datas = connection.execute(query).fetchall()


word_document = Document()
table = word_document.add_table(0,0)
table.style = 'TableGrid'

table.add_column(Cm(20))
table.add_column(Cm(20))
table.add_column(Cm(20))
table.add_column(Cm(20))
table.add_column(Cm(20))
table.add_column(Cm(20))

table.add_row()
row = table.rows[0]
row.cells[0].text = "Imię i nazwisko"
row.cells[1].text = "Poniedziałek"
row.cells[2].text = "Wtorek"
row.cells[3].text = "Środa"
row.cells[4].text = "Czwartek"
row.cells[5].text = "Piątek"

i=1
for user in users:
    table.add_row()
    row = table.rows[i]
    row.cells[0].text = user[5] +' '+ user[1]
    for data in datas:
        if data[-1]==user[1]:
            start = str(data[3]).split(':')
            start = start[0]+':'+start[1]
            end = (datetime.datetime.combine(datetime.date(1,1,1),data[3]) + datetime.timedelta(minutes=int(data[4]))).time()
            end = str(end).split(':')
            end = end[0] +':'+end[1]

            text = data[5] +' '+start +' - ' + end +' '+  str(data[12]) + ' (' +data[11]+')\n'
            if data[1] == "Pon":
                row.cells[1].text += text
            if data[1] == "Wt":
                row.cells[2].text += text
            if data[1] == "Sr":
                row.cells[3].text += text
            if data[1] == "Czw":
                row.cells[4].text += text
            if data[1] == "Pt":
                row.cells[5].text += text
    i=i+1

word_document.save('Plan.docx')

