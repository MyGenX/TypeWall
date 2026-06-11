# Validation CLI

The CLI loads a trusted Python schema target and validates JSON from a file or standard input.

```shell
typewall validate examples.cli.schema:User examples/cli/user.json
cat examples/cli/user.json | typewall validate --json examples.cli.schema:User -
```

Exit code `0` means success, `1` means validation failure, and `2` means invocation, target-loading, I/O, or JSON input failure. Import targets execute Python code and must be trusted.
