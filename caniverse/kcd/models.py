from django.db import models

"""The models in this application are designed to be a faithful representation
of the .kcd format from the Kayak tool. These models are based on the schema
definition at
https://github.com/dschanoeh/Kayak/blob/master/Kayak-kcd/src/main/resources/com/github/kayak/canio/kcd/loader/Definition.xsd
"""


class NetworkDefinition(models.Model):
    """Definition of one or more CAN bus networks in one file."""
    pass

class Bus(models.Model):
    """A network transport system that transfers the data between several
    nodes."""
    pass


class Message(models.Model):
    """A datagram that is used to transport payload data along the bus
    network."""
    pass


class Multiplex(models.Model):
    """A looping counter to make a group of signals (MuxGroup) alternately
    active at a time."""
    pass


class MuxGroup(models.Model):
    """A group of signals that is just valid when the count value of the group
    matches with the looping counter (Multiplex)."""
    pass


class LabelSet(models.Model):
    """A set of label and label groups. Each label describes the meaning of a
    single raw value by an alias name. A single value can only belong to a
    one label or label group."""
    pass


class Signal(models.Model):
    """A discrete part of information contained in the payload of a
    message."""
    pass


class Notes(models.Model):
    """Describes the purpose of the signal/variable and/or comments on its
    usage."""
    pass


class Producer(models.Model):
    """Origin network node that is the sender of the assigned message."""
    pass


class Consumer(models.Model):
    """Network node that is a user/receiver of the assigned signal."""
    pass


class Value(models.Model):
    """Details of how the raw value of the signal/variable shall be
    interpreted."""
    TYPES = (('unsigned', 'unsigned'),
             ('signed', 'signed'),
             ('single', 'IEEE754 Single'),
             ('double', 'IEEE754 Double')
            )

    type = models.CharField(help_text='Datatype of the value',
                            choices=TYPES, default='unsigned', null=True)
    slope = models.FloatField(default=1, help_text='The slope "m" of a linear equation y = mx + b.')
    intercept = models.FloatField(default=0, help_text='The y-axis intercept "b" of a linear equation y = mx + b.')
    unit = models.TextField(help_text='Physical unit of the value written as unit term as described in "The Unified'
                                      ' Code for Units of Measure" (http://unitsofmeasure.org/ucum.html)')
    min = models.FloatField(help_text='Lower validity limit of the interpreted value after using the'
                                      ' slope/intercept equation.',
                            default=0)
    max = models.FloatField(help_text='Upper validity limit of the interpreted value after using the slope/intercept'
                                      ' equation.',
                            default=1)
class Label(models.Model):
    """Descriptive name for a single value e.g. to describe an enumeration
    mark special, invalid or error values."""
    pass


class LabelGroup(models.Model):
    """Descriptive name for a sequence of adjacent values."""
    pass


class Node(models.Model):
    """An endpoint connected to the network (e.g. an electronic control unit)
    that is able to send messages to or receive messages from other
    endpoints."""
    pass


class NodeRef(models.Model):
    """An endpoint connected to the network that is able to send messages to
    or receive messages from other endpoints."""
    pass


class Document(models.Model):
    """Describes the scope of application e.g. the target vehicle or
    controlled device."""
    name = models.TextField(help_text='Describes the scope of application e.g. the target vehicle or controlled device.')
    version = models.TextField(help_text='The version of the network definition document.')
    author = models.TextField(help_text='The owner or author of the network definition document.')
    company = models.TextField(help_text='The owner company of the network definition document.')
    date = models.TextField(help_text='The release date of this version of the network definition document.')

    network_definition = models.OneToOneField("NetworkDefinition", on_delete=models.CASCADE, related_name='document')


class Var(models.Model):
    """A variable, a symbolic name associated to a chunk of information (e.g.
    a string or a value)."""
    pass


class BasicLabelType(models.Model):
    pass


class BasicSignalType(models.Model):
    pass
