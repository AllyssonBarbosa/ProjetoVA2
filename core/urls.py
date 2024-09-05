from seorganiza.urls import path

from .views import index, cadastrar_produto, listar_produto, buscar_produto, modificar_produto, realizar_venda, deletar_produto
from .views import estatisticas_vendas, excluir_venda
from .views import estatisticas_anuais, grafico_vendas_mes_a_mes, produtos_estoque, calcular_valor_total_estoque
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('', index, name='index'),
    path('cadastrar_produto', cadastrar_produto, name='cadastrar_produto'),
    path('listar_produto', listar_produto, name='listar_produto'),
    path('buscar_produto', buscar_produto, name='buscar_produto'),
    path('modificar_produto/<int:produto_id>/', modificar_produto, name='modificar_produto'),
    path('realizar_venda/', realizar_venda, name='realizar_venda'),
    path('deletar_produto/<int:produto_id>/', deletar_produto, name='deletar_produto'),
    path('produtos_estoque', produtos_estoque, name='produtos_estoque'),
    path('estatisticas_vendas', estatisticas_vendas, name='estatisticas_vendas'),
    path('excluir_venda/<int:venda_id>/', excluir_venda, name='excluir_venda'),
    path('index', index, name='index'),
    path('estatisticas_anuais', estatisticas_anuais, name='estatisticas_anuais'),
    path('grafico_vendas_mes_a_mes/<int:ano>/', grafico_vendas_mes_a_mes, name='grafico_vendas_mes_a_mes'),
    path('calcular_valor_total_estoque', calcular_valor_total_estoque, name='calcular_valor_total_estoque'),
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)