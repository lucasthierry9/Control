from django import forms
from control.models import Pedidos_Venda
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Div
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, Submit, HTML, Div
from crispy_forms.bootstrap import FormActions



class PedidosVendaForm(forms.ModelForm):
    class Meta:
        model = Pedidos_Venda
        fields = [
            'cliente', 'vendedor', 'produto', 'quantidade',
            'pagamento', 'status', 'data',
            'frete', 'peso', 'valor_frete',
            'cep', 'estado', 'cidade', 'bairro', 'logradouro', 'numero', 'complemento'
        ]
        widgets = {
            'quantidade': forms.NumberInput(attrs={'min': 1}),
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
        
        # Campos select
        select_fields = ['cliente', 'vendedor', 'produto', 'pagamento',]
        for field_name in select_fields:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update({
                    'class': 'form-select',
                    'style': 'background-color: #EEEEEE; border: none; border-radius: 8px; height: 45px;'
                })
        
        # Labels personalizados
        self.fields['cliente'].empty_label = 'Selecione um cliente'
        self.fields['vendedor'].empty_label = 'Selecione um vendedor'
        self.fields['produto'].empty_label = 'Selecione um produto'
        self.fields['pagamento'].empty_label = 'Selecione'
        self.fields['frete'].empty_label = 'Selecione'
        
        # Placeholders
        self.fields['peso'].widget.attrs['placeholder'] = 'Kg'
        self.fields['valor_frete'].widget.attrs['placeholder'] = 'R$'
        
        # Campos não obrigatórios
        optional_fields = ['frete', 'peso', 'valor_frete', 'cep', 'estado', 'cidade', 'bairro', 'logradouro', 'numero', 'complemento', 'numero']
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
                Column('cliente', css_class='col-12 col-md-6 mb-1'),
                Column('vendedor', css_class='col-12 col-md-6 mb-1'),
            ),
            Row(
                Column('produto', css_class='col-12 col-md-6 mb-3'),
                Column('quantidade', css_class='col-12 col-md-6 mb-3'),
            ),
            
            # Seção Pagamento e Transporte
            Row(
                Column(
                    HTML('<h5 style="font-family: Inter; font-weight: 700; margin-bottom: 8px;">Pagamento</h5>'),
                    Row(
                        Column('pagamento', css_class='col-12'),
                    ),
                    css_class='col-12 col-md-6'
                ),
                Column(
                    HTML('<h5 style="font-family: Inter; font-weight: 700; margin-bottom: 8px;">Transporte</h5>'),
                    Row(
                        Column('frete', css_class='col-5'),
                        Column('peso', css_class='col-3'),
                        Column('valor_frete', css_class='col-4'),
                    ),
                    css_class='col-12 col-md-6'
                ),
            ),
            
            # Seção Endereço
            HTML('<h5 style="font-family: Inter; font-weight: 700; margin-bottom: 8px; margin-top: 10px;">Endereço de entrega</h5>'),
            Row(
                Column('cep', css_class='col-6 col-md-2'),
                Column('estado', css_class='col-6 col-md-1'),
                Column('cidade', css_class='col-12 col-md-5'),
                Column('bairro', css_class='col-12 col-md-4'),
            ),
            Row(
                Column('logradouro', css_class='col-12 col-md-6'),
                Column('numero', css_class='col-6 col-md-2'),
                Column('data', css_class='col-6 col-md-4'),
            ),
            Row(
                Column('complemento', css_class='col-12'),
                Column('status', css_class='col-12'),
            ),
            
            # Botão Submit
            Div(
                Submit('submit', botao_texto, css_class='btn', css_id='btn-registrar',
                       style='background-color: #2563EB; color: white; font-family: Inter; font-weight: 700; font-size: 26px; border-radius: 10px; min-width: 300px; height: 55px;'),
                css_class='mt-4 mb-4'
            ),
        )
