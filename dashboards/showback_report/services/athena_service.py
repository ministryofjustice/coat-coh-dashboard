import time
import boto3
import random

from config import ATHENA_REGION, ATHENA_OUTPUT_LOCATION, ATHENA_ROLE, ATHENA_WORKGROUP


class AthenaService:
    def __init__(self):
        self.workgroup = ATHENA_WORKGROUP

        credentials = boto3.client("sts", region_name=ATHENA_REGION).assume_role(
            RoleArn=ATHENA_ROLE,
            RoleSessionName=f"pod-athena-query-{random.randint(10 ** (5 - 1), (10**5) - 1)}",
        )["Credentials"]

        session = boto3.Session(
            aws_access_key_id=credentials["AccessKeyId"],
            aws_secret_access_key=credentials["SecretAccessKey"],
            aws_session_token=credentials["SessionToken"],
            region_name=ATHENA_REGION,
        )

        identity = session.client("sts").get_caller_identity()
        print(f"Assumed identity: {identity['Arn']}")

        user_id = identity["UserId"]
        self.output_location = ATHENA_OUTPUT_LOCATION + user_id + "/"

        self.client = session.client("athena")


    def start_query(self, database, query):
        response = self.client.start_query_execution(
            QueryString=query,
            QueryExecutionContext={"Database": database},
            ResultConfiguration={"OutputLocation": self.output_location},
            WorkGroup=self.workgroup
        )

        return response.get("QueryExecutionId", "")


    def wait_for_query(self, query_execution_id):
        while True:
            response = self.client.get_query_execution(QueryExecutionId=query_execution_id)

            state = response.get("QueryExecution", {}).get("Status", {}).get("State", "")

            if state == "SUCCEEDED":
                return
            elif state in ("FAILED", "CANCELLED"):
                reason = response.get("QueryExecution", {}).get("Status", {}).get("StateChangeReason", "")

                raise RuntimeError(f"Athena query {state}: {reason}")

            time.sleep(2)


    def get_results(self, query_execution_id):
        paginator = self.client.get_paginator("get_query_results")
        
        pages = paginator.paginate(
            QueryExecutionId=query_execution_id,
            PaginationConfig={"PageSize": 1000},
        )

        columns = []
        rows = []

        for page in pages:
            if columns == []:
                columns = [
                    column.get("Name", "") for column in page.get("ResultSet", {}).get("ResultSetMetadata", {}).get("ColumnInfo", [])
                ]

            for row in page.get("ResultSet", {}).get("Rows", []):
                values = [field.get("VarCharValue", "") for field in row.get("Data", [])]

                key_values = dict(zip(columns, values))

                rows.append(key_values)

        return rows[1:]


    def run_query(self, database, query):
        print(f"Running Athena query: {query}")
        
        query_execution_id = self.start_query(database, query)

        self.wait_for_query(query_execution_id)
        
        athena_response = self.get_results(query_execution_id)

        print("Query result:")
        
        for row in athena_response:
            print(row)

        return athena_response