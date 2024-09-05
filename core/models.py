from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


def upload_to(instance, filename):
    base_filename, extension = os.path.splitext(filename)
    new_filename = f"{instance.nome}{extension}"
    return f"imagens_produto/{new_filename}"

class Produto(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    quantidade = models.IntegerField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField(blank=True)
    foto = models.ImageField(upload_to='core/static/fotos_produtos', blank=True, null=True)



    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']





class Venda(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    data = models.DateField(default=timezone.now, blank=True, null=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    data_venda = models.DateField()
    foto = models.ImageField(upload_to='core/static/fotos_produtos', blank=True, null=True)

    def __str__(self):
        return f"Venda de {self.quantidade} unidades de {self.produto.nome} em {self.data}"

