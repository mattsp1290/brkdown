# BRKDOWN
## Introduction
A small CLI for automating music tasks related to curating a sample library

## Installation
`pip install -e "git+https://github.com/mattsp1290/brkdown.git#egg=brkdown"`

## Usage
`brkdown split $HOME/Documents/Album/ $HOME/brkdown/output`
Will take every audio file in the $HOME/Documents/Album/ and split it apart by silences, then write those as wav files to $HOME/brkdown/output