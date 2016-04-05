{{!-- Template for writing summary in markdown --}}
# {{coalesce meta.title 'System Summary'}}
{{ctime}}

{{#servers}}
## {{name}}

{{#inspectors}}
### {{name}}
{{text}}

{{/inspectors}}


{{/servers}}