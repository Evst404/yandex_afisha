from django.db import migrations, models
import ckeditor.fields

class Migration(migrations.Migration):

    dependencies = [
        ('places', '0004_auto_20250902_1443'), 
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='title',
            field=models.CharField(max_length=300, verbose_name='Название места'),
        ),
        migrations.AlterField(
            model_name='place',
            name='short_description',
            field=models.TextField(blank=True, verbose_name='Краткое описание'),
        ),
        migrations.AlterField(
            model_name='place',
            name='long_description',
            field=ckeditor.fields.RichTextField(blank=True, verbose_name='Длинное описание'),
        ),
        migrations.AlterField(
            model_name='place',
            name='coordinates',
            field=models.JSONField(default=dict, verbose_name='Координаты'),
        ),
        migrations.AlterField(
            model_name='placeimage',
            name='place',
            field=models.ForeignKey(
                related_name='images',
                on_delete=models.CASCADE,
                to='places.place',
                verbose_name='Место'
            ),
        ),
        migrations.AlterField(
            model_name='placeimage',
            name='image',
            field=models.ImageField(upload_to='place_images/', verbose_name='Картинка'),
        ),
        migrations.AlterField(
            model_name='placeimage',
            name='order',
            field=models.PositiveIntegerField(default=0, verbose_name='Порядок'),
        ),
    ]