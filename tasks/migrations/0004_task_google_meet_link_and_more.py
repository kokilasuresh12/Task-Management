from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_alter_progressupdate_id_alter_task_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='google_meet_link',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='task',
            name='presentation_requested_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
