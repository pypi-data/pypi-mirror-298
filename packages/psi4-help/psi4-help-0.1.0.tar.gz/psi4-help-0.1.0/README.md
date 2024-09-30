# Psi4-help Script

## Overview

Psi4-help is a Python script designed to help users explore and understand the keywords and options available in the Psi4 quantum chemistry software. The script reads a YAML file containing Psi4 keyword information and provides a user-friendly interface to view and search through the data.

## Features

- List all top-level keys in the Psi4 keyword YAML file.
- Show detailed information for a specific top-level key, including optional parameters and descriptions.
- Print all top-level keys and their detailed information.
- Print all top-level keys and their secondary keys without descriptions.

## Requirements

- Python 3.6 or higher
- PyYAML
- colorama

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/FLongWang/psi4-help.git
   cd psi4-help