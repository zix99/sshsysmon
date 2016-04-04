{{!-- Template for writing summary in markdown --}}
# System Summary
{{ctime}}

{{#servers}}
## {{name}}

{{#inspectors}}
### {{name}}
{{text}}

{{/inspectors}}


{{/servers}}