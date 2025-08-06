#!/usr/bin/env python3
"""
Simple CLI wrapper for Demucs music source separation
Usage: python cli_example.py <input_file> [options]
"""

import argparse
import os
import sys
from pathlib import Path
import torch
from demucs import api

def main():
    parser = argparse.ArgumentParser(description='Demucs CLI - Music Source Separation')
    parser.add_argument('input', type=str, help='Input audio file path')
    parser.add_argument('-o', '--output', type=str, default='/app/output', 
                        help='Output directory (default: /app/output)')
    parser.add_argument('-m', '--model', type=str, default='htdemucs',
                        help='Model name (default: htdemucs)')
    parser.add_argument('--mp3', action='store_true', 
                        help='Save output as MP3 instead of WAV')
    parser.add_argument('--two-stems', type=str, choices=['vocals', 'drums', 'bass', 'other'],
                        help='Extract only two stems: selected stem and everything else')
    parser.add_argument('--device', type=str, default='cuda' if torch.cuda.is_available() else 'cpu',
                        help='Device to use (cuda/cpu)')
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)
    
    print(f"Processing: {args.input}")
    print(f"Model: {args.model}")
    print(f"Device: {args.device}")
    print(f"Output directory: {args.output}")
    
    try:
        # Initialize separator
        separator = api.Separator(
            model=args.model,
            device=args.device,
        )
        
        # Process the audio file
        origin, separated = separator.separate_audio_file(args.input)
        
        # Get the base filename without extension
        base_name = Path(args.input).stem
        
        # Save separated sources
        for stem, source in separated.items():
            if args.two_stems:
                # Two-stem mode: save only the selected stem and 'other'
                if stem == args.two_stems:
                    output_file = os.path.join(args.output, f"{base_name}_{stem}")
                else:
                    continue
            else:
                output_file = os.path.join(args.output, f"{base_name}_{stem}")
            
            if args.mp3:
                output_file += ".mp3"
                separator.save_audio(source, output_file, samplerate=separator.samplerate)
            else:
                output_file += ".wav"
                separator.save_audio(source, output_file, samplerate=separator.samplerate)
            
            print(f"Saved: {output_file}")
        
        # If two-stem mode, create the 'other' mix
        if args.two_stems:
            other_stems = [source for stem, source in separated.items() if stem != args.two_stems]
            if other_stems:
                other_mix = sum(other_stems)
                output_file = os.path.join(args.output, f"{base_name}_no_{args.two_stems}")
                if args.mp3:
                    output_file += ".mp3"
                else:
                    output_file += ".wav"
                separator.save_audio(other_mix, output_file, samplerate=separator.samplerate)
                print(f"Saved: {output_file}")
        
        print("Processing complete!")
        
    except Exception as e:
        print(f"Error during processing: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()