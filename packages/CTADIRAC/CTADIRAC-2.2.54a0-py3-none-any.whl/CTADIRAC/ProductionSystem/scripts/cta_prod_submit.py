#!/usr/bin/env python
"""
Launch a production from a workflow description

Usage:
    cta-prod-submit <name of the production> <YAML file with workflow description> <execution mode>
Arguments:
   name of the production
   YAML file with the workflow description
   execution mode is optional:
     ps: submit the workflow to the Production System (default)
     wms: submit individual jobs to the WMS
     local: execute the workflow locally as individual jobs
     dry-run: get the list of files that will be processed by each transformation, without running the workflow
Example:
    cta-prod-submit TestProd production_config.yml
Example for local execution (for testing):
    cta-prod-submit TestProd production_config.yml local
"""

__RCSID__ = "$Id$"

from DIRAC.Core.Base.Script import Script

Script.parseCommandLine()

from CTADIRAC.ProductionSystem.Client.Utilities.production_utils import (
    check_and_sort_workflow_config,
    find_parent_prod_step,
    get_parents_list,
    instanciate_and_build_workflow_element,
)

import DIRAC
from ruamel.yaml import YAML

yaml = YAML(typ="safe", pure=True)
import json

from DIRAC.ProductionSystem.Client.ProductionClient import ProductionClient
from DIRAC.TransformationSystem.Client.TransformationClient import TransformationClient
from DIRAC.Interfaces.API.Dirac import Dirac
from DIRAC.Resources.Catalog.FileCatalog import FileCatalog
from CTADIRAC.Core.Utilities.tool_box import read_inputs_from_file


def dry_run(metaquery):
    fc = FileCatalog()
    result = fc.findFilesByMetadata(dict(metaquery))
    return result


def perform_dry_run(workflow_element, workflow_step, prod_name):
    if workflow_element.prod_step.Inputquery:
        res = dry_run(workflow_element.prod_step.Inputquery)
        if res["OK"]:
            print_dry_run_results(res, workflow_element, workflow_step, prod_name)
        else:
            DIRAC.gLogger.notice(
                f"\tStep {workflow_step['ID']} will not use existing files."
            )
    else:
        DIRAC.gLogger.notice(
            f"\tStep {workflow_step['ID']} will not process any file (no input query defined)."
        )


def print_dry_run_results(res, workflow_element, workflow_step, prod_name):
    if res["Value"]:
        files_list = res["Value"]
        print_files_to_process(files_list, workflow_element, workflow_step)
        filename = f"{prod_name}_Step{workflow_step['ID']}_input_files.list"
        with open(filename, "w") as ascii:
            for file in files_list:
                ascii.write(f"{file}\n")

        DIRAC.gLogger.notice(
            f"\nFull list of {len(files_list)} files dumped into {filename}"
        )

    else:
        DIRAC.gLogger.notice(
            f"\tStep {workflow_step['ID']} will not use existing files."
        )


def print_files_to_process(files_list, workflow_element, workflow_step):
    DIRAC.gLogger.notice(
        f"\tStep {workflow_step['ID']} will process files matching the following query :"
        f" \n{workflow_element.prod_step.Inputquery}"
    )
    if len(files_list) < 10:
        DIRAC.gLogger.notice(
            f"List of {len(files_list)} files to be processed by step {workflow_step['ID']}:"
        )
        for file in files_list:
            DIRAC.gLogger.notice(file)
    else:
        DIRAC.gLogger.notice(
            f"Example of 10 files to be processed by step {workflow_step['ID']}:"
        )
        for file in files_list[0:10]:
            DIRAC.gLogger.notice(file)


def submit_we_job(workflow_element, mode):
    res = Dirac().submitJob(workflow_element.job, mode=mode)
    if not res["OK"]:
        DIRAC.gLogger.error(res["Message"])
        DIRAC.exit(-1)
    DIRAC.gLogger.notice("\tSubmitted job:", res["Value"])


def build_workflow(workflow_config, prod_sys_client, prod_name, mode):
    """For each workflow step, build the associated workflow element composed of a job and a production step"""
    workflow_element_list = []
    check_and_sort_workflow_config(workflow_config)
    parents_list = get_parents_list(workflow_config["ProdSteps"])
    for workflow_step in workflow_config["ProdSteps"]:
        parent_prod_step = find_parent_prod_step(workflow_element_list, workflow_step)
        workflow_element = instanciate_and_build_workflow_element(
            workflow_step, workflow_config, parent_prod_step, parents_list, mode
        )
        prod_sys_client.addProductionStep(workflow_element.prod_step)
        workflow_element_list.append(workflow_element)

        # For dry-run mode : print the list of input files for each transformation
        if mode.lower() == "dry-run":
            perform_dry_run(workflow_element, workflow_step, prod_name)

        # For local and wms mode : build and submit the job in the same loop
        if mode.lower() in ["wms", "local"]:
            submit_we_job(workflow_element, mode)


def start_production(prod_sys_client, prod_name):
    # Get the production description
    prod_description = prod_sys_client.prodDescription
    # Create the production
    res = prod_sys_client.addProduction(prod_name, json.dumps(prod_description))
    if not res["OK"]:
        DIRAC.gLogger.error(res["Message"])
        DIRAC.exit(-1)

    # Start the production, i.e. instantiate the transformation steps
    res = prod_sys_client.startProduction(prod_name)

    if not res["OK"]:
        DIRAC.gLogger.error(res["Message"])
        DIRAC.exit(-1)
    DIRAC.gLogger.notice(f"\nProduction {prod_name} successfully created")


def print_submitted_transformations(prod_name, trans_list, trans_client):
    # Print the submitted transformations
    if not trans_list:
        DIRAC.gLogger.notice(
            f"No transformation associated with production {prod_name}"
        )
        DIRAC.exit(-1)
    for trans in trans_list:
        trans_id = trans["TransformationID"]
        trans_name = trans_client.getTransformationParameters(
            trans_id, "TransformationName"
        )["Value"]
        DIRAC.gLogger.notice(
            f"\tSubmitted transformation: {trans_name} with transID {trans_id}"
        )


def attach_files_to_transformation(job_config, trans_client, trans_list):
    trans0 = trans_list[0]["TransformationID"]
    DIRAC.gLogger.notice(
        "Using %d input files from test_input_data.list" % (job_config["input_limit"])
    )
    infile_list = read_inputs_from_file("test_input_data.list")
    res = trans_client.addFilesToTransformation(trans0, infile_list)  # Files added here
    if not res["OK"]:
        DIRAC.gLogger.error(res["Message"])
        DIRAC.exit(-1)
    else:
        DIRAC.gLogger.notice(
            "Successfully added %d files to transformation %s"
            % (job_config["input_limit"], trans0)
        )
        DIRAC.exit(0)


@Script()
def main():
    arguments = Script.getPositionalArgs()
    if len(arguments) not in list(range(2, 4)):
        Script.showHelp()

    # Read the arguments
    prod_name = arguments[0]
    workflow_config_file = arguments[1]
    mode = "ps"
    if len(arguments) == 3:
        mode = arguments[2]
    if mode not in ["ps", "wms", "local", "dry-run"]:
        Script.showHelp()

    with open(workflow_config_file) as stream:
        workflow_config = yaml.load(stream)

    if mode == "ps":
        for prod_step in workflow_config["ProdSteps"]:
            if "input_sandbox" in prod_step["job_config"]:
                DIRAC.gLogger.error("Not allowed input_sandbox key in production mode. Only available in wms mode")
                DIRAC.exit(-1)

    ##################################
    # Create the production
    DIRAC.gLogger.notice(f"\nBuilding new production: {prod_name}")
    prod_sys_client = ProductionClient()
    trans_client = TransformationClient()

    ##################################
    # Build production steps according to the workflow description
    build_workflow(workflow_config, prod_sys_client, prod_name, mode)
    ##################################

    # The default mode is ps, i.e. submit the worflow to the Production System
    if mode.lower() == "ps":
        start_production(prod_sys_client, prod_name)
        res = prod_sys_client.getProductionTransformations(prod_name)
        if res["OK"]:
            trans_list = res["Value"]
            print_submitted_transformations(prod_name, trans_list, trans_client)
        else:
            DIRAC.gLogger.error(res["Message"])
            DIRAC.exit(-1)

        # If input_limit is set attach testing files to the first transformation
        prod_step_0 = workflow_config["ProdSteps"][0]
        job_config = prod_step_0["job_config"]
        if "input_limit" in job_config:
            attach_files_to_transformation(job_config, trans_client, trans_list)


########################################################
if __name__ == "__main__":
    main()
