# SUSE Edge Components Versions

This tool retrieves version information for Helm charts, pods, and nodes in a SUSE Edge Kubernetes cluster.

## Features

- Retrieves Helm chart versions, namespaces, revisions, and resources.
- Retrieves pod versions (container images) for each Helm chart.
- Retrieves node information (architecture, kernel version, kubelet version, operating system, OS image).
- Outputs the information in JSON or table format.
- Detects the Edge version.

## Usage

0.  **Prerequisites:**

    - python3
    - helm

    Ideally a virtualenv should be created:

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

1.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the script:**

    ```bash
    python suse-edge-components-versions.py -k <kubeconfig_path> -c <chart_names> -o <output_format> --versions-dir edge-versions/
    ```

    - `-k`: Path to the kubeconfig file (optional). If not provided, defaults to `/kubeconfig`
    - `-c`: Comma-separated list of Helm chart names (optional). If not provided, defaults to `metallb, endpoint-copier-operator, 
rancher, longhorn, cdi,
kubevirt, neuvector, elemental-operator,
sriov-network-operator, akri, metal3, system-upgrade-controller & rancher-turtles`.
    - `-o`: Output format: `json` (default) or `table`.
    - `--get-resources`: Get (and print) resources created by the helm chart.
    - `-h`: Show help.
    - `--versions-dir`: Directory storing the json files with Edge versions

**Example:**

```bash
python suse-edge-components-versions.py -k /path/to/kubeconfig -c cert-manager,metallb -o table --versions-dir edge-versions/
```

## Example output

- Json

```bash
{
  "helm_charts": {
    "elemental-operator": {
      "version": "1.6.5",
      "namespace": "cattle-elemental-system",
      "revision": 1,
      "pods": {
        "elemental-operator-767db5756c-ctlth": [
          "registry.suse.com/rancher/elemental-operator:1.6.5"
        ]
      }
    },
    "endpoint-copier-operator": {
      "version": "302.0.0+up0.2.1",
      "namespace": "endpoint-copier-operator",
      "revision": 1,
      "pods": {
        "endpoint-copier-operator-7bf97b9d45-g5lwt": [
          "registry.suse.com/edge/3.2/endpoint-copier-operator:0.2.0"
        ],
        "endpoint-copier-operator-7bf97b9d45-rvqtv": [
          "registry.suse.com/edge/3.2/endpoint-copier-operator:0.2.0"
        ]
      }
    },
    "metallb": {
      "version": "302.0.0+up0.14.9",
      "namespace": "metallb-system",
      "revision": 1,
      "pods": {
        "metallb-controller-5756c8898-hhw8k": [
          "registry.suse.com/edge/3.2/metallb-controller:v0.14.8"
        ],
        "metallb-speaker-4x8p5": [
          "registry.suse.com/edge/3.2/metallb-speaker:v0.14.8"
        ],
        "metallb-speaker-ctbnw": [
          "registry.suse.com/edge/3.2/metallb-speaker:v0.14.8"
        ],
        "metallb-speaker-pwqzm": [
          "registry.suse.com/edge/3.2/metallb-speaker:v0.14.8"
        ]
      }
    },
    "rancher": {
      "version": "2.10.1",
      "namespace": "cattle-system",
      "revision": 1,
      "pods": {
        "rancher-7899bd4998-jpj4d": [
          "registry.rancher.com/rancher/rancher:v2.10.1"
        ],
        "rancher-webhook-79798674c5-zpfmn": [
          "registry.rancher.com/rancher/rancher-webhook:v0.6.2"
        ],
        "system-upgrade-controller-56696956b-8hzhr": [
          "registry.rancher.com/rancher/system-upgrade-controller:v0.14.2"
        ]
      }
    },
    "system-upgrade-controller": {
      "version": "105.0.1",
      "namespace": "cattle-system",
      "revision": 2,
      "pods": {
        "rancher-7899bd4998-jpj4d": [
          "registry.rancher.com/rancher/rancher:v2.10.1"
        ],
        "rancher-webhook-79798674c5-zpfmn": [
          "registry.rancher.com/rancher/rancher-webhook:v0.6.2"
        ],
        "system-upgrade-controller-56696956b-8hzhr": [
          "registry.rancher.com/rancher/system-upgrade-controller:v0.14.2"
        ]
      }
    }
  },
  "nodes": {
    "vm1": {
      "architecture": "amd64",
      "kernelVersion": "6.4.0-18-default",
      "kubeletVersion": "v1.31.6+rke2r1",
      "operatingSystem": "linux",
      "osImage": "SUSE Linux Micro 6.0"
    },
    "vm2": {
      "architecture": "amd64",
      "kernelVersion": "6.4.0-18-default",
      "kubeletVersion": "v1.31.6+rke2r1",
      "operatingSystem": "linux",
      "osImage": "SUSE Linux Micro 6.0"
    },
    "vm3": {
      "architecture": "amd64",
      "kernelVersion": "6.4.0-18-default",
      "kubeletVersion": "v1.31.6+rke2r1",
      "operatingSystem": "linux",
      "osImage": "SUSE Linux Micro 6.0"
    }
  },
  "detected_edge_version": {
    "release": "Posible 3.2.0",
    "items_matching": {
      "elemental-operator": "1.6.5",
      "endpoint-copier-operator": "302.0.0+up0.2.1",
      "metallb": "302.0.0+up0.14.9",
      "rancher": "2.10.1",
      "system-upgrade-controller": "105.0.1"
    },
    "items_not_matching": {
      "kubeversion": "v1.31.6+rke2r1"
    }
  }
}
```

- Table

```
Release: elemental-operator
+-----------+-------------------------+
| Version   | 1.6.5                   |
+-----------+-------------------------+
| Namespace | cattle-elemental-system |
+-----------+-------------------------+
| Revision  | 1                       |
+-----------+-------------------------+

  Pods:
+-------------------------------------+----------------------------------------------------+
| Pod Name                            | Images                                             |
+=====================================+====================================================+
| elemental-operator-767db5756c-ctlth | registry.suse.com/rancher/elemental-operator:1.6.5 |
+-------------------------------------+----------------------------------------------------+

Release: endpoint-copier-operator
+-----------+--------------------------+
| Version   | 302.0.0+up0.2.1          |
+-----------+--------------------------+
| Namespace | endpoint-copier-operator |
+-----------+--------------------------+
| Revision  | 1                        |
+-----------+--------------------------+

  Pods:
+-------------------------------------------+-----------------------------------------------------------+
| Pod Name                                  | Images                                                    |
+===========================================+===========================================================+
| endpoint-copier-operator-7bf97b9d45-g5lwt | registry.suse.com/edge/3.2/endpoint-copier-operator:0.2.0 |
+-------------------------------------------+-----------------------------------------------------------+
| endpoint-copier-operator-7bf97b9d45-rvqtv | registry.suse.com/edge/3.2/endpoint-copier-operator:0.2.0 |
+-------------------------------------------+-----------------------------------------------------------+

Release: metallb
+-----------+------------------+
| Version   | 302.0.0+up0.14.9 |
+-----------+------------------+
| Namespace | metallb-system   |
+-----------+------------------+
| Revision  | 1                |
+-----------+------------------+

  Pods:
+------------------------------------+-------------------------------------------------------+
| Pod Name                           | Images                                                |
+====================================+=======================================================+
| metallb-controller-5756c8898-hhw8k | registry.suse.com/edge/3.2/metallb-controller:v0.14.8 |
+------------------------------------+-------------------------------------------------------+
| metallb-speaker-4x8p5              | registry.suse.com/edge/3.2/metallb-speaker:v0.14.8    |
+------------------------------------+-------------------------------------------------------+
| metallb-speaker-ctbnw              | registry.suse.com/edge/3.2/metallb-speaker:v0.14.8    |
+------------------------------------+-------------------------------------------------------+
| metallb-speaker-pwqzm              | registry.suse.com/edge/3.2/metallb-speaker:v0.14.8    |
+------------------------------------+-------------------------------------------------------+

Release: rancher
+-----------+---------------+
| Version   | 2.10.1        |
+-----------+---------------+
| Namespace | cattle-system |
+-----------+---------------+
| Revision  | 1             |
+-----------+---------------+

  Pods:
+-------------------------------------------+----------------------------------------------------------------+
| Pod Name                                  | Images                                                         |
+===========================================+================================================================+
| rancher-7899bd4998-jpj4d                  | registry.rancher.com/rancher/rancher:v2.10.1                   |
+-------------------------------------------+----------------------------------------------------------------+
| rancher-webhook-79798674c5-zpfmn          | registry.rancher.com/rancher/rancher-webhook:v0.6.2            |
+-------------------------------------------+----------------------------------------------------------------+
| system-upgrade-controller-56696956b-8hzhr | registry.rancher.com/rancher/system-upgrade-controller:v0.14.2 |
+-------------------------------------------+----------------------------------------------------------------+

Release: system-upgrade-controller
+-----------+---------------+
| Version   | 105.0.1       |
+-----------+---------------+
| Namespace | cattle-system |
+-----------+---------------+
| Revision  | 2             |
+-----------+---------------+

  Pods:
+-------------------------------------------+----------------------------------------------------------------+
| Pod Name                                  | Images                                                         |
+===========================================+================================================================+
| rancher-7899bd4998-jpj4d                  | registry.rancher.com/rancher/rancher:v2.10.1                   |
+-------------------------------------------+----------------------------------------------------------------+
| rancher-webhook-79798674c5-zpfmn          | registry.rancher.com/rancher/rancher-webhook:v0.6.2            |
+-------------------------------------------+----------------------------------------------------------------+
| system-upgrade-controller-56696956b-8hzhr | registry.rancher.com/rancher/system-upgrade-controller:v0.14.2 |
+-------------------------------------------+----------------------------------------------------------------+

Node Information:
+--------+----------------+------------------+-------------------+--------------------+----------------------+
| Node   | Architecture   | Kernel Version   | Kubelet Version   | Operating System   | OS Image             |
+========+================+==================+===================+====================+======================+
| vm1    | amd64          | 6.4.0-18-default | v1.31.6+rke2r1    | linux              | SUSE Linux Micro 6.0 |
+--------+----------------+------------------+-------------------+--------------------+----------------------+
| vm2    | amd64          | 6.4.0-18-default | v1.31.6+rke2r1    | linux              | SUSE Linux Micro 6.0 |
+--------+----------------+------------------+-------------------+--------------------+----------------------+
| vm3    | amd64          | 6.4.0-18-default | v1.31.6+rke2r1    | linux              | SUSE Linux Micro 6.0 |
+--------+----------------+------------------+-------------------+--------------------+----------------------+

SUSE Edge detected version: Posible 3.2.0

SUSE Edge items matching:
+---------------------------+------------------+
| Component                 | Version          |
+===========================+==================+
| elemental-operator        | 1.6.5            |
+---------------------------+------------------+
| endpoint-copier-operator  | 302.0.0+up0.2.1  |
+---------------------------+------------------+
| metallb                   | 302.0.0+up0.14.9 |
+---------------------------+------------------+
| rancher                   | 2.10.1           |
+---------------------------+------------------+
| system-upgrade-controller | 105.0.1          |
+---------------------------+------------------+

SUSE Edge items NOT matching:
+-------------+----------------+
| Component   | Version        |
+=============+================+
| kubeversion | v1.31.6+rke2r1 |
+-------------+----------------+
```

## Contributing

Contributions are welcome! Feel free to open issues or pull requests.
