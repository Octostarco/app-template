import csv
from io import StringIO
import streamlit as st
from typing import Any
import os

from octostar.client import dev_mode
from streamlit_octostar_utils.octostar.client import impersonating_running_user
from streamlit_octostar_utils.style.common import hide_streamlit_header
from octostar_streamlit.components import os_contextmenu, os_dropzone
from octostar_streamlit.core.components.params import (
    OsContextMenuParams,
    OsDropzoneParams,
)
from octostar_streamlit.core.desktop.params import (
    OpenParams,
    SearchResultsParams,
)
from octostar_streamlit.core.entities import Entity, WorkspaceIdHost
from octostar_streamlit.core.extras.params import CreateLinkChartParams
from octostar_streamlit.desktop import (
    get_open_workspace_ids,
    close_workspace,
    get_active_workspace,
    open as desktop_open,
    get_search_results,
)
from octostar_streamlit.extras import create_link_chart
from octostar.utils.ontology import query_ontology


st.header("This is a streamlit app")
st.subheader("Connected to the Octostar")


def set_state(key: str, value: Any):
    if "state" not in st.session_state:
        st.session_state["state"] = {}
    st.session_state["state"][key] = value


def get_state(key: str):
    if "state" in st.session_state and key in st.session_state["state"]:
        return st.session_state["state"][key]
    return None


@impersonating_running_user()
@dev_mode(os.environ.get("OS_DEV_MODE"))
def initialize(client):
    # Any initialization of the session state can go here
    st.session_state["initialized"] = True


@impersonating_running_user()
@dev_mode(os.environ.get("OS_DEV_MODE"))
def loop(client):
    hide_streamlit_header()

    records = os_dropzone(
        key="dropzone-1",
        params=OsDropzoneParams(label="Drag/drop records here or click to select"),
    )
    if records is not None:
        st.header("Records")
        for item in records:
            os_contextmenu(
                params=OsContextMenuParams(
                    item=item, label=f"{item['entity_label']} ({item['entity_type']})"
                )
            )

    os_contextmenu(
        params=OsContextMenuParams(
            item={"entity_type": "person", "entity_id": "123"},
            label="Context Menu Here!",
        )
    )

    query = st.text_area(
        "Search",
        """
        select count(*) from dtimbr.person where entity_label like '%Robert%'
        """,
    )

    if st.button("Run Query"):
        set_state(key="query", value=query_ontology.sync(query, client=client))

    query_state = get_state(key="query")
    if query_state is not None:
        st.header("Query Result")
        st.json(query_state, expanded=True)

    chartdata = st.text_area(
        "New Link Chart Data",
        """
    node|Giovanni|person|Giovanni
    node|Robert|person|Robert
    node|Simone|person|Simone
    node|Octostar Research|company|Octostar Research
    node|Investigation Software|product|Investigation Software
    node|Investricor|company|Investricor
    node|John|person|John
    edge|Giovanni|Octostar Research|owns
    edge|Robert|Octostar Research|works for
    edge|Simone|Octostar Research|works for
    edge|John|Investricor|works for
    edge|Investricor|Octostar Research|invests in
    edge|Octostar Research|Investigation Software|develops

        """,
    )

    if get_state("linkchart1") == "pending" or (
        chartdata and st.button("Create Link Chart")
    ):
        column_names = ["type", "entity_id", "entity_type", "entity_label"]

        csv_reader = csv.DictReader(
            StringIO(chartdata), delimiter="|", fieldnames=column_names
        )

        nodes = [
            Entity(**{key: value for key, value in row.items() if key != "type"})
            for row in csv_reader
            if row["type"] == "node"
        ]

        column_names = ["type", "from", "to", "label"]
        csv_reader = csv.DictReader(
            StringIO(chartdata), delimiter="|", fieldnames=column_names
        )
        edges = [
            {key: value for key, value in row.items() if key != "type"}
            for row in csv_reader
            if row["type"] == "edge"
        ]

        chart = create_link_chart(
            CreateLinkChartParams(
                name="Octostar Research",
                draft=True,
                path="linkcharts",
                nodes=nodes,
                edges=edges,
            ),
            key="linkchart1",
        )
        set_state(key="linkchart1", value=chart if chart is not None else "pending")

    linkchart1 = get_state(key="linkchart1")
    if linkchart1 is not None and linkchart1 != "pending":
        desktop_open(OpenParams(records=Entity(**linkchart1)))
        st.header("Link Chart")
        st.json(linkchart1, expanded=True)

    value = get_search_results(
        params=SearchResultsParams(
            q="Giovanni", enableSelection=True, label="Search Giovanni"
        )
    )
    if value is not None:
        for ele in value:
            st.write(ele.to_dict())

    st.header("About the Desktop")
    current_workspace_id = get_active_workspace()
    open_workspaces = get_open_workspace_ids()
    st.write(f"Current workspace id: {current_workspace_id}")

    if open_workspaces is not None:
        st.header("Open Workspaces (ids)")
        st.subheader("See what can happen, with the right permissions")
        cols = st.columns((1, 1))
        fields = ["uid", "action"]
        for col, field_name in zip(cols, fields):
            col.write(f"**{field_name}**")

        for ws in open_workspaces:
            col1, col2 = st.columns((1, 1))
            with col1:
                os_contextmenu(
                    params=OsContextMenuParams(
                        item={"entity_type": "os_workspace", "entity_id": ws}, label=ws
                    )
                )

            if col2.button(
                label="Remove from Desktop",
                key=f"del-{ws}",
                disabled=ws == current_workspace_id,
            ):
                close_workspace(WorkspaceIdHost(id=ws))

    else:
        st.write("No open workspaces found")


if not st.session_state.get("initialized"):
    initialize()
if st.session_state.get("initialized"):
    loop()
