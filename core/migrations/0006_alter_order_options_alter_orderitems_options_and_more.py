# Generated by Django 4.1 on 2023-10-05 02:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_order_orderitems_remove_cartorderitems_item_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="order", options={"verbose_name_plural": "Orders"},
        ),
        migrations.AlterModelOptions(
            name="orderitems", options={"verbose_name_plural": "Order Items"},
        ),
        migrations.RemoveField(model_name="orderitems", name="product_status",),
        migrations.AddField(
            model_name="order",
            name="destination",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.address",
            ),
            preserve_default=False,
        ),
    ]