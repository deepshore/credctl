# credctl

`credctl` is a simple command line application designed to exemplify how to build custom Kubernetes clients in Python.
It manages Kubernetes secrets, each of which contains credentials (username, password).
`credctl` is essentially based on the Python packages [click](https://click.palletsprojects.com/) and [kubernetes](https://github.com/kubernetes-client/python).

## Installation

Get `credctl`'s code like this:
```bash
git clone https://github.com/deepshore/credctl.git
```

Enter the project folder, create `venv` and activate it:
```bash
python3 -m venv venv
source venv/bin/activate
```

Make sure you have the latest version of `build` installed:
```bash
pip install --upgrade build
```

Build the package like this:
```bash
python -m build
```

Install the package like this:
```bash
pip install dist/credctl-0.0.1.tar.gz
```

Alternatively, `credctl` can also be installed "editable":
```bash
pip install -e .
```

Building the package is not necessary in this case.

Now the following command should be executable and show hints on how to use `credctl`:
```bash
credctl
```

## How to use `credctl`

### Create secrets

Create a Kubernetes secret containing credentials like this 
(you can optionally specify the namespace):
```bash
credctl create my-creds my-username my-password -n default
```

### List secrets

List all of the Kubernetes secrets managed by `credctl` like this:
```bash
credctl list
```

### Delete secrets 

You can delete secrets managed by `credctl` like this:
```bash
credctl delete my-creds
```

If the secret is not managed by `credctl`, the deletion is canceled:
```bash
kubectl create secret generic not-managed-by-credctl --from-literal==my-key=my-value
credctl delete not-managed-by-credctl
```
