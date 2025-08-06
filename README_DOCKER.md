# Demucs Docker GPU Setup

This directory contains a GPU-enabled Docker setup for running Demucs music source separation.

## Prerequisites

- Docker with GPU support
- NVIDIA Container Toolkit
- NVIDIA GPU with CUDA support

## Environment Details

- Base Image: NVIDIA PyTorch 23.10
- Python Version: 3.10 (included in the base image)
- CUDA Version: 12.2 (included in the base image)
- PyTorch Version: 2.1.0 (included in the base image)

## Building the Docker Image

```bash
docker-compose build
```

## Usage

### Using the standard Demucs CLI

```bash
# Process test.mp3
docker compose run --rm demucs-docker python -m demucs test.mp3 -o /app/output

# Process a file from the input directory
docker compose run --rm demucs-docker python -m demucs /app/input/song.mp3 -o /app/output

# Use a specific model
docker compose run --rm demucs-docker python -m demucs /app/input/song.mp3 -o /app/output -n htdemucs_6s
```

### Using the custom CLI wrapper (cli_example.py)

```bash
# Basic usage
docker compose run --rm demucs-docker python cli_example.py /app/input/song.mp3

# Save as MP3
docker compose run --rm demucs-docker python cli_example.py /app/input/song.mp3 --mp3

# Extract only vocals
docker compose run --rm demucs-docker python cli_example.py /app/input/song.mp3 --two-stems vocals

# Use a different model
docker compose run --rm demucs-docker python cli_example.py /app/input/song.mp3 -m htdemucs_ft
```

## Directory Structure

- `input/` - Place your audio files here
- `output/` - Separated tracks will be saved here
- `test.mp3` - Sample audio file included with Demucs

## Available Models

- `htdemucs` - Default model, good quality
- `htdemucs_ft` - Fine-tuned version
- `htdemucs_6s` - 6-source model
- `mdx` - MDX model
- `mdx_extra` - MDX with extra training
- `mdx_q` - Quantized MDX
- `mdx_extra_q` - Quantized MDX extra

