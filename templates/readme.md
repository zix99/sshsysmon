# SshSysMon Templates

Templates control how the SshSysMon summary is output to stdout.
SshSysMon uses handlebars for output templating.  It is passed the data structure in the below format
and will turn it in to the desired document and export to stdout.  If not template is specified,
it will be output in JSON.

The default templtae is `md` (markdown).

## Helpers

### ifEq

Checks equality between a variable and a value.

Example:
```
{{#ifEq type "memory"}}
Output this
{{else}}
Output other thing
{{/ifEq}}
```

### replace
Replaces one string with another string.

Example:
```
{{replace text 'thing' 'other'}}
```

## Data Format
```json
{
  "ctime" : GENERATION_TIME,
  "servers" : [
    {
      "name" : NAME_OF_SERVER,
      "inspectors" : [
        {
          "type" : INSPECTOR_TYPE,
          "name" : INSPECTOR_NAME,
          "config" : INSPECTOR_CONFIG,
          "text" : SUMMARY_TEXT,
          "metrics" : {RAW_METRICS,...}
        },
        ...
      ]
    },
    ...
  ]
}
```

