# Generated by Django 2.1.3 on 2019-01-26 07:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_firewallrule'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='firewallrule',
            unique_together={('firewall', 'name')},
        ),
    ]