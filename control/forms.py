from django import forms
from . models import Cliente, Produto, Funcionario, Vendedor, Fornecedor, Categoria_Produto, Pedidos_Venda
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Div
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, Submit, HTML, Div

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = "__all__"

        labels = {
            "nome": "Nome completo",
            "email": "E-mail",
            "cpf": "CPF",
            "telefone": "Telefone",
            "cep": "CEP",
            "estado": "Estado",
            "cidade": "Cidade",
            "bairro": "Bairro",
            "logradouro": "Logradouro",
            "numero": "Número",
            "complemento": "Complemento",
        }

        widgets = {
            'cep': forms.TextInput(attrs={'maxlength': 9}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        botao_texto = "Salvar" if self.instance and self.instance.pk else "Registrar"

        # Estilo padrão para todos os campos
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'style': 'background-color: #EEEEEE; border: none; border-radius: 8px; height: 45px;'
            })
        
        # Campos não obrigatórios
        optional_fields = ['cep', 'estado', 'cidade', 'bairro', 'logradouro', 'numero', 'complemento',]
        for field_name in optional_fields:
            if field_name in self.fields:
                self.fields[field_name].required = False

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = ''
        self.helper.label_class = 'form-label'
        self.helper.field_class = ''
        
        self.helper.layout = Layout(
            # Seção Dados
            HTML('<h5 style="font-family: Inter; font-weight: 700; margin-bottom: 8px; margin-top: 10px;">Dados</h5>'),
            Row(
                Column('nome', css_class='col-12 col-md-6'),
                Column('email', css_class='col-12 col-md-6'),
            ),
            Row(
                Column('cpf', css_class='col-12 col-md-6'),
                Column('telefone', css_class='col-12 col-md-6'),
            ),
            
            # Seção Endereço
            HTML('<h5 style="font-family: Inter; font-weight: 700; margin-bottom: 8px; margin-top: 10px;">Endereço</h5>'),
            Row(
                Column('cep', css_class='col-6 col-md-2'),
                Column('estado', css_class='col-6 col-md-1'),
                Column('cidade', css_class='col-12 col-md-5'),
                Column('bairro', css_class='col-12 col-md-4'),
            ),
            Row(
                Column('logradouro', css_class='col-12 col-md-6'),
                Column('numero', css_class='col-6 col-md-2'),
                Column('complemento', css_class='col-6 col-md-4'),
            ),
            
            # Botão Submit
            Div(
                Submit('submit', botao_texto, css_class='btn', css_id='btn-registrar',
                       style='background-color: #2563EB; color: white; font-family: Inter; font-weight: 700; font-size: 26px; border-radius: 10px; min-width: 300px; height: 55px;'),
                css_class='mt-4'
            ),
        )

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = "__all__"
        labels = {
            "nome": "Nome completo",
            "categoria": "Categoria",
            "imagem": "Imagem",
            "estado": "Estado",
            "preco": "Preço",
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        botao_texto = "Salvar" if self.instance and self.instance.pk else "Registrar"

        # Estilo padrão para todos os campos
        for field_name, field in self.fields.items():
            if field_name == "imagem":
                field.widget.attrs.update({
                    "class": "form-control-file",
                    "style": "background-color: #EEEEEE; border: none; border-radius: 8px; height: 45px;",
                })
            else:
                field.widget.attrs.update({
                    'class': 'form-control',
                    'style': 'background-color: #EEEEEE; border: none; border-radius: 8px; height: 45px;'
                })

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = ''
        self.helper.label_class = 'form-label'
        self.helper.field_class = ''
        
        self.helper.layout = Layout(
            # Seção Dados
            HTML('<h5 style="font-family: Inter; font-weight: 700; margin-bottom: 8px; margin-top: 10px;">Dados</h5>'),
            Row(
                Column('nome', css_class='col-12 col-md-6'),
                Column('categoria', css_class='col-12 col-md-6'),
            ),
            Row(
                Column('preco', css_class='col-12 col-md-6'),
                Column('imagem', css_class='col-12 col-md-6'),
            ),
            
            # Botão Submit
            Div(
                Submit('submit', botao_texto, css_class='btn', css_id='btn-registrar',
                       style='background-color: #2563EB; color: white; font-family: Inter; font-weight: 700; font-size: 26px; border-radius: 10px; min-width: 300px; height: 55px;'),
                css_class='mb-4'
            ),
        )

class FuncionarioForm(forms.Form):
    nome = forms.CharField(max_length=100, label="Nome completo")
    email = forms.EmailField(label="Email")
    telefone = forms.CharField(max_length=20, label="Telefone")
    cpf = forms.CharField(max_length=11, label="CPF")
    cargo = forms.CharField(max_length=50, label="Cargo")
    senha = forms.CharField(widget=forms.PasswordInput, label="Senha de acesso")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        botao_texto = "Salvar" 

        # Estilo padrão para todos os campos
        for field_name, field in self.fields.items():
            if field_name == "senha":
                field.widget.attrs.update({
                    'class': 'form-control',
                    'style': 'background-color: #EEEEEE; border: none; border-radius: 8px; height: 45px;',
                    'autocomplete': 'new-password',
                })
            else:
                field.widget.attrs.update({
                    'class': 'form-control',
                    'style': 'background-color: #EEEEEE; border: none; border-radius: 8px; height: 45px;'
                })

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = ''
        self.helper.label_class = 'form-label'
        self.helper.field_class = ''
        
        self.helper.layout = Layout(
            # Seção Dados
            HTML('<h5 style="font-family: Inter; font-weight: 700; margin-bottom: 8px; margin-top: 10px;">Dados</h5>'),
            Row(
                Column('nome', css_class='col-12 col-md-6'),
                Column('cargo', css_class='col-12 col-md-6'),
            ),
            Row(
                Column('cpf', css_class='col-12 col-md-6'),
                Column('telefone', css_class='col-12 col-md-6'),
            ),
            Row(
                Column('senha', css_class='col-12 col-md-6'),
            ),
            # Botão Submit
            Div(
                Submit('submit', botao_texto, css_class='btn', css_id='btn-registrar',
                       style='background-color: #2563EB; color: white; font-family: Inter; font-weight: 700; font-size: 26px; border-radius: 10px; min-width: 300px; height: 55px;'),
                css_class='mt-4'
            ),
        )

class VendedorForm(forms.ModelForm):
    class Meta:
        model = Vendedor
        fields = "__all__"
        labels = {
            "nome": "Nome completo",
            "email": "Email",
            "cpf": "CPF",
            "telefone": "Telefone",
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        botao_texto = "Salvar" if self.instance and self.instance.pk else "Cadastrar"

        # Estilo padrão para todos os campos
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'style': 'background-color: #EEEEEE; border: none; border-radius: 8px; height: 45px;'
            })

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = ''
        self.helper.label_class = 'form-label'
        self.helper.field_class = ''
        
        self.helper.layout = Layout(
            # Seção Dados
            HTML('<h5 style="font-family: Inter; font-weight: 700; margin-bottom: 8px; margin-top: 10px;">Dados</h5>'),
            Row(
                Column('nome', css_class='col-12 col-md-6'),
                Column('email', css_class='col-12 col-md-6'),
            ),
            Row(
                Column('cpf', css_class='col-12 col-md-6'),
                Column('telefone', css_class='col-12 col-md-6'),
            ),
            
            # Botão Submit
            Div(
                Submit('submit', botao_texto, css_class='btn', css_id='btn-registrar',
                       style='background-color: #2563EB; color: white; font-family: Inter; font-weight: 700; font-size: 26px; border-radius: 10px; min-width: 300px; height: 55px;'),
                css_class='mt-4'
            ),
        )

class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = "__all__"
        labels = {
            "nome": "Nome completo",
            "email": "Email",
            "cpf_cnpj": "CPF/CNPJ",
            "telefone": "Telefone",
            "cep": "CEP",
            "estado": "Estado",
            "cidade": "Cidade",
            "bairro": "Bairro",
            "logradouro": "Logradouro",
            "numero": "Número",
            "complemento": "Complemento",
        }
        widgets = {
            'cep': forms.TextInput(attrs={'maxlength': 9}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        botao_texto = "Salvar" if self.instance and self.instance.pk else "Registrar"

        # Estilo padrão para todos os campos
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'style': 'background-color: #EEEEEE; border: none; border-radius: 8px; height: 45px;'
            })
        
        # Campos não obrigatórios
        optional_fields = ['cep', 'estado', 'cidade', 'bairro', 'logradouro', 'numero', 'complemento',]
        for field_name in optional_fields:
            if field_name in self.fields:
                self.fields[field_name].required = False

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = ''
        self.helper.label_class = 'form-label'
        self.helper.field_class = ''
        
        self.helper.layout = Layout(
            # Seção Dados
            HTML('<h5 style="font-family: Inter; font-weight: 700; margin-bottom: 8px; margin-top: 10px;">Dados</h5>'),
            Row(
                Column('nome', css_class='col-12 col-md-6'),
                Column('email', css_class='col-12 col-md-6'),
            ),
            Row(
                Column('cpf_cnpj', css_class='col-12 col-md-6'),
                Column('telefone', css_class='col-12 col-md-6'),
            ),
            
            # Seção Endereço
            HTML('<h5 style="font-family: Inter; font-weight: 700; margin-bottom: 8px; margin-top: 10px;">Endereço</h5>'),
            Row(
                Column('cep', css_class='col-6 col-md-2'),
                Column('estado', css_class='col-6 col-md-1'),
                Column('cidade', css_class='col-12 col-md-5'),
                Column('bairro', css_class='col-12 col-md-4'),
            ),
            Row(
                Column('logradouro', css_class='col-12 col-md-6'),
                Column('numero', css_class='col-6 col-md-2'),
                Column('complemento', css_class='col-6 col-md-4'),
            ),
            
            # Botão Submit
            Div(
                Submit('submit', botao_texto, css_class='btn', css_id='btn-registrar',
                       style='background-color: #2563EB; color: white; font-family: Inter; font-weight: 700; font-size: 26px; border-radius: 10px; min-width: 300px; height: 55px;'),
                css_class='mt-2'
            ),
        )

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria_Produto
        fields = "__all__"
        labels = {
            "nome": "Nome",
            "descricao": "Descrição",
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        botao_texto = "Salvar" if self.instance and self.instance.pk else "Criar"

        # Estilo padrão para todos os campos
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'style': 'background-color: #EEEEEE; border: none; border-radius: 8px; height: 45px;'
            })

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = ''
        self.helper.label_class = 'form-label'
        self.helper.field_class = ''
        
        self.helper.layout = Layout(
            # Seção Dados
            HTML('<h5 style="font-family: Inter; font-weight: 700; margin-bottom: 8px; margin-top: 10px;">Dados</h5>'),
            Row(
                Column('nome', css_class='col-12 col-md-6 mb-1'),
                Column('descricao', css_class='col-12 col-md-6 mb-1'),
            ),
            
            # Botão Submit
            Div(
                Submit('submit', botao_texto, css_class='btn', css_id='btn-registrar',
                       style='background-color: #2563EB; color: white; font-family: Inter; font-weight: 700; font-size: 26px; border-radius: 10px; min-width: 300px; height: 55px;'),
                css_class='mt-2'
            ),
        )