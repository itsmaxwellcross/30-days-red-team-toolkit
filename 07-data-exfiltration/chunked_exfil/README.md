# Chunked File Exfiltration Framework

Split large files into small chunks for stealthy exfiltration.

## Features

- Split large files into configurable chunk sizes
- SHA256 hash verification for integrity
- Transfer state tracking and resume capability
- Automatic chunk reassembly with verification
- Progress monitoring

## Installation
```bash
# No external dependencies required (uses Python stdlib)
python3 chunked_exfil.py --help
```

## Usage

### Split a File
```bash
# Split with default 5MB chunks
python3 chunked_exfil.py --split sensitive_data.zip

# Split with custom chunk size (10MB)
python3 chunked_exfil.py --split database.sql --chunk-size 10
```

### Reassemble a File
```bash
# Reassemble using transfer ID
python3 chunked_exfil.py --reassemble a1b2c3d4e5f6...

# Reassemble to specific location
python3 chunked_exfil.py --reassemble a1b2c3d4e5f6... --output recovered.zip
```

### Check Progress
```bash
python3 chunked_exfil.py --progress a1b2c3d4e5f6...
```

## Module Usage
```python
from chunked_exfil import ChunkedExfiltration

# Initialize
exfil = ChunkedExfiltration(chunk_size=5*1024*1024)

# Split file
result = exfil.split_file('largefile.zip')
transfer_id = result['transfer_id']

# Get next chunk to transfer
chunk = exfil.get_next_chunk(transfer_id)

# Mark chunk as transferred
exfil.mark_chunk_transferred(transfer_id, chunk['chunk_index'])

# Check progress
progress = exfil.get_transfer_progress(transfer_id)

# Reassemble
exfil.reassemble_file(transfer_id, 'recovered.zip')
```

## Architecture

- `core.py` - Main ChunkedExfiltration interface
- `file_ops.py` - File splitting and reassembly
- `chunk_manager.py` - Transfer state and progress tracking
- `crypto.py` - Hash calculation and verification
- `cli.py` - Command-line interface

## Security Considerations

- Always verify hashes after reassembly
- Delete staging files after successful exfiltration
- Use appropriate chunk sizes based on network constraints
- Consider encrypting chunks before transfer