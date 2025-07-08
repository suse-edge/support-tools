# components_versions/cli.py
import asyncio
import json
import logging
import os
import sys
from argparse import ArgumentParser
from .core import check_edge_version, get_helm_chart_info, print_table_output, get_node_info

# Configure logging
logging.basicConfig(level=logging.WARN,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Default chart names
DEFAULT_CHARTS = ["cdi",
                  "elemental-operator",
                  "endpoint-copier-operator",
                  "kubevirt",
                  "longhorn",
                  "metal3",
                  "metallb",
                  "neuvector",
                  "rancher",
                  "rancher-turtles",
                  "sriov-network-operator",
                  "system-upgrade-controller",
                  "upgrade-controller"]

DEFAULT_KUBECONFIG = "/kubeconfig"
DEFAULT_VERSIONS_DIR = "/usr/share/suse-edge-components-versions"

async def _async_main():
    parser = ArgumentParser(description="Get Helm chart and pod versions.")
    parser.add_argument("-k",
                        "--kubeconfig",
                        help="Path to the kubeconfig file.")
    parser.add_argument("-c",
                        "--charts",
                        help="Comma-separated list of Helm chart names.")
    parser.add_argument(
        "-o",
        "--output",
        default="json",
        choices=["json", "table", "none"],
        help="Output format: json (default), table or none",
    )
    parser.add_argument("--get-resources",
                        action="store_true",
                        help="Include resources in the output")
    parser.add_argument("--versions-dir",
                        help="Directory storing the json files with Edge versions")

    args = parser.parse_args()

    kubeconfig_path = args.kubeconfig if args.kubeconfig else DEFAULT_KUBECONFIG
    output_format = args.output
    get_resources = args.get_resources
    edge_versions_dir = args.versions_dir if args.versions_dir else DEFAULT_VERSIONS_DIR

    chart_names = [
        name.strip() for name in args.charts.split(",")
    ] if args.charts is not None else DEFAULT_CHARTS

    # Check if kubeconfig file exists
    if not os.path.exists(kubeconfig_path):
        logging.error(f"Error: Kubeconfig file not found at {kubeconfig_path}")
        sys.exit(1)

    helm_info = await get_helm_chart_info(kubeconfig_path, chart_names, get_resources)
    node_info = get_node_info(kubeconfig_path)

    edge_version = check_edge_version(node_info, helm_info, edge_versions_dir)

    if output_format == "json":
        output_data = {"helm_charts": helm_info,
                       "nodes": node_info, "detected_edge_version": edge_version}
        if not get_resources:
            for chart_data in output_data["helm_charts"].values():
                chart_data.pop("resources", None)
        print(json.dumps(output_data, indent=2))
    elif output_format == "table":
        print_table_output(helm_info, node_info, edge_version, get_resources)
    elif output_format == "none":
        print(f"SUSE Edge detected version: {edge_version}")

# I don't want to do this but the helm python library needs it...
def main():
    asyncio.run(_async_main())

if __name__ == "__main__":
    main()