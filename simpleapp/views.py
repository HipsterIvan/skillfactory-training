from datetime import datetime
from typing import Any
# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product
from .filters import ProductFilter
from .forms import ProductForm


class ProductsList(ListView):
   model = Product
   ordering = 'name'
   template_name = 'products.html'
   context_object_name = 'products'
   paginate_by = 2

   # Переопределяем функцию получения списка товаров
   def get_queryset(self):
       # Получаем обычный запрос
       queryset = super().get_queryset()
       # Используем наш класс фильтрации.
       # self.request.GET содержит объект QueryDict, который мы рассматривали
       # в этом юните ранее.
       # Сохраняем нашу фильтрацию в объекте класса,
       # чтобы потом добавить в контекст и использовать в шаблоне.
       self.filterset = ProductFilter(self.request.GET, queryset)
       # Возвращаем из функции отфильтрованный список товаров
       return self.filterset.qs

   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       # Добавляем в контекст объект фильтрации.
       context['filterset'] = self.filterset
       return context


class ProductDetail(DetailView):
   model = Product
   template_name = 'product.html'
   context_object_name = 'product'
   
# Добавляем новое представление для создания товаров.
class ProductCreate(CreateView):
    # Указываем нашу разработанную форму
    form_class = ProductForm
    # модель товаров
    model = Product
    # и новый шаблон, в котором используется форма.
    template_name = 'product_edit.html'
    
# Добавляем представление для изменения товара.
class  ProductUpdate(UpdateView):
    form_class = ProductForm
    model=Product
    template_name = 'product_edit.html'
    
class ProductDelete(DeleteView):
    model=Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy('product_list')