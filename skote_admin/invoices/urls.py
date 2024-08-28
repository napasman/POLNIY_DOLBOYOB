from django.urls import path
from . import views

urlpatterns = [
    path('invoicelist',views.InvoiceListView.as_view(),name='invoices-invoicelist'),
    path('invoicedetail',views.InvoiceDetailView.as_view(),name='invoices-invoicedetail'),
]