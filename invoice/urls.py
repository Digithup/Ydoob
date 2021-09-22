from django.urls import path

from invoice import views

app_name = 'invoice'
urlpatterns = [


path('dashboard/invoices',views.invoices, name='AdminInvoices'),
#Create URL Paths
path('dashboard/invoices/create',views.createInvoice, name='AdminCreateInvoice'),
path('dashboard/invoices/create-build/<slug:slug>',views.createBuildInvoice, name='AdminCreateBuildInvoice'),
#Delete an invoice
path('dashboard/invoices/delete/<slug:slug>',views.deleteInvoice, name='DeleteInvoice'),
#PDF and EMAIL Paths
path('dashboard/invoices/view-document/<slug:slug>',views.viewDocumentInvoice, name='AdminViewDocumentInvoice'),
path('dashboard/invoices/view-pdf/<slug:slug>',views.viewPDFInvoice, name='AdminViewPdfInvoice'),
path('dashboard/invoices/email-document/<slug:slug>',views.emailDocumentInvoice, name='AdminEmailDocumentInvoice'),

    #######################DElivery Invoice######################
path('delivery/invoices',views.invoices, name='DeliveryInvoices'),
#Create URL Paths
path('delivery/invoices/create',views.createInvoice, name='DeliveryCreateInvoice'),
path('delivery/invoices/create-build/<slug:slug>',views.createBuildInvoice, name='DeliveryCreateBuildInvoice'),
#Delete an invoice
path('delivery/invoices/delete/<slug:slug>',views.deleteInvoice, name='DeliveryDeleteInvoice'),
#PDF and EMAIL Paths
path('delivery/invoices/view-pdf/<slug:slug>',views.viewPDFInvoice, name='DeliveryViewPdfInvoice'),
path('delivery/invoices/view-document/<slug:slug>',views.viewDocumentInvoice, name='DeliveryViewDocumentInvoice'),
path('delivery/invoices/email-document/<slug:slug>',views.emailDocumentInvoice, name='DeliveryEmailDocumentInvoice'),

#Company Settings Page
#path('company/settings',views.companySettings, name='company-settings'),
]


