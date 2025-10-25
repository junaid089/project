from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actions', models.JSONField(default=list)),
                ('note', models.CharField(blank=True, max_length=255)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('asset', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='versions', to='editor.asset')),
            ],
        ),
        migrations.CreateModel(
            name='GeneratorJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prompt', models.TextField()),
                ('count', models.PositiveSmallIntegerField(default=1)),
                ('size', models.CharField(default='512x512', max_length=32)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('completed', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='generatorjob',
            name='result_assets',
            field=models.ManyToManyField(blank=True, related_name='generator_jobs', to='editor.asset'),
        ),
    ]
