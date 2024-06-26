# Generated by Django 5.0 on 2024-04-01 11:50

import django.db.models.deletion
import streams.models
import wagtail.blocks
import wagtail.fields
import wagtail.snippets.blocks
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0091_remove_revision_submitted_for_moderation'),
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('banner_tagline', models.CharField(blank=True, max_length=200, null=True)),
                ('banner_title', models.CharField(blank=True, max_length=300, null=True)),
                ('banner_subtitle', models.CharField(blank=True, max_length=400, null=True)),
                ('buttons', wagtail.fields.StreamField([('btn', wagtail.blocks.StructBlock([('btn_label', wagtail.blocks.CharBlock(label='Label', max_length=20, required=False)), ('link_url', wagtail.blocks.URLBlock(label='external URL', required=False)), ('link_page', wagtail.blocks.PageChooserBlock(required=False))]))], blank=True, null=True)),
                ('why_us', wagtail.fields.StreamField([('why_us', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(label='Title', max_length=200, required=False)), ('subtitle', wagtail.blocks.CharBlock(label='Subtitle', max_length=400, required=False)), ('cards', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('icon_class', wagtail.blocks.CharBlock(help_text='ex: flaticon-resume', label='Flat Icon Class Name', max_length=100, required=False)), ('title', wagtail.blocks.CharBlock(label='Title', max_length=100, required=False)), ('content', wagtail.blocks.TextBlock(help_text='Content of the card', required=False))], required=False)))]))], blank=True, null=True)),
                ('job_categories', wagtail.fields.StreamField([('job_category', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(label='Heading', max_length=400, required=False)), ('sub_heading', wagtail.blocks.CharBlock(label='Sub heading', max_length=500, required=False)), ('categories', wagtail.blocks.ListBlock(wagtail.snippets.blocks.SnippetChooserBlock(streams.models.Category)))]))], blank=True, null=True)),
                ('banner_bg', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
                ('banner_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'verbose_name_plural': 'Home pages',
            },
            bases=('wagtailcore.page',),
        ),
    ]
