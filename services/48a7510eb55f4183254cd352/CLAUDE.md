# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Gradle AWS Plugin is a Gradle plugin that provides tasks for managing AWS resources (S3, EC2, RDS, Route53, Elastic Beanstalk, CloudFormation, Lambda, IAM, SQS, SNS, SSM, CloudWatch, ECR, ELB).

## Build Commands

```bash
./gradlew build               # Clean and build (default task)
./gradlew check               # Run all code quality checks and tests
./gradlew check jacocoTestReport  # Check with code coverage report
./gradlew resolveDependencies # Resolve all dependencies
./gradlew test                # Run tests only
./gradlew checkstyleMain      # Run checkstyle on main source
./gradlew spotlessApply       # Apply code formatting fixes
./gradlew publishPlugins      # Publish to Gradle plugin portal (requires credentials)
```

## Architecture

### Plugin System

The plugin uses a multi-level architecture:

1. **Root Plugin** (`AwsPlugin`): Registers `AwsPluginExtension` which holds credentials and region configuration
2. **Service Plugins** (e.g., `AmazonS3Plugin`): Each service plugin extends `AwsPlugin` and registers its own extension

### Common Patterns

**Extension Classes**:
- Each service has an `*PluginExtension` class (e.g., `AmazonS3PluginExtension`)
- Extends `BasePluginExtension<T>` which provides lazy initialization of AWS SDK clients
- Clients are created using credentials from `AwsPluginExtension`

**Task Classes**:
- Extend `org.gradle.api.internal.ConventionTask`
- Annotated with `@TaskAction` for the main task logic
- Properties use Lombok `@Getter`/`@Setter`
- Group is set to "AWS" for task organization
- Use `getProject().getExtensions().getByType()` to access service extension

**Example Task Structure**:
```java
public class CreateBucketTask extends ConventionTask {
    @Getter @Setter private String bucketName;
    @Getter @Setter private String region;

    public CreateBucketTask() {
        setDescription("Create the Amazon S3 bucket.");
        setGroup("AWS");
    }

    @TaskAction
    public void createBucket() {
        AmazonS3PluginExtension ext = getProject().getExtensions()
            .getByType(AmazonS3PluginExtension.class);
        AmazonS3 s3 = ext.getClient();
        // Task logic
    }
}
```

### Source Organization

- `src/main/java/jp/classmethod/aws/gradle/` - Root plugin and common classes
- `src/main/java/jp/classmethod/aws/gradle/{service}/` - Service-specific tasks and plugins
- `src/main/resources/META-INF/gradle-plugins/` - Plugin registration properties files
- `config/` - Code quality configurations (checkstyle, findbugs, pmd, forbiddenapis, spotless)
- `samples/` - Example projects demonstrating plugin usage per service

## Code Style

The project uses Spotless for formatting with Eclipse formatter config. Run `./gradlew spotlessApply` before committing.

## Testing

Tests are written in Groovy with Spock framework in `src/test/groovy/`. Run with `./gradlew test`.

## Credentials

AWS credentials are resolved from `AwsPluginExtension`, which uses the standard AWS SDK credential resolution chain (environment variables, system properties, AWS credentials file, etc.).