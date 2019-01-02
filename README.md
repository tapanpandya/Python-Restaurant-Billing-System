# Python-Restaurant-Billing-System
I have created simple gui application using Tkinter and ReportLab to generate pdfs of bill

I have used tkinter which is in-built library of python in making this GUI application.

Functionality of these application is:

- Application would import product/Dishes from items.txt file to show dishes as a restaurant menu.
- So anyone can modify items.txt file to add or delete dishes.
- in the Textbox(Entry) user only have to enter dish number for as many time as user wants purchase and just have to press the place order button

i.e. 
Suppose Menu is like:
1. Bread
2. Butter
3. Cheese 

and if I want to purchase two packets of bread and one packet of cheese then,

I have to enter 113 in the Entry(Textbox) and just need to press place order.

On the next window, total will be calculated and bill will be generated in PDF format on button click.

That's all!!!

you have to install ReportLab if your system haven't have it already.
to install on linux run following command on terminal

pip3 install reportlab

