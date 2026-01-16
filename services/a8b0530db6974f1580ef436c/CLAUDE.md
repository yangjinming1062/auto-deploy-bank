# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

dd-trace-java is Datadog's APM (Application Performance Monitoring) client library for Java. It provides distributed tracing, continuous profiling, error tracking, and other observability features through automatic bytecode instrumentation of Java applications.

**Key directories:**
- `dd-java-agent/` - Main Java agent implementation and ~200 framework instrumentations
- `dd-trace-core/` - Core tracing functionality (span creation, propagation, sampling)
- `dd-trace-api/` - Public tracing API definitions
- `internal-api/` - Internal API for instrumentation
- `dd-smoke-tests/` - Integration smoke tests with real applications
- `components/` - Shared components (context, environment, JSON, native-loader, yaml)
- `telemetry/` - Telemetry collection and reporting
- `remote-config/` - Remote configuration support

## Build Commands

```bash
# Quick build without tests
./gradlew clean assemble

# Build everything (takes very long - not recommended locally)
./gradlew clean build

# Build only the JVM agent JAR
./gradlew :dd-java-agent:shadowJar
# Output: dd-java-agent/build/libs/dd-java-agent-*.jar

# Check code formatting
./gradlew spotlessCheck

# Auto-format code
./gradlew spotlessApply

# Run muzzle version compatibility checks
./gradlew muzzle
```

## Test Commands

```bash
# Run tests for a specific instrumentation
./gradlew :dd-java-agent:instrumentation:<name>:test
# Example: ./gradlew :dd-java-agent:instrumentation:google-http-client:test

# Run tests for a specific module
./gradlew :dd-trace-core:test

# Run latest dependency tests (checks against latest framework versions)
./gradlew latestDepTest
./gradlew :dd-java-agent:instrumentation:<name>:latestDepTest

# Run forked tests (tests that run in a separate JVM)
./gradlew forkedTest
./gradlew :dd-java-agent:instrumentation:<name>:forkedTest

# Run tests on a different JVM version
JAVA_21_HOME=/path/to/jdk-21 ./gradlew test -PtestJvm=21
```

## Environment Setup

Requires JDK versions 8, 11, 17, 21, and 25, plus GraalVM 17:
```bash
export JAVA_8_HOME=/path/to/jdk8
export JAVA_11_HOME=/path/to/jdk11
export JAVA_17_HOME=/path/to/jdk17
export JAVA_21_HOME=/path/to/jdk21
export JAVA_25_HOME=/path/to/jdk25
export JAVA_GRAALVM17_HOME=/path/to/graalvm17
export JAVA_HOME=$JAVA_8_HOME  # PATH should point to this
```

For Akka HTTP 10.6 instrumentation, set: `ORG_GRADLE_PROJECT_akkaRepositoryToken=<token>`

## Instrumentation Architecture

Instrumentations use ByteBuddy to inject bytecode at runtime. Key patterns:

**Instrumentation class** - Extends `InstrumenterModule.Tracing` and implements an `Instrumenter` interface:
```java
@AutoService(InstrumenterModule.class)
public class FooInstrumentation extends InstrumenterModule.Tracing
    implements Instrumenter.ForSingleType {

  public FooInstrumentation() {
    super("foo");  // integration name
  }

  @Override
  public String instrumentedType() {
    return "com.example.Foo";
  }

  @Override
  public void adviceTransformations(AdviceTransformation transformation) {
    transformation.applyAdvice(
      isMethod().and(named("doSomething")).and(takesArguments(0)),
      getClass().getName() + "$FooAdvice"
    );
  }
}
```

**Advice class** - Contains `@Advice.OnMethodEnter` and `@Advice.OnMethodExit` annotated methods:
```java
public static class FooAdvice {
  @Advice.OnMethodEnter(suppress = Throwable.class)
  public static AgentScope enter(@Advice.This Foo foo) {
    AgentSpan span = startSpan(OPERATION_NAME);
    DECORATE.afterStart(span);
    return activateSpan(span);
  }

  @Advice.OnMethodExit(onThrowable = Throwable.class, suppress = Throwable.class)
  public static void exit(@Advice.Enter AgentScope scope,
                          @Advice.Thrown Throwable throwable) {
    AgentSpan span = scope.span();
    DECORATE.onError(span, throwable);
    span.finish();
    scope.close();
  }
}
```

**Decorator class** - Extends `HttpClientDecorator`, `HttpServerDecorator`, `DatabaseClientDecorator`, etc.:
```java
public class FooDecorator extends HttpClientDecorator<FooRequest, FooResponse> {
  public static final FooDecorator DECORATE = new FooDecorator();
  public static final CharSequence OPERATION_NAME = UTF8BytesString.create("foo.request");

  @Override protected String method(FooRequest request) { return request.getMethod(); }
  @Override protected URI url(FooRequest request) { return URIUtils.safeParse(request.getUrl()); }
  @Override protected int status(FooResponse response) { return response.getStatusCode(); }
  @Override protected String component() { return COMPONENT_NAME; }
}
```

**Helper classes** - All classes referenced by Advice must be listed in `helperClassNames()`:
```java
@Override
public String[] helperClassNames() {
  return new String[]{
    packageName + ".FooDecorator",
    packageName + ".FooSetter"
  };
}
```

**Muzzle directives** - Declare library versions the instrumentation is compatible with:
```groovy
muzzle {
  pass {
    group = "com.example"
    module = "foo-library"
    versions = "[1.0.0,2.0.0)"
    assertInverse = true
  }
}
```

## Key Concepts

- **Context Stores** - Attach data to objects across instrumented methods: `InstrumentationContext.get(Carrier.class, Data.class)`
- **CallDepthThreadLocalMap** - Prevent double-instrumentation in recursive calls
- **Scope/Continuation** - Pass trace context between threads
- **Muzzle** - Build-time version compatibility checks (does NOT run tests)

## Code Style

- Uses Google Java Format 1.32 (last version supporting Java 8)
- Java 8+ compatible for main code
- File naming: `*Instrumentation.java`, `*Advice.java`, `*Decorator.java`
- Integration names use kebab-case: `google-http-client`
- Package structure: `datadog.trace.instrumentation.<framework>`