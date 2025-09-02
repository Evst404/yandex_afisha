from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0005_auto_20250902_1853'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='placeimage',
            index=models.Index(fields=['order'], name='places_order_idx'),
        ),
    ]