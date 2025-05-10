from django.shortcuts import render
from django.views.generic import TemplateView
from ot.models import Employee, Decree, Company, Program
from django.core.serializers import serialize
from pathlib import Path
from docxtpl import DocxTemplate
from datetime import datetime
import locale

# Create your views here.


class Home(TemplateView):
    template_name = 'index.html'

class CreateProtocols(TemplateView):
    template_name = 'create_protocols.html'
    extra_context = {
        'list': Employee.objects.all(),
        'decrees': Decree.objects.all(),
        'companies': Company.objects.all(),
        'programs': Program.objects.all(),
        'json': serialize('json', Employee.objects.all()),
    }

    def post(self, request, **kwargs):
        my_data = request.POST
        # do something with your data
        print(my_data)

        BASE_DIR = Path(__file__).resolve().parent.parent
        

        def transform_date_month(date, separator):
            months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
                'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
            day,month,year = date.split(separator)
            return f'{months[int(month) - 1]}'
        
        for program in my_data["programs"].split(','):


            company = Company.objects.get(pk=my_data['company'][0])
            decree = Decree.objects.get(pk=my_data['decree'][0])
            program_object = Program.objects.get(pk=program)
            employees = Employee.objects.filter(pk__in=my_data['selected'].split(','))

            print(my_data['selected'].split(','))

            doc_data = {
                'date':  my_data['date'],
                'date_year':  str(datetime.strptime(my_data['date'], "%Y-%m-%d").year).zfill(2),
                'full_month':  transform_date_month(my_data['date'], '-'),
                'date_month':  str(datetime.strptime(my_data['date'], "%Y-%m-%d").month).zfill(2),
                'date_day':  str(datetime.strptime(my_data['date'], "%Y-%m-%d").day).zfill(2),
                'company':  company.title,
                'short_company':  company.short_title,
                'decree_number':  decree.number,
                'decree_date':   f"{decree.date:%d.%m.%Y}",
                'main': f'{decree.main.firstname} {decree.main.lastname[0]}. {decree.main.middlename[0]}.',
                'second': f'{decree.second.firstname} {decree.second.lastname[0]}. {decree.second.middlename[0]}.',
                'third': f'{decree.third.firstname} {decree.third.lastname[0]}. {decree.third.middlename[0]}.',
                'main_pos': f'{decree.main.firstname} {decree.main.lastname[0]}. {decree.main.middlename[0]}. {decree.main.position}',
                'second_pos': f'{decree.second.firstname} {decree.second.lastname[0]}. {decree.second.middlename[0]}. {decree.main.position}',
                'third_pos': f'{decree.third.firstname} {decree.third.lastname[0]}. {decree.third.middlename[0]}. {decree.main.position}',
                'program_title': program_object.title,
                'program_short_title': program_object.short_title,
                'employees': employees
            }

            print(employees)

            def calculate_total(product):
                return product['firstname'] 

            dict_list = list(employees.values("firstname"))
            employees_str = map(calculate_total, dict_list)
            
            locale.setlocale(locale.LC_ALL, locale="ru_RU.utf8")

            document = DocxTemplate(BASE_DIR / f"doc_templates/document_1.docx")
            document.render(doc_data)
            document.save(BASE_DIR / f"generated_docs/Протокол обучения сотрудников {program_object.short_title}-{doc_data['date_year']}{doc_data['date_month']}-{doc_data['date_day']} {', '.join(list(employees_str))} {doc_data['date']}).docx")
    

        context = self.extra_context  #  set your context
        return super(TemplateView, self).render_to_response(context)