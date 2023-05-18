the app is: A ChatGPT plugin that requires a restful api with CORS, a documentation of the API in the OpenAPI yaml format, and a JSON plugin manifest file that will define relevant metadata for the plugin.

the files we have decided to generate are: /.well-known/ai-plugin.json, app.py, openapi.yaml, requirements.txt

Shared dependencies:
1. API_KEY (in .env file)
2. ai-plugin.json fields: schema_version, name_for_human, name_for_model, description_for_human, description_for_model, auth, api, logo_url, contact_email, legal_info_url
3. openapi.yaml fields: specification version, title, description, version number, server URL, API endpoint descriptions/summaries, API param descriptions
4. Python dependencies in requirements.txt