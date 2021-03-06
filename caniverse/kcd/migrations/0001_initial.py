# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-15 05:36
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import kcd.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(help_text='Human-readable name of the bus network (e.g. "Comfort").')),
                ('baudrate', models.IntegerField(default=500000, help_text='Nominal data transfer rate in baud (e.g. 500000, 125000, 100000 or 83333).', validators=[kcd.validators.RangeValidator(5000, 1000000, code='baud_rate', message='Baud rate must be between %(lower)s and %(upper)s. (it is %(value)s).')])),
            ],
            options={
                'verbose_name_plural': 'Buses',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, help_text='Describes the scope of application e.g. the target vehicle or controlled device.')),
                ('version', models.TextField(blank=True, help_text='The version of the network definition document.')),
                ('author', models.TextField(blank=True, help_text='The owner or author of the network definition document.')),
                ('company', models.TextField(blank=True, help_text='The owner company of the network definition document.')),
                ('date', models.TextField(blank=True, help_text='The release date of this version of the network definition document.')),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(help_text='Human-readable name for this value.')),
                ('label_type', models.CharField(choices=[('value', 'value'), ('invalid', 'invalid'), ('error', 'error')], default='value', help_text='Type of value: "value", "invalid" or "error".', max_length=7)),
                ('value', models.IntegerField(help_text='Signal raw value that is described here.', validators=[django.core.validators.MinValueValidator(0, message='Must be non-negative, was %(value)s')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LabelGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(help_text='Human-readable name for this value.')),
                ('label_type', models.CharField(choices=[('value', 'value'), ('invalid', 'invalid'), ('error', 'error')], default='value', help_text='Type of value: "value", "invalid" or "error".', max_length=7)),
                ('raw_from', models.PositiveIntegerField(help_text='Signal raw value the label group is starting with.')),
                ('raw_to', models.PositiveIntegerField(help_text='Signal raw value the label group is ending with.')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LabelSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField(blank=True, help_text='Describes the purpose of the signal/variable and/or comments on its usage.')),
                ('message_id', models.TextField(help_text='The unique identifier of the message. May have 11-bit (Standard frame format) or 29-bit (Extended frame format). The identifier is usually written in hexadecimal format e.g. 0x123. If format is "extended" this identifier includes both Base ID (11 bits) and Extended ID (18 bits).', validators=[django.core.validators.RegexValidator(regex='0x[A-F0-9]+')])),
                ('name', models.TextField(help_text='Human-readable name of the network message (e.g."OBD-Info").')),
                ('length', models.CharField(help_text='Number of bytes available in the data field of the message (data length code). "auto" (default) calculate minimum length for the contained signals in the message.', max_length=4, validators=[django.core.validators.RegexValidator(regex='r([0-8])|(auto)')])),
                ('interval', models.PositiveIntegerField(default=0, help_text='Repetition interval of a cyclic network message in milliseconds.', validators=[kcd.validators.RangeValidator(0, 60000, code='interval')])),
                ('triggered', models.BooleanField(default=False, help_text='Sending behavior of the network message. True, if message is triggered by signal changes.')),
                ('count', models.PositiveIntegerField(default=0, help_text='Number of repetitions of a triggered network message. 0 (default) for infinitee repetitions.')),
                ('format', models.CharField(choices=[('standard', 'standard'), ('extenteded', 'exteneded')], default='standard', help_text='Frame format of the network message.', max_length=8, validators=[django.core.validators.RegexValidator(regex='(standard)|(extended)')])),
                ('remote', models.BooleanField(default=False, help_text='True, if message is a remote frame.')),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kcd.Bus')),
            ],
        ),
        migrations.CreateModel(
            name='Multiplex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('endianess', models.CharField(choices=[('little', 'little'), ('big', 'big')], default='little', help_text='Determines if Byteorder is big-endian (Motorola), little-endian (Intel) otherwise.', max_length=6)),
                ('length', models.IntegerField(default=1, help_text='Bit length of the signal.', validators=[kcd.validators.RangeValidator(1, 64)])),
                ('name', models.TextField(help_text='Human readable name of the signal.')),
                ('offset', models.IntegerField(help_text='Least significant bit offset of the signal relative to the least significant bit of the messages data payload.', validators=[kcd.validators.RangeValidator(0, 63)])),
                ('notes', models.TextField(blank=True, help_text='Describes the purpose of the signal/variable and/or comments on its usage.')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MuxGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(help_text='Count value of the Multiplex when the signals of this group become valid.', validators=[django.core.validators.MinValueValidator(0)])),
                ('multiplex', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kcd.Multiplex')),
            ],
        ),
        migrations.CreateModel(
            name='NetworkDefinition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='kcd.Document')),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('node_id', models.TextField(help_text='Unique identifier of the network node.')),
                ('name', models.TextField(blank=True, help_text='Human-readable name of the network node (e.g. "Brake").', null=True, unique=True)),
                ('network', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kcd.NetworkDefinition')),
            ],
        ),
        migrations.CreateModel(
            name='NodeRef',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('node_ref', models.OneToOneField(help_text='Referencing a network node by its unique identifier.', on_delete=django.db.models.deletion.CASCADE, to='kcd.Node')),
            ],
        ),
        migrations.CreateModel(
            name='Signal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('endianess', models.CharField(choices=[('little', 'little'), ('big', 'big')], default='little', help_text='Determines if Byteorder is big-endian (Motorola), little-endian (Intel) otherwise.', max_length=6)),
                ('length', models.IntegerField(default=1, help_text='Bit length of the signal.', validators=[kcd.validators.RangeValidator(1, 64)])),
                ('name', models.TextField(help_text='Human readable name of the signal.')),
                ('offset', models.IntegerField(help_text='Least significant bit offset of the signal relative to the least significant bit of the messages data payload.', validators=[kcd.validators.RangeValidator(0, 63)])),
                ('notes', models.TextField(blank=True, help_text='Describes the purpose of the signal/variable and/or comments on its usage.')),
                ('consumer', models.ManyToManyField(to='kcd.NodeRef')),
                ('label_set_label', models.ManyToManyField(to='kcd.Label')),
                ('label_set_label_groups', models.ManyToManyField(to='kcd.LabelGroup')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kcd.Message')),
                ('muxgroup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kcd.MuxGroup')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('unsigned', 'unsigned'), ('signed', 'signed'), ('single', 'IEEE754 Single'), ('double', 'IEEE754 Double')], default='unsigned', help_text='Datatype of the value e.g. "unsigned","signed" or IEE754 "single", "double".', max_length=8, null=True, validators=[django.core.validators.RegexValidator('(unsigned)|(signed)|(single)|(double)')])),
                ('slope', models.FloatField(default=1, help_text='The slope "m" of a linear equation y = mx + b.')),
                ('intercept', models.FloatField(default=0, help_text='The y-axis intercept "b" of a linear equation y = mx + b.')),
                ('unit', models.TextField(help_text='Physical unit of the value written as unit term as described in "The Unified Code for Units of Measure" (http://unitsofmeasure.org/ucum.html)')),
                ('min', models.FloatField(default=0, help_text='Lower validity limit of the interpreted value after using the slope/intercept equation.')),
                ('max', models.FloatField(default=1, help_text='Upper validity limit of the interpreted value after using the slope/intercept equation.')),
            ],
        ),
        migrations.CreateModel(
            name='Var',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField(blank=True, help_text='Describes the purpose of the signal/variable and/or comments on its usage.')),
                ('name', models.TextField(help_text='Unique name of the variable.')),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kcd.Node')),
                ('value', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='kcd.Value')),
            ],
        ),
        migrations.AddField(
            model_name='signal',
            name='values',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='kcd.Value'),
        ),
        migrations.AddField(
            model_name='multiplex',
            name='consumer',
            field=models.ManyToManyField(to='kcd.NodeRef'),
        ),
        migrations.AddField(
            model_name='multiplex',
            name='label_set_label',
            field=models.ManyToManyField(to='kcd.Label'),
        ),
        migrations.AddField(
            model_name='multiplex',
            name='label_set_label_groups',
            field=models.ManyToManyField(to='kcd.LabelGroup'),
        ),
        migrations.AddField(
            model_name='multiplex',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kcd.Message'),
        ),
        migrations.AddField(
            model_name='multiplex',
            name='value',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='kcd.Value'),
        ),
        migrations.AddField(
            model_name='message',
            name='producer',
            field=models.ManyToManyField(to='kcd.NodeRef'),
        ),
        migrations.AddField(
            model_name='labelgroup',
            name='label_set',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kcd.LabelSet'),
        ),
        migrations.AddField(
            model_name='label',
            name='label_set',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kcd.LabelSet'),
        ),
        migrations.AddField(
            model_name='bus',
            name='network_definition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kcd.NetworkDefinition'),
        ),
    ]
