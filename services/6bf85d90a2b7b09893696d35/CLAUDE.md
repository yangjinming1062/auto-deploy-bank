# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LTS (Light Task Scheduler) is a Java-based distributed task scheduling framework that solves distributed job scheduling problems. It supports real-time tasks, scheduled tasks, and cron tasks, with excellent scalability, extensibility, and stability.

## Build Commands

### Maven Commands
- **Compile the project**: `mvn clean compile`
- **Run tests**: `mvn test`
- **Run a single test**: `mvn test -Dtest=TestClassName`
- **Run a specific test method**: `mvn test -Dtest=TestClassName#testMethod`
- **Build all modules**: `mvn clean install -U -DskipTests`
- **Build and skip tests**: `mvn clean install -DskipTests`
- **Package distribution**: `./build.sh` (Linux) or `build.cmd` (Windows)

The build.sh script performs:
1. Builds all modules with `mvn clean install -U -DskipTests`
2. Packages JobTracker and LTS-Admin into `dist/lts-1.7.2-SNAPSHOT-bin.zip`
3. Creates directory structure with startup scripts and configuration

## Module Architecture

LTS follows a distributed architecture with four main node types:

### 1. **JobClient** (`lts-jobclient/`)
- Submits tasks to the system
- Receives execution feedback
- Stateless - can deploy multiple instances for load balancing
- Key class: `RetryJobClient`

### 2. **JobTracker** (`lts-jobtracker/`)
- Receives and dispatches tasks
- Handles task scheduling
- Performs master election
- Stores task queue and execution logs (Mongo or MySQL)
- Listens on configurable port (default 35001)

### 3. **TaskTracker** (`lts-tasktracker/`)
- Executes tasks
- Reports execution results back to JobTracker
- Stateless - can scale horizontally
- Key class: `TaskTracker`

### 4. **LTS-Admin** (`lts-admin/`)
- Web-based management console
- Node management, task queue management, monitoring
- WAR deployment using embedded Jetty

### Supporting Modules

- **lts-core**: Core framework functionality (distributed across other modules)
- **lts-spring**: Spring integration (XML and annotations, NOT in core)
- **lts-monitor**: Monitoring and metrics collection
- **lts-startup**: Startup scripts and distribution packaging

## Key Architectural Concepts

### Master Election
- Each NodeGroup (cluster) elects one master node dynamically
- When master fails, a new master is elected immediately
- API listeners available for master change events

### FailStore (Fault Tolerance)
- Stores failed remote interactions locally when communication fails
- Retries when connection restores
- Implementations: leveldb, rocksdb, berkeleydb, mapdb, ltsdb
- Used for: JobClient submissions, TaskTracker feedback, business logs

### Registry Center
- Supports Zookeeper and Redis
- Handles node discovery and service registry
- Master election coordination

### Storage Options
- **Task Queue**: MongoDB or MySQL (configurable via SPI)
- **Execution Logs**: Stored alongside task queue
- **Business Logs**: Can be console, MySQL, MongoDB (extensible via SPI)

### Communication
- Netty 4.0.20.Final or Apache MINA 2.0.9
- Multiple serialization options: FastJSON, Hessian2, Java

## Task Types

1. **Real-time tasks**: Execute immediately after submission
2. **Scheduled tasks**: Execute at a specific time (one-time)
3. **Cron tasks**: Execute based on cron expressions

## Task Execution Results

- `EXECUTE_SUCCESS`: Execution succeeded, client notified if configured
- `EXECUTE_FAILED`: Execution failed, no retry
- `EXECUTE_LATER`: Retry needed (1min, 2min, 3min strategy), client not notified
- `EXECUTE_EXCEPTION`: Exception occurred, will retry (same strategy as EXECUTE_LATER)

Default max retry: 10 times (configurable)

## Configuration Parameters

### Required Parameters
- `registryAddress`: Zookeeper or Redis address (e.g., `zookeeper://127.0.0.1:2181`)
- `clusterName`: Cluster identifier - only nodes with same name form the cluster
- `listenPort`: JobTracker listening port (default 35001)

### JobTracker Configuration
- `job.logger`: Business log handler (console, mysql, mongo)
- `job.queue`: Task queue implementation (mongo, mysql)
- `jdbc.url/username/password`: MySQL connection details (when job.queue=mysql)
- `mongo.addresses/database`: MongoDB details (when job.queue=mongo)
- `job.max.retry.times`: Max retry attempts (default 10)

### TaskTracker Configuration
- `job.pull.frequency`: Task pull frequency in seconds (default 3)
- `stop.working`: Auto-stop when isolated from JobTracker (default false)

### Zookeeper Configuration
- `zk.client`: ZK client implementation (zkclient or curator)

## SPI Extension Points

1. **JobLogger**: Custom business log handlers
   - Implement `JobLogger` and `JobLoggerFactory`
   - Register in `META-INF/lts/com.github.ltsopensource.biz.logger.JobLoggerFactory`
   - Use via `job.logger=xxx` config

2. **JobQueue**: Custom task queue storage
   - See `lts-queue-mysql` or `lts-queue-mongo` implementations
   - Zero-troughput integration

## Development Standards

From `开发者规范.md`:

1. **Dependency Management**: Avoid unnecessary dependencies; mark plugin jars as `provided`
2. **Code Organization**:
   - Examples: Place in `lts-example` module
   - Tests: Place in `test` directories
3. **Architecture Rule**: Core modules (lts-core) must NOT use Spring; Spring is an extension in `lts-spring`
4. **Contribution Workflow**:
   - New contributors: Merge to `develop` branch first
   - After review, stable developers can commit to `master`
   - Coordinate with maintainer (QQ: 254963746) before major work

## Testing JobRunners

To test TaskTracker JobRunner implementations without starting full cluster:

```java
public class TestJobRunnerTester extends JobRunnerTester {
    public static void main(String[] args) throws Throwable {
        Job job = new Job();
        job.setTaskId("2313213");
        JobContext jobContext = new JobContext();
        jobContext.setJob(job);
        JobExtInfo jobExtInfo = new JobExtInfo();
        jobExtInfo.setRetry(false);
        jobContext.setJobExtInfo(jobExtInfo);

        TestJobRunnerTester tester = new TestJobRunnerTester();
        Result result = tester.run(jobContext);
        System.out.println(JSON.toJSONString(result));
    }

    @Override
    protected void initContext() {
        // Initialize Spring context if needed
    }

    @Override
    protected JobRunner newJobRunner() {
        return new TestJobRunner();
    }
}
```

## Spring Integration

### Spring Boot (Recommended)
```java
@SpringBootApplication
@EnableJobTracker       // Starts JobTracker
@EnableJobClient        // Starts JobClient
@EnableTaskTracker      // Starts TaskTracker
@EnableMonitor          // Starts Monitor
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```
Configure via `application.properties`. See `lts-examples/springboot` package.

### Spring XML
- `JobClientFactoryBean` for JobClient
- `TaskTrackerAnnotationFactoryBean` for TaskTracker

### Spring Annotations
- `@Configuration` with factory beans
- See `docs/LTS_Spring全注解使用说明.md` for details

## Deployment

After running `./build.sh`:
1. Distribution created in `dist/lts-1.7.2-SNAPSHOT-bin.zip`
2. Extract and configure:
   - JobTracker: Edit `conf/zoo/jobtracker.cfg`
   - LTS-Admin: Edit `conf/lts-admin.cfg`
   - TaskTracker: Edit `conf/tasktracker.cfg`
3. Start services:
   - JobTracker: `sh jobtracker.sh zoo start`
   - LTS-Admin: `sh lts-admin.sh`
   - TaskTracker: Configure and start via your application

## Key Dependencies

- **Java**: 1.6+
- **Maven**: 3.x
- **Zookeeper**: 3.4.5+ (for registry)
- **MongoDB**: 3.0.2+ or **MySQL**: 5.1.26+ (for task storage)
- **Netty**: 4.0.20.Final or **Apache MINA**: 2.0.9
- **Spring Framework**: 4.2.5.RELEASE
- **Spring Boot**: 1.3.3.RELEASE

## Important Files

- `pom.xml`: Parent POM with dependency management
- `build.sh` / `build.cmd`: Distribution build scripts
- `开发者规范.md`: Developer standards (Chinese)
- `开发计划.md`: Development roadmap (Chinese)
- `docs/`: Additional documentation
  - `LTS文档.md`: User documentation
  - `LTS_Spring全注解使用说明.md`: Spring annotation usage
  - `包引入说明.md`: Dependency injection guide

## Best Practices

1. **Resource Management**: Use only one JobClient per JVM; use one TaskTracker per JVM when possible
2. **Task Dispatching**: Use a JobRunner dispatcher pattern for multiple task types in one TaskTracker
3. **Testing**: Use JobRunnerTester for unit testing JobRunner logic
4. **Monitoring**: Use LTS-Admin for real-time monitoring of nodes and task execution
5. **Configuration**: Configure FailStore for production deployments (leveldb recommended)