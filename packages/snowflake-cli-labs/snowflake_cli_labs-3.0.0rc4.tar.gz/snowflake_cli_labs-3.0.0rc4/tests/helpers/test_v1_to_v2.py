import logging
from pathlib import Path
from textwrap import dedent

import pytest
import yaml


def test_migration_already_v2(
    runner,
    project_directory,
):
    with project_directory("migration_already_v2"):
        result = runner.invoke(["helpers", "v1-to-v2"])

    assert result.exit_code == 0
    assert "Project definition is already at version 2." in result.output


def test_migrations_with_multiple_entities(
    runner, project_directory, os_agnostic_snapshot
):
    with project_directory("migration_multiple_entities"):
        result = runner.invoke(["helpers", "v1-to-v2"])
    assert result.exit_code == 0
    assert Path("snowflake.yml").read_text() == os_agnostic_snapshot
    assert Path("snowflake_V1.yml").read_text() == os_agnostic_snapshot


def test_migrations_with_all_app_entities(
    runner, project_directory, os_agnostic_snapshot
):
    with project_directory("migration_all_app_entities"):
        result = runner.invoke(["helpers", "v1-to-v2"])
    assert result.exit_code == 0
    assert Path("snowflake.yml").read_text() == os_agnostic_snapshot
    assert Path("snowflake_V1.yml").read_text() == os_agnostic_snapshot


def test_migration_native_app_missing_manifest(runner, project_directory):
    with project_directory("migration_multiple_entities") as project_dir:
        (project_dir / "app" / "manifest.yml").unlink()
        result = runner.invoke(["helpers", "v1-to-v2"])
    assert result.exit_code == 1
    assert "manifest.yml file not found" in result.output


def test_migration_native_app_no_artifacts(runner, project_directory):
    with project_directory("migration_multiple_entities") as project_dir:
        with (project_dir / "snowflake.yml").open("r+") as snowflake_yml:
            pdf = yaml.safe_load(snowflake_yml)
            pdf["native_app"]["artifacts"] = []
            snowflake_yml.seek(0)
            yaml.safe_dump(pdf, snowflake_yml)
            snowflake_yml.truncate()
        result = runner.invoke(["helpers", "v1-to-v2"])
    assert result.exit_code == 1
    assert "No artifacts mapping found in project definition" in result.output
    assert "Could not bundle Native App artifacts" in result.output


def test_migration_native_app_package_scripts(runner, project_directory):
    with project_directory("migration_package_scripts") as project_dir:
        result = runner.invoke(["helpers", "v1-to-v2"])
        assert result.exit_code == 0
        package_scripts_dir = project_dir / "package_scripts"
        for file in package_scripts_dir.iterdir():
            assert file.read_text() == dedent(
                """\
                -- Just a demo package script, won't actually be executed in tests
                select * from <% ctx.entities.pkg.identifier %>.my_schema.my_table
                """
            )


@pytest.mark.parametrize(
    "project_directory_name", ["snowpark_templated_v1", "streamlit_templated_v1"]
)
def test_if_template_is_not_rendered_during_migration_with_option_checked(
    runner, project_directory, project_directory_name, os_agnostic_snapshot, caplog
):
    with project_directory(project_directory_name):
        with caplog.at_level(logging.WARNING):
            result = runner.invoke(["helpers", "v1-to-v2", "--accept-templates"])

    assert result.exit_code == 0
    assert Path("snowflake.yml").read_text() == os_agnostic_snapshot
    assert Path("snowflake_V1.yml").read_text() == os_agnostic_snapshot
    assert (
        "Your V1 definition contains templates. We cannot guarantee the correctness of the migration."
        in caplog.text
    )


@pytest.mark.parametrize(
    "project_directory_name", ["snowpark_templated_v1", "streamlit_templated_v1"]
)
def test_if_template_raises_error_during_migrations(
    runner, project_directory, project_directory_name, os_agnostic_snapshot
):
    with project_directory(project_directory_name):
        result = runner.invoke(["helpers", "v1-to-v2"])
        assert result.exit_code == 1, result.output
        assert "Project definition contains templates" in result.output


def test_migration_with_only_envs(project_directory, runner):
    with project_directory("sql_templating"):
        result = runner.invoke(["helpers", "v1-to-v2"])

    assert result.exit_code == 0


@pytest.mark.parametrize(
    "duplicated_entity",
    [
        """
    - name: test
      handler: "test"
      signature: ""
      returns: string
      runtime: "3.10"
    """,
        """
streamlit:
  name: test
  stage: streamlit
  query_warehouse: test_warehouse
  main_file: "streamlit_app.py"
  title: "My Fancy Streamlit"
    """,
        """
    - name: test
      handler: "test"
      signature: ""
      returns: string
      handler: test
      runtime: "3.10"
    """,
    ],
)
def test_migrating_a_file_with_duplicated_keys_raises_an_error(
    runner, project_directory, os_agnostic_snapshot, duplicated_entity
):
    with project_directory("snowpark_procedures") as pd:
        definition_path = pd / "snowflake.yml"

        with open(definition_path, "a") as definition_file:
            definition_file.write(duplicated_entity)

        result = runner.invoke(["helpers", "v1-to-v2"])
    assert result.exit_code == 1, result.output
    assert result.output == os_agnostic_snapshot
