from tkinter import *
from tkinter import messagebox
import time
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, \
    Table, TableStyle

data = []
selected_item = []
lines = []
root = Tk()
root.geometry("600x600+100+100")
root.resizable(FALSE,FALSE)

class DataToPdf():
    """
    Export a list of dictionaries to a table in a PDF file.
    """

    def __init__(self, fields, data, sort_by=None, title=None):
        """
        Arguments:
            fields - A tuple of tuples ((fieldname/key, display_name))
                specifying the fieldname/key and corresponding display
                name for the table header.
            data - The data to insert to the table formatted as a list of
                dictionaries.
            sort_by - A tuple (sort_key, sort_order) specifying which field
                to sort by and the sort order ('ASC', 'DESC').
            title - The title to display at the beginning of the document.
        """
        self.fields = fields
        self.data = data
        self.title = title
#        self.sort_by = sort_by

    def export(self, filename, data_align='LEFT', table_halign='LEFT'):
        """
        Export the data to a PDF file.

        Arguments:
            filename - The filename for the generated PDF file.
            data_align - The alignment of the data inside the table (eg.
                'LEFT', 'CENTER', 'RIGHT')
            table_halign - Horizontal alignment of the table on the page
                (eg. 'LEFT', 'CENTER', 'RIGHT')
        """
        doc = SimpleDocTemplate(filename, pagesize=letter)

        styles = getSampleStyleSheet()
        styleH = styles['Heading1']

        story = []

        if self.title:
            story.append(Paragraph(self.title, styleH))
            story.append(Spacer(1, 0.25 * inch))

        converted_data = self.__convert_data()
        table = Table(converted_data, hAlign=table_halign)
        table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('ALIGN',(0, 0),(0,-1), data_align),
            ('INNERGRID', (0, 0), (-1, -1), 0.50, colors.black),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ]))

        story.append(table)
        try:
            doc.build(story)
            answer = messagebox.askquestion("Success", "PDF file is successfully generated!!!")
            if answer == 'yes':
                second.quit()
        except Exception as e:
            raise

    def __convert_data(self):
        """
        Convert the list of dictionaries to a list of list to create
        the PDF table.
        """
        # Create 2 separate lists in the same order: one for the
        # list of keys and the other for the names to display in the
        # table header.
        keys, names = zip(*[[k, n] for k, n in self.fields])
        new_data = [names]

        for d in self.data:
            new_data.append([d[k] for k in keys])

        return new_data

def PDFMethod():
    fields = (('filename', 'Product Name'),('filepath', 'Price'))
    doc = DataToPdf(fields, data, title='Product purchase summary')
    doc.export('PurchaseBill.pdf')

def itemList():
    global lines

    lineno = 0
    ro = 3
    col = 0
    nnum = 1
    pnum = 1

    F = open("items.txt","r")
    lines = F.read().splitlines()

    for x in lines:
#        print(x)
#        print(lineno)
        iname, price = lines[lineno].split('-')
        name = 'name{}'.format(nnum)
        pri = 'price{}'.format(pnum)
        name = Label(dishList, text='{} {} {}'.format(lineno+1, iname, price), anchor=W, font=("Courier", 12))
        name.pack(fill=X)

        nnum += 1
        pnum += 1
        ro += 1
        lineno = lineno + 1

def selectingProduct():
    if len(query.get()) > 0:
        global selected_item
        selected_item = list(str(query.get()))
        secondPage(selected_item)
    else:
        print("Something is not right!!!")

def secondPage(lists):
    second = Toplevel()
    second.geometry("500x500+120+120")
    heading = Label(second, text="Restaurant Billing System", font=("Courier", 20))
    heading.pack()
    h1 = Label(second, text="Purchase Summary", font=("Courier", 18))
    h1.pack()

    global data
    total = 0.0
    lineno = 0
    ro = 3
    col = 0
    nnum = 1
    pnum = 1

    for x in lists:
#        print(lines[int(x)-1])
        iname, price = lines[int(x)-1].split('-')
        name = 'name{}'.format(nnum)
        pri = 'price{}'.format(pnum)
        name = Label(second, text='{} {}'.format(lineno+1, iname), anchor=W, font=("Courier", 12))
        #pr = Label(second, text='{}'.format(price), anchor=E, font=("Courier", 12))
        pr = Label(second, text='{}'.format(price), anchor=E, font=("Courier", 12))
        name.pack(fill=X)
        pr.pack(fill=X)

        data.append({'filename': iname,'filepath': price})

        nnum += 1
        pnum += 1
        ro += 1
        lineno = lineno + 1
        tagval = price.replace('$','')
        total = total + float(tagval)

    tot = Label(second, text='Your total purchase is of : ', anchor=W, font=("Courier", 12))
    tota = Label(second, text='${}'.format(total), anchor=E, font=("Courier", 12))
    tot.pack(fill=X)
    tota.pack(fill=X)

    data.append({'filename': "Your total purchase is of : ",'filepath': "${}".format(total)})

    btnPrint = Button(second, text="Generate Bill", bg="light green", command=PDFMethod)
    btnPrint.pack(fill=X, pady=5, padx=15)

heading = Label(root, text="Restaurant Billing System", font=("Courier", 25))
heading.pack()

mainframe = Frame(root)
mainframe.pack()

dishList = Frame(mainframe, width=300)
dishList.pack(side=LEFT)

orderList = Frame(mainframe, width=300)
orderList.pack(side=RIGHT)

heading = Label(dishList, text="Dishes for sell", font=("Bold Courier", 15))
heading.pack(pady=25)

itemList()

heading = Label(orderList, text="Place your order here", font=("Bold Courier", 15))
heading.pack(pady=25)

note = Label(orderList, anchor=E, text="Note: Enter product number for number of time \n you want to purchase it.", font=("Courier", 8))
note.pack(fill=X)

productNumber = StringVar()

query = Entry(orderList, textvariable=productNumber, bd=3, font=("Courier", 19))
query.pack(fill=X, pady=5)

placebtn = Button(orderList, text="Place order", bg="light green", command=selectingProduct)
placebtn.pack(fill=X, pady=5)

root.mainloop()
