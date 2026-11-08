from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_alter_skill_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='logo',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='education',
            name='website',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
