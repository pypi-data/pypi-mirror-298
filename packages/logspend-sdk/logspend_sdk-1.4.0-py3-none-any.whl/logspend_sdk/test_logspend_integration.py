import pytest
from logspend_sdk.core import LogBuilder, LogSpendLogger
from logspend_sdk.constants import Provider

@pytest.mark.integration
def test_logspend_sdk_sends_data_successfully():
    # Setup logger and builder with real API key and project ID
    logger = LogSpendLogger(api_key="lk_live.Cddh6aPsoxF1mVf6Ib3mM", project_id="c7e632b7-253e-4741-a4fe-e32b522ca5d6")
    builder = LogBuilder({
        "provider": Provider.OPENAI.value,
        "model": "gpt-3.5-turbo-instruct",
        "prompt": "Say this is a test",
        # ... other input attributes ...
    })
    builder.set_output({
        "id": "chatcmpl-123",
        # ... other output attributes ...
    })
    builder.set_custom_properties({
        "user_id": "123455",
        # ... other custom properties ...
    })

    # Send the data
    response = logger.send(builder.build())

    # Assert that response is as expected (depends on the actual response structure from the API)
    assert response is not None
    # assert 'request_id' in response  # or any other key that indicates success

# Command to run the test with pytest
# pytest -v -m integration