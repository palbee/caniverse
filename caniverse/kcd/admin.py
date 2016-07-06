from django.contrib import admin

from .models import NetworkDefinition, Bus, Message, Multiplex, MuxGroup, LabelSet, Notes, Producer, Consumer, Value, \
    LabelGroup, Node, NodeRef, Document, Var, Label, Signal


# Register your models here.


class DocumentAdmin(admin.ModelAdmin):
    pass


class NetworkDefinitionAdmin(admin.ModelAdmin):
    pass


class BusAdmin(admin.ModelAdmin):
    pass


class MessageAdmin(admin.ModelAdmin):
    pass


class MultiplexAdmin(admin.ModelAdmin):
    pass


class MuxGroupAdmin(admin.ModelAdmin):
    pass


class LabelSetAdmin(admin.ModelAdmin):
    pass


class NotesAdmin(admin.ModelAdmin):
    pass


class ProducerAdmin(admin.ModelAdmin):
    pass


class ConsumerAdmin(admin.ModelAdmin):
    pass


class ValueAdmin(admin.ModelAdmin):
    pass


class LabelGroupAdmin(admin.ModelAdmin):
    pass


class NodeAdmin(admin.ModelAdmin):
    pass


class NodeRefAdmin(admin.ModelAdmin):
    pass


class VarAdmin(admin.ModelAdmin):
    pass


class LabelAdmin(admin.ModelAdmin):
    pass


class SignalAdmin(admin.ModelAdmin):
    pass


admin.site.register(NetworkDefinition, NetworkDefinitionAdmin)
admin.site.register(Bus, BusAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Multiplex, MultiplexAdmin)
admin.site.register(MuxGroup, MuxGroupAdmin)
admin.site.register(LabelSet, LabelSetAdmin)
admin.site.register(Notes, NotesAdmin)
admin.site.register(Producer, ProducerAdmin)
admin.site.register(Consumer, ConsumerAdmin)
admin.site.register(Value, ValueAdmin)
admin.site.register(LabelGroup, LabelGroupAdmin)
admin.site.register(Node, NodeAdmin)
admin.site.register(NodeRef, NodeRefAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Var, VarAdmin)
admin.site.register(Label, LabelAdmin)
admin.site.register(Signal, SignalAdmin)
