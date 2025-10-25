from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0002_add_version_generatorjob'),
    ]

    operations = [
        migrations.AddField(
            model_name='generatorjob',
            name='params',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
