from django.contrib import admin

from .models import NetworkDefinition, Bus, Message, Multiplex, MuxGroup, LabelSet, \
    Value, LabelGroup, Node, Var, Label, Signal


class NodeInline(admin.StackedInline):
    model = Node
    classes = ['collapse']
    show_change_link = True
    fields = ('name', 'node_id')


class BusInline(admin.StackedInline):
    model = Bus
    classes = ['collapse']
    show_change_link = True


class NetworkDefinitionAdmin(admin.ModelAdmin):
    inlines = [NodeInline, BusInline]
    fieldsets = (
        ('Document',
         {
             'fields': ('name', 'version', 'author', 'company'),
             'classes': ('collapse',),
             'description': 'Network Metadata'
         }),
    )


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


class ValueInline(admin.StackedInline):
    model = Value
    classes = ['collapse']
    show_change_link = True
    fields = ('type', 'slope', 'intercept', 'unit', 'min', 'max')


class MessageAdmin(admin.ModelAdmin):
    inlines = [MultiplexInline]


class MultiplexAdmin(admin.ModelAdmin):
    inlines = [ValueInline]


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
    inlines = [LabelGroupInline, LabelInline]


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
    inlines = [ValueInline]


admin.site.register(NetworkDefinition, NetworkDefinitionAdmin)
admin.site.register(Bus, BusAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Multiplex, MultiplexAdmin)
admin.site.register(MuxGroup, MuxGroupAdmin)
admin.site.register(LabelSet, LabelSetAdmin)
admin.site.register(Value, ValueAdmin)
admin.site.register(LabelGroup, LabelGroupAdmin)
admin.site.register(Node, NodeAdmin)
admin.site.register(Var, VarAdmin)
admin.site.register(Label, LabelAdmin)
admin.site.register(Signal, SignalAdmin)
