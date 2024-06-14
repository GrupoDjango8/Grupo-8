# Generated by Django 5.0.6 on 2024-06-13 03:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webGOcho', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio_total', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Precio total')),
                ('estado', models.CharField(choices=[('PENDIENTE', 'Pendiente'), ('ENTREGADO', 'Entregado')], default='PENDIENTE', max_length=10, verbose_name='Estado del pedido')),
                ('numero_mesa', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='webGOcho.cliente', verbose_name='Numero de mesa')),
            ],
        ),
        migrations.CreateModel(
            name='PedidoItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(default=1)),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webGOcho.menu')),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webGOcho.pedido')),
            ],
        ),
        migrations.AddField(
            model_name='pedido',
            name='comida_bebida',
            field=models.ManyToManyField(through='webGOcho.PedidoItem', to='webGOcho.menu'),
        ),
    ]
