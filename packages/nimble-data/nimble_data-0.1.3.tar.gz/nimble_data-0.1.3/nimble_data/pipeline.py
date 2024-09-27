import requests


HEADERS = {
    "Content-Type": "application/json",
    "Authorization": 'Basic YWNjb3VudC1zdXBwb3J0LXBpcGVsaW5lLW5pbWJsZWRhdGE6MHUwU2VzMHcwRzky',
}


# A sample implementation of Nimble SDK
# Starting with Pipeline module - pull data from Amazon PDP, PLP, and reviews

class Pipeline:
    def __init__(self, pipeline_name):
        self.pipeline_name = pipeline_name
        if pipeline_name == "amazon_product":
            self.pipeline_url = "https://api.webit.live/api/v1/realtime/ecommerce/amazon/product"
        elif pipeline_name == "amazon_search":
            self.pipeline_url = "https://api.webit.live/api/v1/realtime/ecommerce/amazon/search"
        elif pipeline_name == "amazon_reviews":
            self.pipeline_url = "https://api.webit.live/api/v1/realtime/ecommerce/amazon/reviews"
        else:
            raise ValueError("Invalid pipeline name. Only 'amazon_product', 'amazon_search', and 'amazon_reviews' are supported.")

    def pull(self, input_data):
        if not isinstance(input_data, str):
            raise ValueError("Input data must be a string.")
        # determine the data key based on pipline name. amazon_product -> asin, amazon_search -> query, amazon_reviews -> asin
        data_key = "asin" if self.pipeline_name == "amazon_product" or self.pipeline_name == "amazon_reviews" else "query"
        req_data = {data_key: input_data}
        response = requests.post(self.pipeline_url, headers=HEADERS, json=req_data)
        if not response.ok:
            raise ValueError(f"Failed to pull data from the pipeline. Status code: {response.status_code}, error message: {response.text}")
        json_resp = response.json()
        parsed_data = json_resp.get("parsing")
        return parsed_data
