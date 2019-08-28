# TYPE sshmon_alert gauge
{{#servers}}{{#inspectors}}{{#alarms}}
sshmon_alert{server="{{alphanum ../../name}}",inspector="{{alphanum ../type}}",alarm="{{alphanum name}}"} {{#if fired}}1{{else}}0{{/if}}
{{! new line intentional }}
{{/alarms}}{{/inspectors}}{{/servers}}
# TYPE sshmon_metric gauge
{{#servers}}{{#inspectors}}{{#deepEach metrics}}
sshmon_metric{server="{{alphanum ../../name}}",inspector="{{alphanum ../type}}",name="{{alphanum @key}}"} {{numeric this}}
{{! intentionally blank}}
{{/deepEach}}{{/inspectors}}{{/servers}}
