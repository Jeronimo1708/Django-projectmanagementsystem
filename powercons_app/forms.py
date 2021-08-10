from django import forms 
from django.forms import Form
from powercons_app.models import Projects, Contracts

States = (
    ('AL', 'Alabama'), 
    ('AK', 'Alaska'), 
    ('AS', 'American Samoa'), 
    ('AZ', 'Arizona'), 
    ('AR', 'Arkansas'), 
    ('AA', 'Armed Forces Americas'), 
    ('AE', 'Armed Forces Europe'), 
    ('AP', 'Armed Forces Pacific'), 
    ('CA', 'California'), 
    ('CO', 'Colorado'), 
    ('CT', 'Connecticut'), 
    ('DE', 'Delaware'), 
    ('DC', 'District of Columbia'), 
    ('FL', 'Florida'), 
    ('GA', 'Georgia'), 
    ('GU', 'Guam'), 
    ('HI', 'Hawaii'), 
    ('ID', 'Idaho'), 
    ('IL', 'Illinois'), 
    ('IN', 'Indiana'), 
    ('IA', 'Iowa'), 
    ('KS', 'Kansas'), 
    ('KY', 'Kentucky'), 
    ('LA', 'Louisiana'), 
    ('ME', 'Maine'), 
    ('MD', 'Maryland'), 
    ('MA', 'Massachusetts'), 
    ('MI', 'Michigan'), 
    ('MN', 'Minnesota'), 
    ('MS', 'Mississippi'), 
    ('MO', 'Missouri'), 
    ('MT', 'Montana'), 
    ('NE', 'Nebraska'), 
    ('NV', 'Nevada'), 
    ('NH', 'New Hampshire'), 
    ('NJ', 'New Jersey'), 
    ('NM', 'New Mexico'), 
    ('NY', 'New York'), 
    ('NC', 'North Carolina'), 
    ('ND', 'North Dakota'), 
    ('MP', 'Northern Mariana Islands'), 
    ('OH', 'Ohio'), 
    ('OK', 'Oklahoma'), 
    ('OR', 'Oregon'), 
    ('PA', 'Pennsylvania'), 
    ('PR', 'Puerto Rico'), 
    ('RI', 'Rhode Island'), 
    ('SC', 'South Carolina'), 
    ('SD', 'South Dakota'), 
    ('TN', 'Tennessee'), 
    ('TX', 'Texas'), 
    ('UT', 'Utah'), 
    ('VT', 'Vermont'), 
    ('VI', 'Virgin Islands'), 
    ('VA', 'Virginia'), 
    ('WA', 'Washington'), 
    ('WV', 'West Virginia'), 
    ('WI', 'Wisconsin'), 
    ('WY', 'Wyoming')
    )


class DateInput(forms.DateInput):
    input_type = "date"


class AddClientForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    phone = forms.CharField(label="Phone", max_length=15, widget=forms.TextInput(attrs={"class":"form-control"}))
    

    #For Displaying Projects
    try:
        projects = Projects.objects.all()
        project_list = []
        for project in projects:
            single_project = (project.id, project.project_name)
            project_list.append(single_project)
    except:
        project_list = []
    
    #For Displaying Contracts
    try:
        contracts = Contracts.objects.all()
        contract_list = []
        for contract in contracts:
            single_contract = (contract.id, contract.contract_name)
            contract_list.append(single_contract)
            
    except:
        contract_list = []
    
    project = forms.ChoiceField(label="Project", choices=project_list, widget=forms.Select(attrs={"class":"form-control"}))
    contract = forms.ChoiceField(label="Contract", choices=contract_list, widget=forms.Select(attrs={"class":"form-control"}))
    location = forms.ChoiceField(label="Location", choices=States, widget=forms.Select(attrs={"class":"form-control"}))


class EditClientForm(forms.Form):
    
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    location = forms.CharField(label="Location", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))

    #For Displaying Projects
    try:
        projects = Projects.objects.all()
        project_list = []
        for project in projects:
            single_project = (project.id, project.project_name)
            project_list.append(single_project)
    except:
        project_list = []

    #For Displaying Contracts
    try:
        contracts = Contracts.objects.all()
        contract_list = []
        for contract in contracts:
            single_contract = (contract.id, contract.contract_name)
            contract_list.append(single_contract)
            
    except:
        contract_list = []
        
    project_id = forms.ChoiceField(label="Project", choices=project_list, widget=forms.Select(attrs={"class":"form-control"}))
    contract_id = forms.ChoiceField(label="Contract", choices=contract_list, widget=forms.Select(attrs={"class":"form-control"}))
    location = forms.ChoiceField(label="Location", choices=States, widget=forms.Select(attrs={"class":"form-control"}))