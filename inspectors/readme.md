# SshSysMon Inspectors

Inspectors are classes that know how to retrieve `metrics` from a given `driver`.  Unlike
their cousins, `inspectors` use the well-known method with two arguments: `def create(driver, args)`.