from os.path import splitext
from django.db import models
from django.forms import FileField
from django.utils.html import format_html
from wagtailcaptcha.models import WagtailCaptchaForm
from wagtailcaptcha.forms import WagtailCaptchaFormBuilder
from wagtail.contrib.forms.models import AbstractFormField, FORM_FIELD_CHOICES
from wagtail.contrib.forms.views import SubmissionsListView
from wagtail.documents import get_document_model
from wagtail.admin.panels import InlinePanel
from modelcluster.fields import ParentalKey


class ExtendedFormBuilder(WagtailCaptchaFormBuilder):

    def create_document_field(self, field, options):
        return FileField(**options)
    

class CustomSubmissionsListView(SubmissionsListView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not self.is_export:
            # generate a list of field types, the first being the injected 'submission date'
            field_types = ['submission_date'] + [field.field_type for field in self.form_page.get_form_fields()]
            data_rows = context['data_rows']

            DocumentModel = get_document_model()

            for data_row in data_rows:

                fields = data_row['fields']

                for idx, (value, field_type) in enumerate(zip(fields, field_types)):
                    
                    if field_type == 'document' and value:
                        document = DocumentModel.objects.get(pk=value)
                        document_url = document.url
                        document_title = document.title
                        fields[idx] = format_html(
                            "<a href='{}'>{}</a>",
                            document_url,
                            document_title
                        )

        return context


class ApplicationPage(WagtailCaptchaForm):
    parent_page_types = [
        'home.HomePage'
    ]
    subpage_types = []

    form_builder = ExtendedFormBuilder
    submissions_list_view_class = CustomSubmissionsListView

    template = "applications/application_page.html"

    content_panels = WagtailCaptchaForm.content_panels + [
        InlinePanel('form_fields', label='Form Fields For Resume')
    ]

    @staticmethod
    def get_file_title(filename):
        if filename:
            result = splitext(filename)[0]
            result = result.replace('-', ' ').replace('_', ' ')
            return result.title()
        return ''
    
    
    def process_form_submission(self, form):

        cleaned_data = form.cleaned_data

        for name, field in form.fields.items():

            if isinstance(field, FileField):
                file_data = cleaned_data[name]
                if file_data:
                    DocumentModel = get_document_model()
                    kwargs = {
                        'file': cleaned_data[name],
                        'title': self.get_file_title(cleaned_data[name].name),
                    }

                    if form.user and not form.user.is_anonymous:
                        kwargs['uploaded_by_user'] = form.user

                    document = DocumentModel(**kwargs)
                    document.save()
                    cleaned_data.update({name: document.pk})
                else:
                    del cleaned_data[name]


        submission = self.get_submission_class().objects.create(
            form_data=form.cleaned_data,
            page=self,
        )

        return submission
    
    class Meta:
        verbose_name = "Application Page"
        verbose_name_plural = "Application pages"




class ApplicationForm(AbstractFormField):
    FORM_FIELD_CHOICES = list(FORM_FIELD_CHOICES) + [('document', 'Upload Document')]
    field_type = models.CharField(verbose_name='field type', max_length=16, choices=FORM_FIELD_CHOICES)

    page = ParentalKey(ApplicationPage, on_delete=models.CASCADE, related_name='form_fields')

