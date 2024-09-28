# aind-flake8-extensions

Install in your dev dependencies `aind-flake8-extensions`, make sure to pin to a release if you don't want to get random future additions.

Add to your .flake8 file

```
[flake8:local-plugins]
extension =
    PF = aind_flake8_extensions.plugin:run_ast_checks
```
