## ADDED Requirements

### Requirement: Representative benchmark workloads
The benchmark suite SHALL measure primitive, flat object, nested collection, successful validation, and aggregated-failure validation workloads using deterministic inputs.

#### Scenario: Complete benchmark run
- **WHEN** the documented benchmark command runs
- **THEN** every workload executes and produces named measurements

### Requirement: Reproducible benchmark metadata
Benchmark results SHALL record Python version, implementation, platform, dependency versions, benchmark configuration, and source revision in machine-readable form.

#### Scenario: Result artifact inspection
- **WHEN** a benchmark JSON artifact is downloaded
- **THEN** it contains sufficient environment and configuration metadata to interpret and compare the measurements

### Requirement: Non-blocking trend comparison
CI SHALL retain benchmark results for comparison but SHALL NOT use a fixed noisy microbenchmark threshold as the sole release gate.

#### Scenario: Benchmark CI job
- **WHEN** benchmark CI completes
- **THEN** machine-readable results are uploaded regardless of whether timing differs from a previous runner

### Requirement: Local benchmark workflow
Documentation SHALL provide commands for running, recording, and comparing benchmarks locally.

#### Scenario: Contributor benchmark run
- **WHEN** a contributor follows the documented commands in a synchronized development environment
- **THEN** equivalent workload names and result formats are produced
