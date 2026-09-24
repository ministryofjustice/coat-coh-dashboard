import streamlit as st

def manual_file_upload():
    st.sidebar.header("Data input")
    uploaded_file = st.sidebar.file_uploader(
        "Upload AWS Cost Optimization Hub CSV export",
        type=["csv"],
    )

    sample_hint = st.sidebar.checkbox("Show expected columns", value=False)
    if sample_hint:
        st.sidebar.write(
            [
                "estimatedMonthlySavings",
                "accountId",
                "accountName",
                "region",
                "currentResourceType",
                "resourceId",
                "actionType",
                "currentResourceSummary",
                "recommendedResourceSummary",
                "estimatedMonthlyCost",
                "estimatedSavingsPercentage",
                "lastRefreshTimestamp",
                "recommendationId",
                "implementationEffort",
                "tags",
                "restartNeeded",
                "rollbackPossible",
                "recommendationLookbackPeriodInDays",
                "source",
                "currencyCode",
                "recommendedResourceType",
                "resourceArn",
            ]
        )

    if not uploaded_file:
        st.info("Upload your CSV file in the left sidebar to start.")
        st.stop()

    return uploaded_file