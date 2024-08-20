## Stacksync eval API

Goals for the execrcise

✅ `POST /execute` accepts multiline JSON as body and executes a supplied `main` method
✅ Throw error if `main` is missing
✅ Throw error if `main` is not a function
✅ Docker image listening on 8080
✅ Use `flask` and `nsjail`
✅ Expose `os`, `pandas` and `numpy`
❌ Deploy on Google Cloud Run

Building and testing the image

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
curl -X POST http://localhost:8080/execute \
-H "Content-Type: application/json" \
-d '{
  "script": "def main():\n\tprint(f\"Hello from the script with a random 2x3 array {numpy.random.randint(1, 100, size=(2, 3))}\")"
}'
```

Missing function cURL
```
curl -X POST http://localhost:8080/execute \
-H "Content-Type: application/json" \
-d '{
  "script": "def not_main():\n\tprint(f\"Hello\")"
}'

{"error":"main function not found in the script"}
```

Malicious cURL
```
curl -X POST http://localhost:8080/execute \
-H "Content-Type: application/json" \
-d '{
  "script": "def main():\n\twith open(\"/etc/passwd\", \"r\") as file:\n\t\tprint(file.read())"
}'

[Errno 2] No such file or directory: '/etc/passwd'
```