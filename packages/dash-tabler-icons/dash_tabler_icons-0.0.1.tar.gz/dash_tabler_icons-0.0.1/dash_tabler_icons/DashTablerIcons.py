# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashTablerIcons(Component):
    """A DashTablerIcons component.
DashTablerIcons is a component that renders the IconAward from @tabler/icons-react.

Keyword arguments:

- color (string; default 'black'):
    The color of the icon (stroke color).

- icon (string; required):
    The name of the icon to render.

- size (number; default 24):
    The size of the icon (width and height).

- stroke (number; default 1):
    The stroke width of the icon.

- strokeLinejoin (string; default 'miter'):
    The stroke line join of the icon."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_tabler_icons'
    _type = 'DashTablerIcons'
    @_explicitize_args
    def __init__(self, size=Component.UNDEFINED, color=Component.UNDEFINED, stroke=Component.UNDEFINED, strokeLinejoin=Component.UNDEFINED, icon=Component.REQUIRED, **kwargs):
        self._prop_names = ['color', 'icon', 'size', 'stroke', 'strokeLinejoin']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['color', 'icon', 'size', 'stroke', 'strokeLinejoin']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['icon']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(DashTablerIcons, self).__init__(**args)
