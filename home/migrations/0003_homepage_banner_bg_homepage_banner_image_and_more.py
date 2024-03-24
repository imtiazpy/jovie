# Generated by Django 5.0 on 2024-03-24 14:35

import django.db.models.deletion
import wagtail.blocks
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_create_homepage'),
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='banner_bg',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='banner_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='banner_subtitle',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='banner_tagline',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='banner_title',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='buttons',
            field=wagtail.fields.StreamField([('btn', wagtail.blocks.StructBlock([('btn_label', wagtail.blocks.CharBlock(label='Label', max_length=20, required=False)), ('link_url', wagtail.blocks.URLBlock(label='external URL', required=False)), ('link_page', wagtail.blocks.PageChooserBlock(required=False))]))], blank=True, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='why_us',
            field=wagtail.fields.StreamField([('why_us', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Title', max_length=200, required=False)), ('subtitle', wagtail.blocks.CharBlock(label='Subtitle', max_length=400, required=False)), ('cards', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('icon_class', wagtail.blocks.CharBlock(help_text='ex: flaticon-resume', label='Icon Class Name', max_length=100, required=False)), ('title', wagtail.blocks.CharBlock(label='Title', max_length=100, required=False)), ('content', wagtail.blocks.TextBlock(help_text='Content of the card', required=False))], required=False)))]))], blank=True, null=True),
        ),
    ]
