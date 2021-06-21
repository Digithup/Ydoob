from django.test import TestCase

# Create your tests here.
from catalog.models.models import Category

europe = Category.objects.translate('title').all()

print(europe)
"""""

class ProductsView(ListView):
    model = SellerProducts
    template_name = 'admin/pages/Products-admin.html'
    paginate_by = 10


class ProductsDetailView(DetailView):
    model = SellerProducts
    template_name = 'admin/pages/banner-detail.html'


class ProductsCreateView(CreateView):
    model = SellerProducts
    template_name = 'admin/pages/add-catalog.html'
    fields = '__all__'


def Products_admin(request):
    category = Category.objects.all()
    Products = SellerProducts.objects.all()
    context = {'Products': Products,

               }

    return render(request, 'admin/pages/Products-admin.html', context)


def Products_admin(request, id, slug):
    query = request.GET.get('q')
    category = Category.objects.all()
    catalog = SellerProducts.objects.get(pk=id)

    context = {'catalog': catalog, 'category': category,

               }
    # return HttpResponse('f')
    return render(request, 'admin/pages/banner-detail.html', context)


def create(request):
    if request.method == 'POST':
        form = ProductsAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/admin/catalog')
    form = ProductsAddForm()
    return render(request, 'admin/pages/add-catalog.html', {'form': form})


def edit(request, pk, template_name='admin/pages/edit-catalog'):
    catalog = get_object_or_404(SellerProducts, pk=pk)
    form = ProductsAddForm(request.POST or None, instance=title)
    if form.is_valid():
        form.save()
        return redirect('/admin/Products')
    return render(request, template_name, {'form': form})


def delete(request, pk, template_name='crudapp/confirm_delete.html'):
    catalog = get_object_or_404(SellerProducts, pk=pk)
    if request.method == 'POST':
        catalog.delete()
        return redirect('/admin')
    return render(request, template_name, {'object': catalog})


def Products_edit(request, id, slug):
    # return HttpResponse('1')
    Products = SellerProducts.objects.all()
    catalog = SellerProducts.objects.filter(pk=id)

    context = {
        'catalog': catalog,
    }
    if request.method == 'GET':
        return render(request, 'admin/pages/edit-catalog.html', context)
    if request.method == 'POST':
        title = request.POST.get('title')

        if not title:
            messages.error(request, 'Title is required')
            return render(request, 'admin/pages/edit-catalog.html', context)
        category = request.POST['category']
        keywords = request.POST['keywords']
        description = request.POST['description']
        image = request.POST.get['image']
        price = request.POST['price']
        n_price = request.POST['n_price']
        discount = request.POST['discount']
        amount = request.POST['amount']
        minamount = request.POST['minamount']
        variant = request.POST['variant']
        detail = request.POST['detail']
        status = request.POST['status']
        slug = request.POST['slug']

        if not category:
            messages.error(request, 'category is required')
            return render(request, 'admin/pages/edit-catalog.html', context)

        catalog.title = title
        catalog.category = category
        catalog.keywords = keywords
        catalog.description = description
        catalog.image = image
        catalog.price = price
        catalog.n_price = n_price
        catalog.discount = discount
        catalog.amount = amount
        catalog.minamount = minamount
        catalog.variant = variant
        catalog.detail = detail
        catalog.status = status
        catalog.slug = slug
        catalog.save()
        messages.success(request, 'Category updated  successfully')

        return redirect('/admin/catalog/')
        
        
        
        
        
        
        
        
        
        from urllib import request

from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, Select, FileInput, Textarea

from catalog.models import Category, SellerProducts, ImageAlbum, Manufacturer


class CategoryAddForm(forms.ModelForm):
    title = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Category
        fields = '__all__'



class ProductsAddForm(forms.ModelForm):
    class Meta:
        model = SellerProducts
        fields = '__all__'

class ProductsAddFormm(forms.ModelForm):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )

    VARIANTS = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color'),

    )
    category = forms.ModelChoiceField(queryset=Category.objects.filter(title='title'),empty_label="Chose One")  # many to one relation with Category
    title = forms.CharField()
    keywords = forms.CharField()
    description = forms.Textarea()
    m_image = forms.ImageField()
    price = forms.DecimalField()
    n_price = forms.DecimalField()
    discount = forms.DecimalField()
    amount = forms.IntegerField()
    min_amount = forms.IntegerField()
    variant = forms.ChoiceField(choices=VARIANTS)
    slug = forms.SlugField()
    status = forms.ChoiceField(choices=STATUS)
    class Meta:
        model = SellerProducts
        fields = ('category','title','keywords','description','m_image','price','n_price','discount','amount','min_amount'
                  ,'variant','slug','status')


class ManufacturerAddForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = '__all__'




def addProductsView(request):
    if request.method == "POST":
        contributeForm = ProductsFullForm(request.POST)

        if contributeForm.is_valid():
            post = contributeForm.save(commit=False)
            try:
                post.save()
                return redirect('/admin/catalog')
            except:
                pass
        else:
            # this should be include if form validate failed
            return render(request, 'admin/pages/add-catalog.html', {'contributeForm': contributeForm})
        elif request.method == "GET":
        category = Category.objects.all()
        contributeForm = ProductsFullForm()
        context = {'contributeForm': contributeForm
            , 'category': category}
        # return render(request, 'index.html', context) <-- why do you have this here?
        return render(request, 'admin/pages/add-catalog.html', context)


"""
