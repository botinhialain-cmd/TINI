from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produits', '0003_alter_produit_categorie'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(help_text='Ex: Bières, Vins, Cocktails...', max_length=50, unique=True)),
                ('ordre', models.PositiveIntegerField(default=0, help_text="Détermine l'ordre d'affichage des sections sur le menu client (plus petit = affiché en premier)")),
                ('actif', models.BooleanField(default=True, help_text='Décocher pour masquer temporairement toute la catégorie du menu client, sans la supprimer')),
            ],
            options={
                'verbose_name': 'Catégorie',
                'verbose_name_plural': 'Catégories',
                'ordering': ['ordre', 'nom'],
            },
        ),
    ]
