from typing import Any, Dict, Union

from sqlalchemy.orm import Session

from morph.task.utils.connections.database.mysql import MysqlConnector
from morph.task.utils.connections.database.postgres import PostgresqlConnector
from morph.task.utils.connections.database.redshift import RedshiftConnector
from morph.task.utils.profile import (
    MysqlConnection,
    PostgresqlConnection,
    RedshiftConnection,
)


class DBConnector:
    """
    Database connector implements sqlalchemy connection to the database
    Available mysql, postgres, redshift connection
    @param connection: Connection object from `get_service_connection` method or dict params
    """

    def __init__(
        self,
        connection: Union[
            PostgresqlConnection, MysqlConnection, RedshiftConnection, Dict[str, Any]
        ],
    ):
        if isinstance(connection, dict):
            connection_type = connection.get("type")
            if connection_type == "mysql":
                connection = MysqlConnection(**connection)
            elif connection_type == "postgres":
                connection = PostgresqlConnection(**connection)
            elif connection_type == "redshift":
                connection = RedshiftConnection(**connection)
            else:
                raise ValueError(f"Invalid connection type: {connection_type}")
        self.connection = connection

    def execute_sql(self, sql: str) -> Any:
        """
        Execute sql query on the specified database
        """
        if isinstance(self.connection, PostgresqlConnection):
            pg_connection = PostgresqlConnector(
                self.connection,
                use_ssh=self.connection.ssh_host is not None
                and self.connection.ssh_host != "",
            )
            return pg_connection.execute_sql(sql)
        elif isinstance(self.connection, MysqlConnection):
            mysql_connection = MysqlConnector(
                self.connection,
                use_ssh=self.connection.ssh_host is not None
                and self.connection.ssh_host != "",
            )
            return mysql_connection.execute_sql(sql)
        elif isinstance(self.connection, RedshiftConnection):
            redshift_connection = RedshiftConnector(self.connection)
            return redshift_connection.execute_sql(sql)
        else:
            raise ValueError("Invalid connection type")

    def get_db_session(self) -> Session:
        """
        Get sqlalchemy session object
        """
        if isinstance(self.connection, PostgresqlConnection):
            pg_connection = PostgresqlConnector(
                self.connection,
                use_ssh=self.connection.ssh_host is not None
                and self.connection.ssh_host != "",
            )
            return pg_connection.get_session()
        elif isinstance(self.connection, MysqlConnection):
            mysql_connection = MysqlConnector(
                self.connection,
                use_ssh=self.connection.ssh_host is not None
                and self.connection.ssh_host != "",
            )
            return mysql_connection.get_session()
        elif isinstance(self.connection, RedshiftConnection):
            redshift_connection = RedshiftConnector(self.connection)
            return redshift_connection.get_session()
        else:
            raise ValueError("Invalid connection type")
