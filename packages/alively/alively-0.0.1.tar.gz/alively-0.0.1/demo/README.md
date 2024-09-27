# Demo dbt project

Navigate to the demo directory.

```
cd demo
```

Start a postgres database with the config defined in `.env.postgres`.

```
docker run --detach --env-file .env.postgres --publish 127.0.0.1:5432:5432 --name postgres postgres:16-alpine
```

Build the models.

```
live dbt build
```

## Screen recording

Use the `vhs` command to capture a demo.

```
vhs demo.tape
```

To modify the prompt used in the demo, set the PROMPT var.

```
export PROMPT='> '
```
