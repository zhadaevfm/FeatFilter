# Generated by Django 2.0.2 on 2018-03-06 21:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('feats', '0002_auto_20180306_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='feat',
            name='req_as_text',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='race',
            name='traits',
            field=models.ManyToManyField(to='feats.Trait'),
        ),
        migrations.AlterField(
            model_name='feat',
            name='benefit',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='feat',
            name='completion_benefit',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='feat',
            name='feat_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='feats.FeatType'),
        ),
        migrations.AlterField(
            model_name='feat',
            name='full_text',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='feat',
            name='goal',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='feat',
            name='normal',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='feat',
            name='note',
            field=models.TextField(null=True),
        ),
    ]
