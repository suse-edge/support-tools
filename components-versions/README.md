# SUSE Edge Components Versions

This tool retrieves version information for Helm charts, pods, and nodes in a SUSE Edge Kubernetes cluster.

## Features

- Retrieves Helm chart versions, namespaces, revisions, and resources.
- Retrieves pod versions (container images) for each Helm chart.
- Retrieves node information (architecture, kernel version, kubelet version, operating system, OS image).
- Outputs the information in JSON or table format.
- Detects the Edge version.
- Easy to use container image based

## Usage

0.  **Prerequisites:**

    - podman

1.  **Run the container image:**

    ```bash
    podman run -it --rm -v /path/to/mykubeconfig:/kubeconfig registry.opensuse.org/isv/suse/edge/factory/images/suse-edge-components-versions:0.1.1
    ```

    If running the container directly on the host, `--net=host` is needed because the kubeconfig probably will point to 127.0.0.1:

    ```bash
    podman run -it --rm --net=host -v /path/to/mykubeconfig:/kubeconfig registry.opensuse.org/isv/suse/edge/factory/images/suse-edge-components-versions:0.1.1
    ```

There are a few optional flags like:

    ```bash
    podman run -it --rm registry.opensuse.org/isv/suse/edge/factory/images/suse-edge-components-versions:0.1.1 -h
    usage: suse-edge-components-versions [-h] [-k KUBECONFIG] [-c CHARTS] [-o {json,table,none}] [-r]
                                        [-d VERSIONS_DIR] [-v]

    Get Helm chart and pod versions.

    options:
      -h, --help            show this help message and exit
      -k KUBECONFIG, --kubeconfig KUBECONFIG
                            Path to the kubeconfig file.
      -c CHARTS, --charts CHARTS
                            Comma-separated list of Helm chart names.
      -o {json,table,none}, --output {json,table,none}
                            Output format: json (default), table or none
      -r, --get-resources   Include resources in the output
      -d VERSIONS_DIR, --versions-dir VERSIONS_DIR
                            Directory storing the json files with Edge versions
      -v, --version         Show program version
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
