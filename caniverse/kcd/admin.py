from django.contrib import admin

from .models import NetworkDefinition, Bus, Message, Multiplex, MuxGroup, LabelSet, \
    Value, LabelGroup, Node, NodeRef, Document, Var, Label, Signal


class DocumentAdmin(admin.ModelAdmin):
    pass


class NodeInline(admin.StackedInline):
    model = Node
    classes = ['collapse']
    show_change_link = True


class BusInline(admin.StackedInline):
    model = Bus
    classes = ['collapse']
    show_change_link = True


class NetworkDefinitionAdmin(admin.ModelAdmin):
    inlines = [NodeInline, BusInline]


class MessageInline(admin.StackedInline):
    model = Message
    classes = ['collapse']
    show_change_link = True


class BusAdmin(admin.ModelAdmin):
    inlines = [MessageInline]


class MultiplexInline(admin.StackedInline):
    model = Multiplex
    classes = ['collapse']
    show_change_link = True


class MessageAdmin(admin.ModelAdmin):
    inlines = [MultiplexInline]


class MultiplexAdmin(admin.ModelAdmin):
    pass

class SignalInline(admin.StackedInline):
    model = Signal
    classes = ['collapse']
    show_change_link = True

class MuxGroupAdmin(admin.ModelAdmin):
    inlines = [SignalInline]


class LabelGroupInline(admin.StackedInline):
    model = LabelGroup
    classes = ['collapse']
    show_change_link = True



class LabelInline(admin.StackedInline):
    model = Label
    classes = ['collapse']
    show_change_link = True



class LabelSetAdmin(admin.ModelAdmin):
    inlines=[LabelGroupInline, LabelInline]


class ValueAdmin(admin.ModelAdmin):
    pass


class LabelGroupAdmin(admin.ModelAdmin):
    pass



class VarInline(admin.StackedInline):
    model = Var
    classes = ['collapse']


class NodeAdmin(admin.ModelAdmin):
    inlines = [VarInline]


class NodeRefAdmin(admin.ModelAdmin):
    pass


class VarAdmin(admin.ModelAdmin):
    pass


class LabelAdmin(admin.ModelAdmin):
    pass


class SignalAdmin(admin.ModelAdmin):
    pass


admin.site.register(NetworkDefinition, NetworkDefinitionAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Bus, BusAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Multiplex, MultiplexAdmin)
admin.site.register(MuxGroup, MuxGroupAdmin)
admin.site.register(LabelSet, LabelSetAdmin)
admin.site.register(Value, ValueAdmin)
admin.site.register(LabelGroup, LabelGroupAdmin)
admin.site.register(Node, NodeAdmin)
admin.site.register(NodeRef, NodeRefAdmin)
admin.site.register(Var, VarAdmin)
admin.site.register(Label, LabelAdmin)
admin.site.register(Signal, SignalAdmin)
