import os
from uuid import uuid4
import pdfkit
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template.loader import get_template
from django.utils.crypto import get_random_string

from DNigne import settings
from invoice.forms import InvoiceForm
from invoice.functions import emailInvoiceClient
from invoice.models import Invoice, Settings
from sales.forms.forms import OrderProductForm
from sales.models.orders import OrderProduct


@login_required
def invoices(request):
    context = {}
    invoices = Invoice.objects.all()
    context['invoices'] = invoices

    return render(request, 'invoice/invoices.html', context)


@login_required
def createInvoice(request):
    #create a blank invoice ....
    number = 'INV-'+str(uuid4()).split('-')[1]
    newInvoice = Invoice.objects.create(number=number)
    newInvoice.save()

    inv = Invoice.objects.get(number=number)
    return redirect('invoice:AdminCreateBuildInvoice', slug=inv.slug)


@login_required
def createBuildInvoice(request, slug):
    #fetch that invoice
    try:
        invoice = Invoice.objects.get(slug=slug)
        pass
    except:
        messages.error(request, 'Something went wrong')
        return redirect('invoice:AdminInvoices')

    #fetch all the products - related to this invoice
    order = OrderProduct.objects.filter(invoice=invoice)


    context = {}
    context['invoice'] = invoice
    context['order'] = order

    if request.method == 'GET':
        prod_form  = OrderProductForm()
        inv_form = InvoiceForm(instance=invoice)
       # client_form = ClientSelectForm(initial_client=invoice.client)
        context['prod_form'] = prod_form
        context['inv_form'] = inv_form
        #context['client_form'] = client_form
        return render(request, 'invoice/create-invoice.html', context)

    if request.method == 'POST':
        prod_form  = OrderProductForm(request.POST)
        inv_form = InvoiceForm(request.POST, instance=invoice)
        #client_form = ClientSelectForm(request.POST, initial_client=invoice.client, instance=invoice)

        if prod_form.is_valid():
            obj = prod_form.save(commit=False)
            obj.invoice = invoice
            obj.save()

            messages.success(request, "Invoice product added succesfully")
            return redirect('invoice:AdminCreateBuildInvoice', slug=slug)
        elif inv_form.is_valid and 'paymentTerms' in request.POST:
            inv_form.save()

            messages.success(request, "Invoice updated succesfully")
            return redirect('invoice:AdminCreateBuildInvoice', slug=slug)
        elif client_form.is_valid() and 'client' in request.POST:

            client_form.save()
            messages.success(request, "Client added to invoice succesfully")
            return redirect('invoice:AdminCreateBuildInvoice', slug=slug)
        else:
            context['prod_form'] = prod_form
            context['inv_form'] = inv_form
            context['client_form'] = client_form
            messages.error(request,"Problem processing your request")
            return render(request, 'invoice/create-invoice.html', context)


    return render(request, 'invoice/create-invoice.html', context)

def deleteInvoice(request, slug):
    try:
        Invoice.objects.get(slug=slug).delete()
    except:
        messages.error(request, 'Something went wrong')
        return redirect('invoice:AdminInvoices')

    return redirect('invoices')

def viewPDFInvoice(request, slug):
    #fetch that invoice
    try:
        invoice = Invoice.objects.get(slug=slug)
        pass
    except:
        messages.error(request, 'Something went wrong')
        return redirect('invoices')

    #fetch all the products - related to this invoice
    order_product = OrderProduct.objects.filter(invoice=invoice)

    #Get Client Settings
    p_settings = Settings.objects.get(order__invoice=invoice)

    #Calculate the Invoice Total
    invoiceCurrency = ''
    invoiceTotal = 0.0
    if len(order_product) > 0:
        for x in order_product:
            y = float(x.quantity) * float(x.price)
            invoiceTotal += y
            invoiceCurrency = x.currency



    context = {}
    context['invoice'] = invoice
    context['order_product'] = order_product
    context['p_settings'] = p_settings
    context['invoiceTotal'] = "{:.2f}".format(invoiceTotal)
    context['invoiceCurrency'] = invoiceCurrency

    return render(request, 'invoice/invoice-template.html', context)



def viewDocumentInvoice(request, slug):
    #fetch that invoice
    try:
        invoice = Invoice.objects.get(slug=slug)
        pass
    except:
        messages.error(request, 'Something went wrong')
        return redirect('invoices')

    #fetch all the products - related to this invoice
    products = OrderProduct.objects.filter(invoice=invoice)

    #Get Client Settings
    #p_settings = Settings.objects.get(order__address__first_name=invoice.client.)

    #Calculate the Invoice Total
    invoiceTotal = 0.0
    if len(products) > 0:
        for x in products:
            y = float(x.quantity) * float(x.price)
            invoiceTotal += y
    context = {}
    context['invoice'] = invoice
    context['products'] = products
    #context['p_settings'] = p_settings
    context['invoiceTotal'] = "{:.2f}".format(invoiceTotal)

    #The name of your PDF file
    filename = '{}.pdf'.format(invoice.uniqueId)

    #HTML FIle to be converted to PDF - inside your Django directory
    template = get_template('invoice/pdf-template.html')


    #Render the HTML
    html = template.render(context)

    #Options - Very Important [Don't forget this]
    options = {
          'encoding': 'UTF-8',
          'javascript-delay':'10', #Optional
          'enable-local-file-access': None, #To be able to access CSS
          'page-size': 'A4',
          'custom-header' : [
              ('Accept-Encoding', 'gzip')
          ],
      }
      #Javascript delay is optional

    #Remember that location to wkhtmltopdf
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    #IF you have CSS to add to template
    css1 = os.path.join(settings.CSS_LOCATION, 'assets', 'css', 'bootstrap.min.css')
    css2 = os.path.join(settings.CSS_LOCATION, 'assets', 'css', 'dashboard.css')

    #Create the file
    file_content = pdfkit.from_string(html, False, configuration=config, options=options)

    #Create the HTTP Response
    response = HttpResponse(file_content, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename = {}'.format(filename)

    #Return
    return response


def emailDocumentInvoice(request, slug):
    #fetch that invoice
    try:
        invoice = Invoice.objects.get(slug=slug)
        pass
    except:
        messages.error(request, 'Something went wrong')
        return redirect('invoices')

    #fetch all the products - related to this invoice
    products = OrderProduct.objects.filter(invoice=invoice)

    #Get Client Settings
    p_settings = Settings.objects.get(clientName='Skolo Online Learning')

    #Calculate the Invoice Total
    invoiceTotal = 0.0
    if len(products) > 0:
        for x in products:
            y = float(x.quantity) * float(x.price)
            invoiceTotal += y



    context = {}
    context['invoice'] = invoice
    context['products'] = products
    context['p_settings'] = p_settings
    context['invoiceTotal'] = "{:.2f}".format(invoiceTotal)

    #The name of your PDF file
    filename = '{}.pdf'.format(invoice.uniqueId)

    #HTML FIle to be converted to PDF - inside your Django directory
    template = get_template('invoice/pdf-template.html')


    #Render the HTML
    html = template.render(context)

    #Options - Very Important [Don't forget this]
    options = {
          'encoding': 'UTF-8',
          'javascript-delay':'1000', #Optional
          'enable-local-file-access': None, #To be able to access CSS
          'page-size': 'A4',
          'custom-header' : [
              ('Accept-Encoding', 'gzip')
          ],
      }
      #Javascript delay is optional

    #Remember that location to wkhtmltopdf
    config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')

    #Saving the File
    filepath = os.path.join(settings.MEDIA_ROOT, 'client_invoices')
    os.makedirs(filepath, exist_ok=True)
    pdf_save_path = filepath+filename
    #Save the PDF
    pdfkit.from_string(html, pdf_save_path, configuration=config, options=options)


    #send the emails to client
    to_email = invoice.client.emailAddress
    from_client = p_settings.clientName
    emailInvoiceClient(to_email, from_client, pdf_save_path)

    invoice.status = 'EMAIL_SENT'
    invoice.save()

    #Email was send, redirect back to view - invoice
    messages.success(request, "Email sent to the client succesfully")
    return redirect('create-build-invoice', slug=slug)
