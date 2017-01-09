"""The models in this application are designed to be a faithful representation
of the .kcd format from the Kayak tool. These models are based on the schema
definition at
"https://github.com/dschanoeh/Kayak/blob/master/Kayak-kcd/src/main/resources/com/github/kayak/
canio/kcd/loader/Definition.xsd"
"""

from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .validators import RangeValidator


class Entry(models.Model):
    """Entry in the system."""
    network = models.OneToOneField('NetworkDefinition')
    user = models.OneToOneField('auth.User')


class NetworkDefinition(models.Model):
    """Definition of one or more CAN bus networks in one file."""

    # nodes - relation defined in Node object.
    # buses - relation defined in Bus object.

    name = models.TextField(blank=True,
                            help_text='Describes the scope of application e.g. the target vehicle '
                                      'or controlled device.')
    version = models.TextField(blank=True,
                               help_text='The version of the network definition document.')
    author = models.TextField(blank=True,
                              help_text='The owner or author of the network definition document.')
    company = models.TextField(blank=True,
                               help_text='The owner company of the network definition document.')
    date = models.TextField(blank=True,
                            help_text='The release date of this version of the network definition'
                                      ' document.')

    def __str__(self):
        if len(self.name) != 0:
            return self.name
        else:
            return 'Network Definition {}'.format(self.id)


class Bus(models.Model):
    """A network transport system that transfers the data between several
    nodes."""
    # messages - relation defined in Message object.
    name = models.TextField(blank=False,
                            help_text='Human-readable name of the bus network (e.g. "Comfort").')
    baudrate = models.IntegerField(default=500000,
                                   validators=[RangeValidator(5000, 1000000,
                                                              message=_('Baud rate must be between '
                                                                        '%(lower)s and %(upper)s. ('
                                                                        'it is %(value)s).'),
                                                              code='baud_rate')],
                                   help_text='Nominal data transfer rate in baud (e.g. 500000, '
                                             '125000, 100000 or 83333).')
    network_definition = models.ForeignKey('NetworkDefinition', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Buses'


class Message(models.Model):
    """A datagram that is used to transport payload data along the bus
    network."""
    FRAME_FORMATS = [('standard', 'standard'), ('extenteded', 'exteneded')]
    notes = models.TextField(blank=True,
                             help_text='Describes the purpose of the signal/variable and/or '
                                       'comments on its usage.')
    # multiplex - relation defined in Multiplex field
    # signal - relation defined in Signal field
    producer = models.ManyToManyField('Node')
    message_id = models.TextField(validators=[RegexValidator(regex=r'0x[A-F0-9]+')],
                                  help_text='The unique identifier of the message. May have 11-bit '
                                            '(Standard frame format) or 29-bit (Extended frame '
                                            'format). The identifier is usually written in '
                                            'hexadecimal format e.g. 0x123. If format is "extended"'
                                            ' this identifier includes both Base ID (11 bits) and'
                                            ' Extended ID (18 bits).')
    bus = models.ForeignKey('Bus', on_delete=models.CASCADE)
    name = models.TextField(blank=False,
                            help_text='Human-readable name of the network message'
                                      ' (e.g."OBD-Info").')
    length = models.CharField(max_length=4,
                              validators=[RegexValidator(regex='r([0-8])|(auto)')],
                              help_text='Number of bytes available in the data field of the message'
                                        ' (data length code). "auto" (default) calculate minimum '
                                        'length for the contained signals in the message.')
    interval = models.PositiveIntegerField(default=0,
                                           validators=[RangeValidator(0, 60000,
                                                                      code='interval')],
                                           help_text='Repetition interval of a cyclic network '
                                                     'message in milliseconds.')
    triggered = models.BooleanField(default=False,
                                    help_text='Sending behavior of the network message. True, if '
                                              'message is triggered by signal changes.')
    count = models.PositiveIntegerField(default=0,
                                        help_text='Number of repetitions of a triggered network '
                                                  'message. 0 (default) for infinitee repetitions.')
    format = models.CharField(max_length=8, default='standard',
                              validators=[RegexValidator(regex=r'(standard)|(extended)')],
                              help_text='Frame format of the network message.',
                              choices=FRAME_FORMATS)
    remote = models.BooleanField(default=False,
                                 help_text='True, if message is a remote frame.')

    def __str__(self):
        return "{}({})".format(self.name, self.message_id)


class MuxGroup(models.Model):
    """A group of signals that is just valid when the count value of the group
    matches with the looping counter (Multiplex)."""
    multiplex = models.ForeignKey("Multiplex", on_delete=models.CASCADE)

    # signal - relation defined in Signal
    count = models.PositiveIntegerField(validators=[MinValueValidator(0)],
                                        help_text='Count value of the Multiplex when the signals of'
                                                  ' this group become valid.')


class LabelSet(models.Model):
    """A set of label and label groups. Each label describes the meaning of a
    single raw value by an alias name. A single value can only belong to a
    one label or label group."""
    # label = Relation defined in Label
    # label_group = Relation defined in LabelGroup
    pass


class Value(models.Model):
    """Details of how the raw value of the signal/variable shall be
    interpreted."""
    TYPES = (
        ('unsigned', 'unsigned'),
        ('signed', 'signed'),
        ('single', 'IEEE754 Single'),
        ('double', 'IEEE754 Double'))

    type = models.CharField(max_length=8,
                            choices=TYPES, default='unsigned', null=True,
                            help_text='Datatype of the value e.g. "unsigned","signed" or IEE754 '
                                      '"single", "double".',
                            validators=[RegexValidator(r'(unsigned)|(signed)|(single)|(double)')])
    slope = models.FloatField(default=1, help_text='The slope "m" of a linear equation y = mx + b.')
    intercept = models.FloatField(default=0,
                                  help_text='The y-axis intercept "b" of a linear equation y = mx +'
                                            ' b.')
    unit = models.TextField(help_text='Physical unit of the value written as unit term as described'
                                      ' in "The Unified Code for Units of Measure" (http://unitsofm'
                                      'easure.org/ucum.html)')
    min = models.FloatField(help_text='Lower validity limit of the interpreted value after using th'
                                      'e slope/intercept equation.',
                            default=0)
    max = models.FloatField(help_text='Upper validity limit of the interpreted value after using th'
                                      'e slope/intercept equation.',
                            default=1)
    # signal = models.OneToOneField('Signal', on_delete=models.CASCADE)
    # multiplex = models.OneToOneField('Multiplex', on_delete=models.CASCADE)


class Node(models.Model):
    """An endpoint connected to the network (e.g. an electronic control unit)
    that is able to send messages to or receive messages from other
    endpoints."""
    # var -- defined via Var instances.
    network = models.ForeignKey('NetworkDefinition', on_delete=models.CASCADE)
    node_id = models.TextField(blank=False,
                               help_text='Unique identifier of the network node.')
    name = models.TextField(null=True, blank=True, unique=True,
                            help_text='Human-readable name of the network node (e.g. "Brake").')


class Var(models.Model):
    """A variable, a symbolic name associated to a chunk of information (e.g.
    a string or a value)."""
    node = models.ForeignKey('Node', on_delete=models.CASCADE)
    notes = models.TextField(blank=True,
                             help_text='Describes the purpose of the signal/variable and/or '
                                       'comments on its usage.')
    value = models.OneToOneField('Value', null=True, on_delete=models.SET_NULL)
    name = models.TextField(help_text='Unique name of the variable.')

    def __str__(self):
        return self.name


class BasicLabelType(models.Model):
    LABEL_TYPES = (('value', 'value'),
                   ('invalid', 'invalid'),
                   ('error', 'error'))
    name = models.TextField(null=False,
                            help_text='Human-readable name for this value.')
    label_type = models.CharField(max_length=7, default='value',
                                  choices=LABEL_TYPES,
                                  help_text='Type of value: "value", "invalid" or "error".')

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class BasicSignalType(models.Model):
    ENDIANESS = (('little', 'little'),
                 ('big', 'big'))
    endianess = models.CharField(max_length=6,
                                 choices=ENDIANESS,
                                 default='little',
                                 help_text='Determines if Byteorder is big-endian (Motorola), '
                                           'little-endian (Intel) otherwise.')

    length = models.IntegerField(default=1,
                                 validators=[RangeValidator(1, 64)],
                                 help_text='Bit length of the signal.')
    name = models.TextField(blank=False,
                            help_text='Human readable name of the signal.')
    offset = models.IntegerField(blank=False,
                                 validators=[RangeValidator(0, 63)],
                                 help_text='Least significant bit offset of the signal relative to '
                                           'the least significant bit of the messages data payload'
                                           '.')

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Label(BasicLabelType):
    """Descriptive name for a single value e.g. to describe an enumeration
    mark special, invalid or error values."""
    value = models.IntegerField(
        validators=[MinValueValidator(0, message=_('Must be non-negative, was %(value)s'))],
        help_text='Signal raw value that is described here.'
    )
    label_set = models.ForeignKey('LabelSet', on_delete=models.CASCADE)


class Signal(BasicSignalType):
    """A discrete part of information contained in the payload of a
    message."""
    notes = models.TextField(blank=True,
                             help_text='Describes the purpose of the signal/variable and/or '
                                       'comments on its usage.')
    consumer = models.ManyToManyField('Node')
    values = models.OneToOneField('Value', null=True, on_delete=models.SET_NULL)
    label_set_label = models.ManyToManyField('Label')
    label_set_label_groups = models.ManyToManyField('LabelGroup')
    message = models.ForeignKey('Message', on_delete=models.CASCADE)
    muxgroup = models.ForeignKey('MuxGroup', on_delete=models.CASCADE)


class Multiplex(BasicSignalType):
    """A looping counter to make a group of signals (MuxGroup) alternately
    active at a time."""
    # muxgroup - Defined in MuxGroup
    # value - Defined in Value
    notes = models.TextField(blank=True,
                             help_text='Describes the purpose of the signal/variable and/or '
                                       'comments on its usage.')
    consumer = models.ManyToManyField('Node')
    value = models.OneToOneField('Value', null=True, on_delete=models.SET_NULL)
    label_set_label = models.ManyToManyField('Label')
    label_set_label_groups = models.ManyToManyField('LabelGroup')
    message = models.ForeignKey('Message', on_delete=models.CASCADE)


class LabelGroup(BasicLabelType):
    """Descriptive name for a sequence of adjacent values."""
    label_set = models.ForeignKey("LabelSet", on_delete=models.CASCADE)
    raw_from = models.PositiveIntegerField(help_text='Signal raw value the label group is starting '
                                                     'with.')
    raw_to = models.PositiveIntegerField(help_text='Signal raw value the label group is ending '
                                                   'with.')
