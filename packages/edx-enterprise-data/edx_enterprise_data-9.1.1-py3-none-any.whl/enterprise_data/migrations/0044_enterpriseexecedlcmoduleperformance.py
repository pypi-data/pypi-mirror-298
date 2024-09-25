# Generated by Django 4.2.14 on 2024-08-08 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise_data', '0040_auto_20240718_0536_squashed_0043_alter_enterpriselearnerenrollment_enterprise_enrollment_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnterpriseExecEdLCModulePerformance',
            fields=[
                ('module_performance_unique_id', models.CharField(max_length=350, primary_key=True, serialize=False)),
                ('registration_id', models.PositiveIntegerField(null=True)),
                ('subsidy_transaction_id', models.UUIDField(null=True)),
                ('enterprise_customer_uuid', models.UUIDField(db_index=True, null=True)),
                ('ocm_lms_user_id', models.PositiveIntegerField(null=True)),
                ('is_internal_subsidy', models.BooleanField(null=True)),
                ('ocm_enrollment_id', models.PositiveIntegerField(null=True)),
                ('ocm_courserun_key', models.CharField(max_length=255, null=True)),
                ('university_name', models.CharField(max_length=500, null=True)),
                ('university_abbreviation', models.CharField(max_length=255, null=True)),
                ('partner_short_name', models.CharField(max_length=255, null=True)),
                ('university_country', models.CharField(max_length=255, null=True)),
                ('school', models.CharField(max_length=500, null=True)),
                ('faculty', models.CharField(max_length=500, null=True)),
                ('department', models.CharField(max_length=500, null=True)),
                ('course_code', models.PositiveIntegerField(null=True)),
                ('course_name', models.CharField(db_index=True, max_length=500)),
                ('course_abbreviation', models.CharField(max_length=128, null=True)),
                ('course_abbreviation_short', models.CharField(max_length=64, null=True)),
                ('course_type', models.CharField(max_length=128, null=True)),
                ('subject_vertical', models.CharField(max_length=128, null=True)),
                ('presentation_abbreviation', models.CharField(max_length=128, null=True)),
                ('presentation_name', models.CharField(max_length=500, null=True)),
                ('presentation_code', models.PositiveIntegerField(null=True)),
                ('presentation_close_date', models.DateField(null=True)),
                ('presentation_start_date', models.DateField(null=True)),
                ('promotion_code', models.CharField(max_length=255, null=True)),
                ('promotion_category_name', models.CharField(max_length=255, null=True)),
                ('product_type', models.CharField(max_length=128, null=True)),
                ('product_life_cycle_status', models.CharField(max_length=128, null=True)),
                ('enrolment_id', models.PositiveIntegerField(null=True)),
                ('olc_user_id', models.PositiveIntegerField(null=True)),
                ('first_name', models.CharField(max_length=255, null=True)),
                ('last_name', models.CharField(max_length=255, null=True)),
                ('username', models.CharField(db_index=True, max_length=255)),
                ('status', models.CharField(max_length=128, null=True)),
                ('company_name', models.CharField(max_length=255, null=True)),
                ('module_number', models.PositiveIntegerField(null=True)),
                ('module_name', models.CharField(max_length=255, null=True)),
                ('module_1_release_date', models.DateField(null=True)),
                ('last_module_release_date', models.DateField(null=True)),
                ('last_module_end_date', models.DateField(null=True)),
                ('final_mark', models.DecimalField(decimal_places=2, max_digits=38, null=True)),
                ('assign_grade', models.DecimalField(decimal_places=2, max_digits=38, null=True)),
                ('last_access', models.DateField(null=True)),
                ('all_activities_completed_count', models.PositiveIntegerField(null=True)),
                ('all_activities_total_count', models.PositiveIntegerField(null=True)),
                ('percentage_completed_activities', models.DecimalField(decimal_places=2, max_digits=38, null=True)),
                ('extensions_requested', models.PositiveIntegerField(null=True)),
                ('module_grade', models.DecimalField(decimal_places=2, max_digits=38, null=True)),
                ('log_viewed', models.PositiveIntegerField(null=True)),
                ('hours_online', models.DecimalField(decimal_places=2, max_digits=38, null=True)),
                ('orientation_module_accessed', models.CharField(max_length=128, null=True)),
                ('graded_activities_completed_count', models.PositiveIntegerField(null=True)),
                ('graded_activities_total_count', models.PositiveIntegerField(null=True)),
                ('percentage_completed_graded_activities', models.DecimalField(decimal_places=2, max_digits=38, null=True)),
                ('assessment_activities_completed_count', models.PositiveIntegerField(null=True)),
                ('assessment_activities_total_count', models.PositiveIntegerField(null=True)),
                ('course_material_activities_completed_count', models.PositiveIntegerField(null=True)),
                ('course_material_activities_total_count', models.PositiveIntegerField(null=True)),
                ('discussion_forum_activities_completed_count', models.PositiveIntegerField(null=True)),
                ('discussion_forum_activities_total_count', models.PositiveIntegerField(null=True)),
                ('pass_grade', models.DecimalField(decimal_places=2, max_digits=38, null=True)),
            ],
            options={
                'verbose_name': 'Exec Ed LC Module Performance',
                'verbose_name_plural': 'Exec Ed LC Module Performance',
                'db_table': 'exec_ed_lc_module_performance',
                'ordering': ['last_access'],
            },
        ),
    ]
