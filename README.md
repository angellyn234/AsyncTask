# AsyncTask — Parallel Task Runner with Real-Time Feedback UI

https://github.com/angellyn234/AsyncTask/releases

[![Release](https://img.shields.io/github/v/release/angellyn234/AsyncTask?color=brightgreen&label=Releases)](https://github.com/angellyn234/AsyncTask/releases)

![AsyncTask banner](https://images.unsplash.com/photo-1518773553398-650c184e0bb3?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=60)

Table of contents
- About
- Features
- Key concepts
- Architecture
- Quickstart — download and run
- Install from source
- CLI usage
- API examples (Python, Node, Go)
- Real-time feedback and UI
- Configuration file
- Patterns and best practices
- Performance and benchmarks
- Security and sandboxing
- Testing and CI
- Troubleshooting and FAQ
- Contributing
- License

About
- AsyncTask is a concurrency framework. It runs many tasks in parallel. It ships a CLI, a library API, and a web UI for live progress.
- You can use it to run CPU-bound jobs, I/O-bound jobs, and mixed workloads.
- It exposes progress metrics and per-task feedback in real time.

Features
- Worker pool with dynamic scaling.
- Task scheduler with priorities and retry policies.
- Real-time feedback via websockets and HTTP SSE.
- Pluggable executors for local, container, and remote execution.
- Built-in task tracing, logs, and metrics.
- CLI tooling for batch runs and test harnesses.
- Lightweight UI for live monitoring and control.
- Simple API for embedding in apps.

Key concepts
- Task: A unit of work. A task has an ID, a payload, and an execution spec.
- Worker: A process or thread that executes tasks.
- Executor: The mechanism that runs a task. Examples: local process, Docker container, remote worker.
- Scheduler: The component that assigns tasks to workers.
- Feedback channel: A live stream from the running task. It may carry logs, progress, and events.
- Retry policy: Rules that determine how and when to retry failed tasks.
- Backoff: A delay pattern used on retries.
- Priority: A numeric value that affects scheduling order.
- Cancellation: A mechanism to stop running tasks on demand.

Architecture
AsyncTask uses a modular architecture. Each module holds a single responsibility.

Core modules
- core/scheduler: task queue, priority handling, backpressure
- core/executor: executor interface and implementations
- core/worker: worker lifecycle, health checks
- core/feedback: websocket and SSE handlers
- core/storage: metadata store and state persistence
- ui: web client, graphs, live console
- cli: shell command entry points
- api: language bindings and HTTP endpoints

Data flow
1. Client submits a task via CLI, API, or UI.
2. Scheduler enqueues the task and picks an executor based on the task spec.
3. Worker claims the task and runs the executor.
4. Executor streams logs and progress to the feedback channel.
5. Storage records task state, timestamps, and logs.
6. UI subscribes to feedback channels and shows updates.

Design goals
- Predictable throughput under varied load.
- Low latency for small tasks.
- Live feedback without polling.
- Minimal API surface for quick adoption.
- Safe defaults for retries and resource limits.

Quickstart — download and run
The releases page contains build artifacts. Download the release asset for your platform and execute it.

- Visit the Releases page to find the binary or archive for your OS:
  https://github.com/angellyn234/AsyncTask/releases

- Example download and run commands.

  Linux example (bash):
  ```bash
  # replace <asset> with the actual filename from the Releases page
  curl -L -o AsyncTask.tar.gz "https://github.com/angellyn234/AsyncTask/releases/download/vX.Y.Z/AsyncTask-linux-amd64.tar.gz"
  tar -xzf AsyncTask.tar.gz
  chmod +x async-task
  ./async-task server --config config.yml
  ```

  macOS (intel / apple silicon):
  ```bash
  curl -L -o async-task-macos.zip "https://github.com/angellyn234/AsyncTask/releases/download/vX.Y.Z/AsyncTask-darwin-amd64.zip"
  unzip async-task-macos.zip
  chmod +x async-task
  ./async-task server
  ```

  Windows (PowerShell):
  ```powershell
  Invoke-WebRequest -Uri "https://github.com/angellyn234/AsyncTask/releases/download/vX.Y.Z/AsyncTask-windows-amd64.zip" -OutFile "async-task-windows.zip"
  Expand-Archive .\async-task-windows.zip -DestinationPath .\async-task
  cd .\async-task
  .\async-task.exe server --config config.yml
  ```

- Run quick local demo:
  ```bash
  ./async-task run \
    --name "demo:parallel-sleep" \
    --concurrency 4 \
    --script ./examples/sleep-job.sh \
    --payload '{"sleep": 3}' \
    --feedback websocket://localhost:8080/feedback
  ```

Install from source
- Clone the repo
  ```bash
  git clone https://github.com/angellyn234/AsyncTask.git
  cd AsyncTask
  ```

- Build with Go (project core implemented in Go)
  ```bash
  cd cmd/async-task
  go build -o async-task
  ```

- Or build with Cargo for the Rust executor bindings
  ```bash
  cd bindings/rust
  cargo build --release
  ```

- Or install the Python client
  ```bash
  cd bindings/python
  pip install .
  ```

- Or install the Node client
  ```bash
  cd bindings/node
  npm install
  ```

- Common targets with Makefile
  ```bash
  make build
  make test
  make lint
  ```

CLI usage
- Start server:
  ```
  async-task server --config ./config.yml
  ```

- Submit tasks:
  ```
  async-task submit --name compress-images --image=worker:latest --payload ./jobs/images.json
  ```

- Monitor tasks:
  ```
  async-task list --state running
  async-task logs --task-id 12345 --tail
  ```

- Control:
  ```
  async-task cancel --task-id 12345
  async-task retry --task-id 12345
  async-task scale --workers 8
  ```

- Export metrics:
  ```
  async-task metrics --format prometheus > metrics.prom
  ```

API examples

Python example
- Install:
  ```bash
  pip install async-task-client
  ```

- Submit a batch of tasks and watch progress:
  ```python
  from asynctask import Client

  client = Client("http://localhost:8080")

  def on_progress(task_id, state, data):
      print(f"[{task_id}] {state}: {data}")

  client.subscribe_feedback(on_progress)

  tasks = [
      {"name": "resize", "payload": {"file": "img1.jpg", "w": 800}},
      {"name": "resize", "payload": {"file": "img2.jpg", "w": 800}},
      {"name": "resize", "payload": {"file": "img3.jpg", "w": 800}},
  ]

  results = client.submit_batch(tasks, concurrency=4, retry=2)
  for r in results:
      print("done:", r.id, r.status)
  ```

Node example
- Install:
  ```bash
  npm install @asynctask/client
  ```

- Submit and stream logs:
  ```js
  const { Client } = require('@asynctask/client');

  const client = new Client('http://localhost:8080');

  client.on('progress', (taskId, state, data) => {
    console.log(`[${taskId}] ${state}:`, data);
  });

  const task = await client.submit({
    name: 'transcode',
    payload: { src: 'video.mkv', fmt: 'mp4' },
    retry: 1,
  });

  console.log('task queued', task.id);
  ```

Go example
- Import:
  ```go
  import "github.com/angellyn234/AsyncTask/pkg/client"
  ```

- Submit tasks:
  ```go
  func main() {
    c := client.New("http://localhost:8080")
    ch := make(chan client.Event)
    go c.Subscribe(ch)
    go func() {
      for ev := range ch {
        fmt.Printf("task %s: %s\n", ev.TaskID, ev.Type)
      }
    }()

    t := client.Task{
      Name: "fetch",
      Payload: map[string]interface{}{"url":"https://example.com"},
    }
    res, err := c.Submit(t)
    if err != nil {
      log.Fatal(err)
    }
    fmt.Println("submitted", res.ID)
  }
  ```

Real-time feedback and UI
- AsyncTask ships a small web UI at /ui. The UI connects to a websocket endpoint for live updates.
- Feedback channels:
  - WebSocket: ws://host:port/feedback?token=...
  - SSE: http://host:port/feedback/sse?task=123
  - HTTP callback: an HTTP POST to a user-provided endpoint
- Feedback payload
  - event: one of progress, log, heartbeat, done, error
  - task_id: string
  - seq: integer
  - body: arbitrary JSON
- Example websocket message
  ```json
  {
    "event":"progress",
    "task_id":"abc123",
    "seq":42,
    "body":{"percent":65,"message":"compressing"}
  }
  ```
- UI features
  - Live task tree and filters.
  - Per-task log stream with timestamps.
  - Timeline view of events and state changes.
  - Manual control actions: pause, resume, cancel, retry.
  - Charts for throughput and latency.
  - Search and saved views.

Configuration file
- Use YAML or JSON. Sample YAML:
  ```yaml
  server:
    host: 0.0.0.0
    port: 8080
    metrics: /metrics
  storage:
    type: sqlite
    path: ./data/async.db
  scheduler:
    max_workers: 32
    min_workers: 2
    idle_shutdown_seconds: 60
  executor:
    local:
      max_concurrent_tasks: 4
      cpu_limit: 0.75
    docker:
      image_pull_timeout: 30
  feedback:
    websocket:
      ping_interval: 15
    sse:
      buffer_size: 1024
  security:
    api_tokens:
      - token: "changeme"
        role: admin
  logging:
    level: info
    format: json
  ```
- Important fields
  - max_workers: caps the worker pool size.
  - idle_shutdown_seconds: how long a worker idles before shutting down.
  - max_concurrent_tasks: per-executor concurrency limit.
  - feedback.websocket.ping_interval: heartbeat interval for websockets.

Patterns and best practices
- Use short tasks for low latency. Batch when tasks are tiny to reduce overhead.
- Use idempotent tasks. Retry logic assumes idempotence or compensating actions.
- Prefer streaming logs for long tasks. Keep the log buffer small.
- Tune worker counts based on CPU and I/O profile. Measure first.
- Use priorities for mixed workloads. Reserve slots for high-priority tasks.
- Use cancellation for user-initiated stops. Clean up external resources.
- Monitor metrics and set alerts on queue length and worker error rate.

Task spec example
- Minimal JSON spec:
  ```json
  {
    "name": "thumbnail",
    "executor": "local",
    "payload": {"src": "s3://bucket/01.jpg"},
    "resources": {"cpu": 0.5, "memory_mb": 256},
    "retry": {"count": 3, "backoff": "exponential"},
    "priority": 50,
    "callback": {"type": "http", "url": "https://ci.example.com/hook"}
  }
  ```

Advanced features
- Batching: group small tasks into a single executor run to reduce overhead.
- Sharding: split large sets of work across workers with consistent hashing.
- Circuit breaker: pause retries for a task type when error rate spikes.
- Dynamic scaling: autoscale workers based on queue depth and CPU.
- Canary runs: run a fraction of tasks with a new executor image for validation.
- Resource isolation: run executors in containers with limits.
- Pluggable stores: swap sqlite for postgres for production.

Performance and benchmarks
- Benchmark method
  - Use a synthetic workload generator in examples/bench.
  - Measure throughput (tasks/sec), latency (ms to first progress), and error rate.
- Sample numbers on a 4-core VM
  - 1s sleep tasks: 2000 tasks/sec with batching 100
  - 100ms CPU tasks: 450 tasks/sec without batching
  - Mixed I/O task with network: throughput depends on network concurrency
- Tips for tuning
  - Increase max_workers until CPU saturates.
  - Use async I/O executors for many concurrent network calls.
  - Batch small tasks into one process to cut scheduling overhead.
  - Turn on compression for websocket feedback when payloads are large.

Security and sandboxing
- API tokens: use per-service tokens with scoped permissions.
- Executor isolation: run untrusted code in containers or sandboxes.
- Resource caps: set CPU and memory limits per task.
- Secrets: inject secrets at runtime via secure vault backends. Do not store secrets in task payloads.
- Transport security: run server behind TLS and use secure websocket connections.
- Audit logs: capture task submission, modifications, and control actions.

Testing and CI
- Unit tests for scheduler, state machine, and retry logic.
- Integration tests for executors and feedback channels.
- Example CI workflow (GitHub Actions)
  - Run unit tests.
  - Build docker image for executor.
  - Run integration tests in ephemeral environment.
  - Publish release artifacts on tag events.
- Test harness
  - Use the included harness at tools/harness to simulate workers and faults.
  - Use chaos jobs to validate retry and backoff logic.

Troubleshooting and FAQ
- The server will not start on port 8080
  - Check if another process binds the port.
  - Use --port to change the port.
- Tasks stall in queued state
  - Check worker health and max_workers.
  - Inspect logs for executor errors.
- Feedback does not reach UI
  - Confirm websocket endpoint and token.
  - Check reverse proxy for websocket passthrough.
- Tasks fail with resource errors
  - Increase cpu or memory in task spec.
  - Use container-based executor for strict limits.
- Where are releases?
  - Visit the Releases page to download the binaries and archives:
    https://github.com/angellyn234/AsyncTask/releases
  - Download the appropriate asset for your OS and run the binary.

Releases and upgrade path
- Releases include:
  - Linux, macOS, Windows binaries
  - Docker images for executors and the UI
  - Source tarball and checksums
- Upgrade steps
  1. Backup storage and config.
  2. Drain new tasks: set scheduler to drain mode.
  3. Stop server instances.
  4. Replace binary with new release.
  5. Start server and verify health.
  6. Resume normal scheduling.
- Release artifacts must be downloaded and executed for local installs. Find assets on:
  https://github.com/angellyn234/AsyncTask/releases

Integrations
- Prometheus metrics exporter exposes:
  - async_tasks_submitted_total
  - async_tasks_completed_total
  - async_tasks_failed_total
  - async_queue_depth
  - async_worker_count
- Tracing
  - OpenTelemetry spans for task lifecycle.
  - Configure OTLP exporter in config.yml.
- Logging
  - JSON logs by default. Send logs to ELK or a centralized store.
- Hooks
  - HTTP callback on task done.
  - Kafka or NATS publisher for events.
  - Custom plugin interface for exotic sinks.

Extending AsyncTask
- Custom executor
  - Implement the Executor interface in core/executor.
  - Build a binary that can be registered via config.
  - Use the provided executor-sdk to simplify integration.
- Plugins
  - Feedback plugins for custom transports.
  - Storage plugin for alternate persistence layers.
- Language bindings
  - Add bindings in bindings/ for new languages following existing patterns.

Examples
- Built-in examples live in the examples/ folder.
- Example tasks:
  - image-resize: reads input from S3 and writes thumbnails.
  - video-transcode: uses container executor and ffmpeg.
  - http-crawl: a set of I/O-heavy tasks that exercise the async executors.
- Example pipelines
  - Fan-out/fan-in pattern: submit many fetch tasks and reduce results.
  - Map-reduce style: shard, map operations in parallel, then run a reduce task.

Contribution guide
- Run tests and linters before opening a PR:
  ```bash
  make test
  make lint
  ```
- Create a feature branch:
  ```
  git checkout -b feature/my-feature
  ```
- Keep PRs small. Add unit tests for new logic.
- Follow code style and formatting:
  - gofmt / goimports for Go code
  - black and flake8 for Python
  - eslint for Node
- Label PRs:
  - bug, enhancement, docs, refactor
- Maintainers will review and merge after CI passes.

Issue reporting
- Provide a minimal reproduction.
- Include logs, config.yml, and steps to reproduce.
- Provide the output of:
  ```
  async-task version
  async-task status --verbose
  ```

Roadmap
- v1.x
  - Stable scheduler and core executors.
  - Built-in web UI for monitoring.
  - Basic scaling and resource limits.
- v2.x
  - Advanced autoscaling and cluster mode.
  - Role-based access control.
  - Multi-tenant support.
- v3.x
  - Enterprise features: audit, SSO, quota management.
  - Cross-region federated scheduling.

License
- AsyncTask uses the MIT License. See LICENSE.md for the full text.

Acknowledgements
- The design borrows ideas from classic worker pools and modern streaming systems.
- Thank you to the contributors who built the CLI, UI, and executor integrations.

Contact
- Open issues and PRs on GitHub.
- Release assets and binaries:
  https://github.com/angellyn234/AsyncTask/releases

Appendix: Common commands cheat sheet
- Start server
  ```
  async-task server --config config.yml
  ```
- Submit a task from JSON
  ```
  async-task submit --file task.json
  ```
- List tasks
  ```
  async-task list --limit 100 --state running
  ```
- Show logs
  ```
  async-task logs --task-id <id> --follow
  ```
- Cancel a task
  ```
  async-task cancel --task-id <id>
  ```
- Retry a failed task
  ```
  async-task retry --task-id <id>
  ```

Appendix: Example system diagram
![System diagram](https://images.unsplash.com/photo-1498050108023-c5249f4df085?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=60)

- Client submits tasks.
- Scheduler enqueues and assigns tasks.
- Workers execute tasks using executors.
- Executors stream feedback to the feedback service.
- UI subscribes and shows live updates.

Binary releases
- Download the executable file for your OS from the Releases page and run it. The release asset contains the binary and any required runtime files. Visit:
  https://github.com/angellyn234/AsyncTask/releases

Security checklist for production
- Use TLS for HTTP and websockets.
- Rotate API tokens regularly.
- Run executors in isolated environments.
- Set resource limits per task.
- Monitor queue depth and failures.

FAQ (short)
- How do I scale?
  - Increase max_workers. Use autoscaler with queue depth metrics.
- How do I debug a task?
  - Stream logs via CLI or UI. Use the harness to reproduce.
- Can I run untrusted code?
  - Use container or sandbox executors. Limit resources and run as a non-root user.

Changelog
- Check the Releases page for full changelog and artifacts:
  https://github.com/angellyn234/AsyncTask/releases

Keep this README with the repo. Update it when you change config, API, or release formats.