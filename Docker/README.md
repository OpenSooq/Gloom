# Build it
```
docker build -f Dockerfile -t opensooq/gloom .
```

# Run it
```
docker run --env-file env.file -p3000:3000 -d opensooq/gloom
```