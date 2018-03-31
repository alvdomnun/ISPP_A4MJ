# Generated by Django 2.0.2 on 2018-03-30 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elementPrices', '0002_elementprice_profitexercisevalue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elementprice',
            name='buyExerciseValue',
            field=models.DecimalField(decimal_places=2, default=4.0, max_digits=9, verbose_name='Precio de compra'),
        ),
        migrations.AlterField(
            model_name='elementprice',
            name='profitExerciseValue',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=9, verbose_name='Ganancias Climbcode'),
        ),
        migrations.AlterField(
            model_name='elementprice',
            name='promoteExerciseValue',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=9, verbose_name='Precio de promoción'),
        ),
    ]
