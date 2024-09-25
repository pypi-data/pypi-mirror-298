# `contswi` - Kubernetes Context Switcher

`contswi` is a simple but effective command-line tool designed for Linux environments to quickly switch between different Kubernetes contexts. By leveraging `kubectl`, this tool allows users to select and change their active context using an intuitive menu-driven interface, navigable with arrow keys.

## Features

- Quickly view all available Kubernetes contexts.
- Highlight the current active context.
- Easily switch between contexts using an interactive, arrow-key driven menu.
- Clean, responsive, and simple interface that fits into any Kubernetes workflow.

## Requirements

Before using `contswi`, ensure you have the following set up:

1. **kubectl**: The Kubernetes command-line tool must be installed and properly configured on your system. This application interacts directly with `kubectl` to retrieve and set contexts.
   
   - Installation guide: [kubectl official documentation](https://kubernetes.io/docs/tasks/tools/)
   
2. **Pre-configured Kubernetes Contexts**: You must have one or more Kubernetes contexts already set up in your `kubeconfig`. If you don't have any contexts configured, refer to the [Kubernetes context documentation](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/#context) to set them up.

## Installation

You can install the `contswi` tool in two ways: directly from the source code or via pip.

### 1. Installing from Source

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/contswi.git
   cd contswi
   ```

2. **Install the tool**:

   After cloning the repository, you can install the tool locally with pip:

   ```bash
   pip install .
   ```

### 2. Installing via pip

To install the tool directly from PyPI, simply run:

```bash
pip install contswi
```


## Usage

Once installed, you can use the `contswi` tool to interactively switch Kubernetes contexts.

### Run the tool

```bash
contswi
```

### Key Bindings

- **Up Arrow (`↑`)**: Move the selection upwards.
- **Down Arrow (`↓`)**: Move the selection downwards.
- **Enter**: Select the highlighted context and switch to it.
- **Ctrl+C**: Exit the program at any time.

### Example

1. Running `contswi` will present a list of your Kubernetes contexts:
   ```
     dev-cluster  
   > prod-cluster <  
     staging-cluster  
   ```

2. Use the arrow keys to navigate through the contexts and press **Enter** to switch.

3. The tool will execute the equivalent of:
   ```bash
   kubectl config use-context <selected_context>
   ```

4. You will see the selected context become the active one.

## Error Handling

If you encounter any errors or issues with the program (e.g., no configured contexts), the tool will handle it gracefully, providing helpful error messages.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the functionality of this tool. Contributions are always welcome!

---

### Author

**Gabor Puskas**  
[GitHub](https://github.com/Savalinn)  
[LinkedIn](https://www.linkedin.com/in/gaborpuskas/)

---

`contswi` is designed to make Kubernetes context management fast and simple, enhancing the experience for developers and DevOps engineers working across multiple clusters and environments.
