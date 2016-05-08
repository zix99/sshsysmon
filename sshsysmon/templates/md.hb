{{!-- Template for writing summary in markdown --}}
# {{coalesce meta.title 'System Summary'}}
{{ctime}}

{{#servers}}
## {{name}}

### Alarms
{{#inspectors}}{{#alarms}}
{{{name}}}:	{{fired}}

{{/alarms}}{{/inspectors}}

### Inspectors

{{#inspectors}}
#### {{name}}
{{text}}

{{/inspectors}}

--

{{/servers}}