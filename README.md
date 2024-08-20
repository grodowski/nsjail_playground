## Stacksync eval API

Goals for the execrcise

- `POST /execute` accepts multiline JSON as body and executes a supplied `main` method
- Throw error if `main` is missing
- Throw error if `main` is not a function
- Docker image listening on 8080
- Use `flask` and `nsjail`
- Expose `os`, `pandas` and `numpy`
- Deploy on Google Cloud Run

Building the image

```
# build it
docker build . -f Dockerfile --no-cache -t stacksyncjail

# run it
docker run --rm -it -p8080:8080 stacksyncjail

# or test with
docker run --rm -it -p8080:8080 stacksyncjail bash
$ nsjail --config sandbox.cfg -- /usr/local/bin/python -c "print('hello world')"
```

Example cURL

```
curl -X POST http://localhost:8080/run \
-H "Content-Type: application/json" \
-d '{
  "script": "def main():\n\timport time\n\ttime.sleep(1)\n\tprint(\"Hello from the script\")\n\nif __name__ == \"__main__\":\n\tmain()"
}'
```
