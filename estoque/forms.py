from django import forms
from control.models import Movimentacao, Deposito, Pedidos_Compra
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Div
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, Submit, HTML, Div

class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model =  Movimentacao
        fields = "__all__"
        labels = {
            "tipo": "Tipo",
            "produto": "Produto",
            "quantidade": "Quantidade",
            "deposito": "Depósito",
            "preco_compra": "Preço compra",
            "preco_custo": "Preço custo",
            "dataehora": "Data e hora",
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        botao_texto = "Salvar" if self.instance and self.instance.pk else "Adicionar"

        # Estilo padrão para todos os campos
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'style': 'background-color: #EEEEEE; border: none; border-radius: 8px; height: 45px;'
            })

        # Campos select
        select_fields = ['tipo']
        for field_name in select_fields:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update({
                    'class': 'form-select',
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
                Column('tipo', css_class='col-12 col-md-6'),
                Column('produto', css_class='col-12 col-md-6'),
            ),
            Row(
                Column('quantidade', css_class='col-12 col-md-6'),
                Column('deposito', css_class='col-12 col-md-6'),
            ),
            Row(
                Column('preco_compra', css_class='col-12 col-md-6'),
                Column('preco_custo', css_class='col-12 col-md-6'),
            ),
            Row(
                Column('dataehora', css_class='col-12 col-md-6'),
            ),
            
            # Botão Submit
            Div(
                Submit('submit', botao_texto, css_class='btn', css_id='btn-registrar',
                       style='background-color: #2563EB; color: white; font-family: Inter; font-weight: 700; font-size: 26px; border-radius: 10px; min-width: 300px; height: 55px;'),
                css_class='mt-2'
            ),
        )

class DepositoForm(forms.ModelForm):
    class Meta:
        model =  Deposito
        fields = "__all__"
        labels = {
            "descricao": "Nome",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        botao_texto = "Salvar" if self.instance and self.instance.pk else "Adicionar"

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
            Row(
                Column('descricao', css_class='col-12 col-md-6 mt-2'),
            ),
            
            # Botão Submit
            Div(
                Submit('submit', botao_texto, css_class='btn', css_id='btn-registrar',
                       style='background-color: #2563EB; color: white; font-family: Inter; font-weight: 700; font-size: 26px; border-radius: 10px; min-width: 300px; height: 55px;'),
                css_class='mt-2'
            ),
        )

class Pedidos_CompraForm(forms.ModelForm):
    class Meta:
        model = Pedidos_Compra
        fields = "__all__"
        labels = {
            "fornecedor": "Fornecedor",
            "produto": "Produto",
            "quantidade": "Quantidade",
            "status": "Status",
            "valor": "Valor Total",
        }
        widgets = {
            'quantidade': forms.NumberInput(attrs={'min': 1}),
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
        
        # Campos select
        select_fields = ['fornecedor', 'produto',]
        for field_name in select_fields:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update({
                    'class': 'form-select',
                    'style': 'background-color: #EEEEEE; border: none; border-radius: 8px; height: 45px;'
                })
        
        # Labels personalizados
        self.fields['fornecedor'].empty_label = 'Selecione um fornecedor'
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = ''
        self.helper.label_class = 'form-label'
        self.helper.field_class = ''
        
        self.helper.layout = Layout(
            # Seção Dados
            HTML('<h5 style="font-family: Inter; font-weight: 700; margin-bottom: 8px;">Pedido</h5>'),
            Row(
                Column('fornecedor', css_class='col-12 col-md-6'),
                Column('produto', css_class='col-12 col-md-6'),
            ),
            Row(
                Column('quantidade', css_class='col-12 col-md-6'),
                Column('valor', css_class='col-12 col-md-6'),
            ),
            Row(
                Column('status', css_class='col-12 col-md-6'),
            ),
            
            # Botão Submit
            Div(
                Submit('submit', botao_texto, css_class='btn', css_id='btn-registrar',
                       style='background-color: #2563EB; color: white; font-family: Inter; font-weight: 700; font-size: 26px; border-radius: 10px; min-width: 300px; height: 55px;'),
                css_class='mt-2'
            ),
        )

