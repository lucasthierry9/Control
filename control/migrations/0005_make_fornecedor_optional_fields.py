from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("control", "0004_estados_e_empresas"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fornecedor",
            name="cpf_cnpj",
            field=models.CharField(blank=True, default="", max_length=14),
        ),
        migrations.AlterField(
            model_name="fornecedor",
            name="email",
            field=models.EmailField(blank=True, default="", max_length=254),
        ),
        migrations.AlterField(
            model_name="fornecedor",
            name="telefone",
            field=models.CharField(blank=True, default="", max_length=11),
        ),
    ]
