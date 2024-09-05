from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.db.models import F, Sum
from django.utils import timezone
from django.http import HttpResponse
from .models import Produto, Venda
from .forms import ProdutoForm
from datetime import datetime, date
from decimal import Decimal



def index(request):
    return render(request, 'index.html')


def produto(request, pk):
    prod = get_list_or_404(Produto, id=pk)
    context = {
        'produto': prod

    }
    return render(request, 'produto.html', context)



def cadastrar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_produto')
    else:
        form = ProdutoForm()
    return render(request, 'cadastrar_produto.html', {'form': form})



def listar_produto(request):
    produtos = Produto.objects.all()
    if not produtos:
        mensagem = "Nenhum produto cadastrado."
    else:
        mensagem = None
    return render(request, 'listar_produto.html', {'produtos': produtos, 'mensagem': mensagem})


def buscar_produto(request):
    query_nome = request.GET.get('q_nome')
    query_id = request.GET.get('q_id')
    produtos_por_nome = []
    produto_por_id = None

    if query_id:
        try:
            produto_por_id = Produto.objects.get(id=query_id)
        except (Produto.DoesNotExist, ValueError):
            pass
    elif query_nome:
        produtos_por_nome = Produto.objects.filter(nome__icontains=query_nome)

    context = {
        'query_nome': query_nome,
        'query_id': query_id,
        'produto_por_id': produto_por_id,
        'produtos_por_nome': produtos_por_nome
    }
    return render(request, 'buscar_produto.html', context)



def modificar_produto(request, produto_id):
    try:
        produto = Produto.objects.get(id=produto_id)
    except Produto.DoesNotExist:
        produto = None

    if request.method == 'POST':
        novo_nome = request.POST.get('novo_nome')
        novo_valor = request.POST.get('novo_valor')
        novo_quantidade = request.POST.get('novo_quantidade')
        nova_imagem = request.FILES.get('nova_imagem')

        if novo_nome:
            produto.nome = novo_nome
        if novo_valor:
            produto.valor = novo_valor
        if novo_quantidade:
            produto.quantidade = novo_quantidade
        if nova_imagem:
            produto.foto.delete()  # Remove a imagem atual
            produto.foto = nova_imagem

        produto.save()
        return redirect('buscar_produto')

    context = {
        'produto': produto
    }
    return render(request, 'modificar_produto.html', context)



def realizar_venda(request):
    if request.method == 'POST':
        produto_id = request.POST.get('produto_id')
        quantidade_str = request.POST.get('quantidade')
        data_str = request.POST.get('data')

    
        if quantidade_str:
            quantidade = int(quantidade_str)
        else:
            quantidade = 0

        produto = Produto.objects.get(id=produto_id)

        if quantidade > produto.quantidade:
            return render(request, 'realizar_venda.html', {'produto': produto, 'hoje': datetime.now(), 'error_message': 'Quantidade insuficiente em estoque'})

        valor_total = Decimal(produto.valor) * quantidade

        # Obter a data atual
        data_venda = datetime.now().date()

        venda = Venda(produto=produto, quantidade=quantidade, valor_total=valor_total, data_venda=data_venda)
        venda.save()

        produto.quantidade -= quantidade
        produto.save()

        return render(request, 'realizar_venda.html', {'produto': produto, 'hoje': datetime.now()})

    produtos = Produto.objects.all()
    hoje = datetime.now()
    return render(request, 'realizar_venda.html', {'produtos': produtos, 'hoje': hoje})


def deletar_produto(request, produto_id):
    try:
        produto = Produto.objects.get(id=produto_id)
        produto.delete()
        return redirect('listar_produto')
    except Produto.DoesNotExist:

        return render(request, 'erro.html', {'mensagem': 'Produto não encontrado'})






def calcular_valor_total_estoque():
    return Produto.objects.annotate(valor_total_estoque=F('quantidade') * F('valor')).aggregate(total_estoque=Sum('valor_total_estoque'))['total_estoque']

def estatisticas_vendas(request):
    mes_atual = timezone.now().month
    ano_atual = timezone.now().year
    vendas = Venda.objects.all().order_by('data_venda')

    produtos_vendidos = Venda.objects.filter(data_venda__month=mes_atual)

    quantidade_total_estoque = Produto.objects.aggregate(total_estoque=Sum('quantidade', field='quantidade * valor'))['total_estoque']
    valor_vendas_mes = produtos_vendidos.aggregate(valor_mes=Sum('valor_total'))['valor_mes']
    valor_vendas_ano = Venda.objects.filter(data_venda__year=ano_atual).aggregate(valor_ano=Sum('valor_total'))['valor_ano']

    produto_mais_vendido = produtos_vendidos.values('produto__nome').annotate(Sum('quantidade')).order_by('-quantidade__sum').first()

    produto_menos_vendido = produtos_vendidos.values('produto__nome').annotate(
        quantidade_total=Sum('quantidade')).order_by('quantidade_total').first()

    valor_total_estoque = calcular_valor_total_estoque()

    context = {
        'mes_atual': mes_atual,
        'ano_atual': ano_atual,
        'produtos_vendidos': produtos_vendidos,
        'quantidade_total_estoque': quantidade_total_estoque,
        'valor_vendas_mes': valor_vendas_mes,
        'valor_vendas_ano': valor_vendas_ano,
        'produto_mais_vendido': produto_mais_vendido,
        'produto_menos_vendido': produto_menos_vendido,
        'valor_total_estoque': valor_total_estoque,
    }

    return render(request, 'estatisticas_vendas.html', context)




def excluir_venda(request, venda_id):
    venda = get_object_or_404(Venda, id=venda_id)

    # Atualiza o estoque do produto
    produto = venda.produto
    produto.quantidade += venda.quantidade
    produto.save()

    # Atualiza o valor das vendas no mês e no ano
    mes_atual = date.today().month
    ano_atual = date.today().year

    vendas_mes = Venda.objects.filter(data_venda__month=mes_atual).aggregate(Sum('valor_total'))['valor_total__sum']
    vendas_ano = Venda.objects.filter(data_venda__year=ano_atual).aggregate(Sum('valor_total'))['valor_total__sum']

    # Atualiza a venda
    venda.delete()

    return redirect('estatisticas_vendas')



def estatisticas_anuais(request):
    # Obtenha o ano selecionado a partir dos parâmetros da requisição
    ano_selecionado = request.GET.get('ano')

    # Realize o cálculo das estatísticas para o ano selecionado
    if ano_selecionado:
        # Converta o ano selecionado para um valor numérico inteiro
        ano = int(ano_selecionado)

        # Restante do código para calcular as estatísticas usando o ano selecionado

    return render(request, 'estatisticas_anuais.html')





def grafico_vendas_mes_a_mes(request, ano):
    vendas_por_mes = Venda.objects.filter(data_venda__year=ano).values('data_venda__month').annotate(
        total=Sum('valor_total'))

    meses = [str(mes['data_venda__month']) for mes in vendas_por_mes]
    valores = [mes['total'] for mes in vendas_por_mes]

    context = {
        'ano': ano,
        'meses': meses,
        'valores': valores,
    }

    return render(request, 'grafico_vendas_mes_a_mes.html', context)




def produtos_estoque(request):
    produtos_0 = Produto.objects.filter(quantidade__in=[0]).order_by('nome')
    produtos_1 = Produto.objects.filter(quantidade__in=[1]).order_by('nome')
    produtos_2 = Produto.objects.filter(quantidade__in=[2]).order_by('nome')
    produtos_3 = Produto.objects.filter(quantidade__in=[3]).order_by('nome')

    context = {
        'produtos_0': produtos_0,
        'produtos_1': produtos_1,
        'produtos_2': produtos_2,
        'produtos_3': produtos_3,
    }
    return render(request, 'produtos_estoque.html', context)







