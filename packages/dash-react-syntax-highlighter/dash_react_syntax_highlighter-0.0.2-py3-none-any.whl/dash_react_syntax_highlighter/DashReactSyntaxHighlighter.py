# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashReactSyntaxHighlighter(Component):
    """A DashReactSyntaxHighlighter component.
DashReactSyntaxHighlighter is a component for syntax highlighting.
It takes properties for the code to highlight, the programming language, the style, and an optional parameter to allow copying the snippet to the clipboard.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- allowCopy (boolean; default True):
    Optional parameter to allow copying the snippet to the clipboard.

- code (string; required):
    The code string to be highlighted.

- language (string; default 'javascript'):
    The programming language of the code.

- styleName (string; default 'okaidia'):
    The name of the style to use for syntax highlighting. Options are:
    'dark', 'coy', 'okaidia', 'twilight', 'solarizedlight'."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_react_syntax_highlighter'
    _type = 'DashReactSyntaxHighlighter'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, code=Component.REQUIRED, language=Component.UNDEFINED, styleName=Component.UNDEFINED, allowCopy=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'allowCopy', 'code', 'language', 'styleName']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'allowCopy', 'code', 'language', 'styleName']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['code']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(DashReactSyntaxHighlighter, self).__init__(**args)
