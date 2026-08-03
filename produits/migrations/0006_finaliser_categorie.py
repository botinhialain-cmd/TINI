import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produits', '0005_migrer_categories_existantes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produit',
            name='categorie',
        ),
        migrations.RenameField(
            model_name='produit',
            old_name='categorie_temp',
            new_name='categorie',
        ),
        migrations.AlterField(
            model_name='produit',
            name='categorie',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='produits',
                to='produits.categorie',
            ),
        ),
        migrations.AlterModelOptions(
            name='produit',
            options={'ordering': ['categorie__ordre', 'nom']},
        ),
    ]
