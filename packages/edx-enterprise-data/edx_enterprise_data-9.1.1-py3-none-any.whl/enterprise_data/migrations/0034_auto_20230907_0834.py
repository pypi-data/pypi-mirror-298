# Generated by Django 3.2.20 on 2023-09-07 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise_data', '0033_enterpriseadminlearnerprogress_enterpriseadminsummarizeinsights'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnterpriseSubsidyBudget',
            fields=[
                ('id', models.CharField(db_index=True, max_length=32, primary_key=True, serialize=False)),
                ('subsidy_access_policy_uuid', models.UUIDField()),
                ('subsidy_uuid', models.UUIDField()),
                ('enterprise_customer_uuid', models.UUIDField()),
                ('enterprise_customer_name', models.CharField(max_length=255, null=True)),
                ('subsidy_access_policy_description', models.CharField(max_length=500, null=True)),
                ('subsidy_title', models.CharField(max_length=255, null=True)),
                ('catalog_name', models.CharField(max_length=255, null=True)),
                ('subsidy_access_policy_type', models.CharField(max_length=255, null=True)),
                ('date_created', models.DateTimeField(null=True)),
                ('subsidy_start_datetime', models.DateTimeField(null=True)),
                ('subsidy_expiration_datetime', models.DateTimeField(null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_test', models.BooleanField(default=False)),
                ('ocm_usage', models.FloatField(null=True)),
                ('exec_ed_usage', models.FloatField(null=True)),
                ('usage_total', models.FloatField(null=True)),
                ('enterprise_contract_discount_percent', models.FloatField(null=True)),
                ('starting_balance', models.FloatField(null=True)),
                ('amount_of_policy_spent', models.FloatField(null=True)),
                ('remaining_balance', models.FloatField(null=True)),
                ('percent_of_policy_spent', models.FloatField(null=True)),
            ],
            options={
                'verbose_name': 'Enterprise Subsidy Budget',
                'verbose_name_plural': 'Enterprise Subsidy Budgets',
                'db_table': 'ent_subsidy_access_policy_aggregates',
            },
        ),
        migrations.AddField(
            model_name='enterpriselearnerenrollment',
            name='budget_id',
            field=models.UUIDField(db_index=True, null=True),
        ),
    ]
