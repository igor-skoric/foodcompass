from decimal import Decimal

from django.db import migrations, models


def copy_amount_to_agreed(apps, schema_editor):
    Partner = apps.get_model('website', 'Partner')
    for partner in Partner.objects.all():
        Partner.objects.filter(pk=partner.pk).update(
            agreed_amount=partner.amount or Decimal('0'),
        )


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_partner_payments_due'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner',
            name='agreed_amount',
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=12,
                verbose_name='Dogovoreni iznos',
            ),
        ),
        migrations.AlterField(
            model_name='partner',
            name='amount',
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=12,
                verbose_name='Uplaćeno',
            ),
        ),
        migrations.RunPython(copy_amount_to_agreed, migrations.RunPython.noop),
    ]
