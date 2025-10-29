from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0003_generatorjob_params'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='preview_image',
            field=models.ImageField(blank=True, null=True, upload_to='previews/'),
        ),
    ]
