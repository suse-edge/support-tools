# components_versions/core.py
import json
import logging
import os
from typing import Dict, List

from kubernetes import client, config
from pyhelm3 import Client, Command
from tabulate import tabulate

CHARTS_AND_PRODUCTS = {"longhorn": ["SUSE Storage","Longhorn"],
                       "metal3": ["Metal3"],
                       "metallb": ["MetalLB"],
                       "endpoint-copier-operator": ["Endpoint Copier Operator"],
                       "elemental-operator": ["Elemental"],
                       "rancher": ["SUSE Rancher Prime","Rancher Prime"],
                       "cdi": ["Containerized Data Importer"],
                       "kubevirt": ["KubeVirt"],
                       "neuvector": ["SUSE Security","NeuVector"],
                       "sriov-network-operator": ["SR-IOV Network Operator"],
                       "akri": ["Akri (tech-preview)"],
                       "rancher-turtles": ["Rancher Turtles (CAPI)"],
                       "system-upgrade-controller": ["System Upgrade Controller"],
                       "upgrade-controller": ["Upgrade Controller"]}

async def get_helm_chart_info(kubeconfig_path: str,
                              chart_names: List[str],
                              get_resources: bool) -> Dict:
    """
    Retrieves specific Helm chart information using pyhelm3.
    """
    chart_info = {}
    try:
        helm = Client(kubeconfig=kubeconfig_path)
        releases = await helm.list_releases(all_namespaces=True)

        for release in releases:
            if release.name in chart_names:
                revision = await release.current_revision()
                if revision is not None:  # Check if revision is not None
                    chart_metadata = await revision.chart_metadata()
                    if chart_metadata is not None:  # Check if chart_metadata is not None
                        chart_info[release.name] = {
                            "version": f"{chart_metadata.version}",
                            "namespace": release.namespace,
                            "revision": revision.revision,
                            "resources": [],
                            "pods": {}
                        }
                        if get_resources:
                            command = Command(kubeconfig=kubeconfig_path)
                            resources = await command.get_resources(
                                release_name=release.name,
                                namespace=release.namespace)
                            if resources is not None:  # Check if resources is not None
                                for resource in resources:
                                    if resource is not None and isinstance(resource, dict) and 'kind' in resource and 'metadata' in resource and 'name' in resource['metadata']:
                                        chart_info[release.name]["resources"].append({
                                            "kind": resource['kind'],
                                            "name": resource['metadata']['name']
                                        })
                                    else:
                                        logging.warning(
                                            f"Skipping invalid resource: {resource}")

                        # Get pod names and versions on the target namespace of the helm chart
                        # This should match the pods deployed by the chart in most of the cases
                        pods_info = get_pod_versions_by_namespace(
                            kubeconfig_path, release.namespace)
                        if pods_info is not None:  # Check if pods_info is not None
                            chart_info[release.name]["pods"] = pods_info

        return chart_info

    except Exception as e:
        logging.error(f"Error retrieving Helm chart information: {e}")
        return {}


def get_pod_versions_by_namespace(kubeconfig_path: str,
                                  namespace: str) -> Dict:
    """
    Retrieves pod image versions in a namespace.

    Args:
        kubeconfig_path: Path to the kubeconfig file.
        namespace: The namespace where the pods are located.

    Returns:
        A dictionary containing pod names as keys and lists of image versions as values.
    """
    try:
        config.load_kube_config(config_file=kubeconfig_path)
        v1 = client.CoreV1Api()
        pods = v1.list_namespaced_pod(namespace)
        pod_versions = {}
        for pod in pods.items:
            pod_name = pod.metadata.name
            image_versions = []
            for container in pod.spec.containers:
                image_versions.append(container.image)
            pod_versions[pod_name] = image_versions
        return pod_versions

    except Exception as e:
        logging.error(f"Error retrieving pod versions: {e}")
        return {}


def get_node_info(kubeconfig_path: str) -> Dict:
    """
    Retrieves node information (architecture, kernelVersion, kubeletVersion, operatingSystem, osImage).

    Args:
        kubeconfig_path: Path to the kubeconfig file.

    Returns:
        A dictionary containing node names as keys and node information dictionaries as values.
    """
    try:
        config.load_kube_config(config_file=kubeconfig_path)
        v1 = client.CoreV1Api()
        nodes = v1.list_node()
        node_info = {}
        for node in nodes.items:
            node_info[node.metadata.name] = {
                "architecture": node.status.node_info.architecture,
                "kernelVersion": node.status.node_info.kernel_version,
                "kubeletVersion": node.status.node_info.kubelet_version,
                "operatingSystem": node.status.node_info.operating_system,
                "osImage": node.status.node_info.os_image,
            }
        return node_info

    except Exception as e:
        logging.error(f"Error retrieving node information: {e}")
        return {}

def print_table_output(helm_info: Dict, node_info: Dict, edge_version: Dict, get_resources: bool):
    """
    Prints the cluster information in a table format.

    Args:
        helm_info: Dictionary containing Helm chart information.
        node_info: Dictionary containing node information.
        edge_version: Dictionary with the detected SUSE Edge version
        get_resources: Whether to get (and print) resources.
    """

    # Helm chart information
    for release_name, info in helm_info.items():
        print(f"\nRelease: {release_name}")

        # Helm Chart Table
        chart_table_data = [
            ["Version", info['version']],
            ["Namespace", info['namespace']],
            ["Revision", info['revision']]
        ]
        print(tabulate(chart_table_data,
                       tablefmt="grid",
                       numalign="left",
                       stralign="left"))

        if get_resources:
            # Resources table
            print("\n  Resources:")
            resources_table_data = []
            for resource in info["resources"]:
                resources_table_data.append(
                    [resource["kind"], resource["name"]])
            print(
                tabulate(resources_table_data,
                         headers=["Kind", "Name"],
                         tablefmt="grid",
                         numalign="left",
                         stralign="left"))

        # Pods table
        print("\n  Pods:")
        pods_table_data = []
        for pod_name, images in info["pods"].items():
            pods_table_data.append([pod_name, ", ".join(images)])
        print(tabulate(pods_table_data,
                       headers=["Pod Name", "Images"],
                       tablefmt="grid",
                       numalign="left",
                       stralign="left"))

    # Node information
    print("\nNode Information:")
    node_table_data = []
    for node_name, info in node_info.items():
        node_table_data.append([
            node_name, info["architecture"], info["kernelVersion"],
            info["kubeletVersion"], info["operatingSystem"], info["osImage"]
        ])
    print(tabulate(node_table_data,
                   headers=[
                       "Node", "Architecture", "Kernel Version",
                       "Kubelet Version", "Operating System", "OS Image"
                   ],
                   tablefmt="grid",
                   numalign="left",
                   stralign="left"))

    # Edge version
    print(f"\nSUSE Edge detected version: {edge_version['release']}")

    if edge_version['items_matching'] != {}:
        matching = edge_version['items_matching']
        matching_table_data = []
        for k, v in matching.items():
            matching_table_data.append([k, v])
        print(f"\nSUSE Edge items matching:")
        print(tabulate(matching_table_data, headers=["Component", "Version"],
                       tablefmt="grid",
                       numalign="left",
                       stralign="left"))

    if edge_version['items_not_matching'] != {}:
        notmatching = edge_version['items_not_matching']
        notmatching_table_data = []
        for k, v in notmatching.items():
            notmatching_table_data.append([k, v])
        print(f"\nSUSE Edge items NOT matching:")
        print(tabulate(notmatching_table_data, headers=["Component", "Version"],
                       tablefmt="grid",
                       numalign="left",
                       stralign="left"))


def check_edge_version(node_info, helm_info, edge_versions_dir):
    # Check for same versions on all the hosts
    kubelet_versions = set(node["kubeletVersion"]
                           for node in node_info.values())
    # Get the first one of the set
    kubelet_version = list(kubelet_versions)[0]
    # If the set is >1
    if len(kubelet_versions) != 1:
        print(
            f"Kubelet Versions mismatch! {kubelet_versions}, using {kubelet_version} as reference")
    # Try to match the distro
    # kube_distro = re.search(r"\+(k3s|rke2)r\d+", kubelet_version).group(1)
    # And version
    kube_version = kubelet_version.split("+")[0].split("v")[1]

    # Do the same for osImage
    os_images = set(node["osImage"] for node in node_info.values())
    os_image = list(os_images)[0]
    if len(os_images) != 1:
        print(
            f"Node osImage mismatch! {os_images}, using {os_image} as reference")

    # And kernel version
    kernel_versions = set(node["kernelVersion"] for node in node_info.values())
    kernel_version = list(kernel_versions)[0]
    if len(kernel_versions) != 1:
        print(
            f"Node kernel mismatch! {kernel_versions}, using {kernel_version} as reference")

    candidates = []

    edge_version = {}

    # Try to match the edge version with each one of the released versions
    for filename in os.listdir(edge_versions_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(edge_versions_dir, filename)
            try:
                with open(filepath, 'r') as f:
                    release_data = json.load(f)
                # Initialize the data
                edge_version = {"release": "unknown"}
                matches = {}
                notmatches = {}

                # Identify the candidate version
                candidate_version = release_data['Version']

                k3s_version = (release_data['Data']['K3s']['Version'])
                rke2_version = (release_data['Data']['RKE2']['Version'])

                if (k3s_version or rke2_version) == kube_version:
                    # Kube version matches
                    matches['kubeversion'] = kubelet_version
                else:
                    notmatches['kubeversion'] = kubelet_version

                # Time to check the helm charts
                for name, info in helm_info.items():
                    # This is required because chart name != product name
                    chart_name = sanitize_chart_name(name,release_data['Data'])
                    # Skip charts not found
                    if chart_name and release_data['Data'].get(chart_name):
                        chart_version = info['version']
                        release_version = release_data['Data'][chart_name]['Helm Chart Version']
                        if release_version == chart_version:
                            matches[name] = chart_version
                        else:
                            notmatches[name] = chart_version
                
                edge_version["items_matching"] = matches
                edge_version["items_not_matching"] = notmatches
                
                if notmatches == {}:
                    # Everything matches
                    edge_version["release"] = candidate_version
                    return edge_version
                elif matches == {}:
                    # Nothing matches
                    continue
                else:
                    # Posible match
                    candidates.append({"version": candidate_version, "items_matching": matches, "items_not_matching": notmatches})

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in {filename}: {e}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    # No exact matches, so choose the one with max matches
    if candidates:
        # Find and store the entire dictionary item that has the maximum number of matches
        best_candidate = max(candidates, key=lambda item: len(item["items_matching"]))
        
        # Now, access the desired fields from 'best_candidate' dictionary
        edge_version["release"] = f"Posible {best_candidate['version']}"
        edge_version["items_matching"] = best_candidate["items_matching"]
        edge_version["items_not_matching"] = best_candidate["items_not_matching"]
    else:
        edge_version["release"] = "unknown"
        edge_version["items_matching"] = {}
        edge_version["items_not_matching"] = {}

    return edge_version

def sanitize_chart_name(chart_name,data):
    candidates=CHARTS_AND_PRODUCTS[chart_name]
    if len(candidates) > 1:
        for candidate in candidates:
            if candidate in data:
                return candidate
    else:
        return candidates[0]
