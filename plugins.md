A ChatGPT plugin that requires a restful api with CORS, a documentation of the API in the OpenAPI yaml format, and a 
JSON plugin manifest file that will define relevant metadata for the plugin.

# Notes on building Plugins

## API
The API we will be building should wrap the etherscan API endpoints. Etherscan will need an API KEY, for now just create a `.env` file and I will put the key there afterwards

Use python to write the API


## Plugin Manifest
* Every plugin requires a ai-plugin.json file, which needs to be hosted on the API’s domain. For example, a company called example.com would make the plugin JSON file accessible via an https://example.com domain since that is where their API is hosted. When you install the plugin via the ChatGPT UI, on the backend we look for a file located at /.well-known/ai-plugin.json. The /.well-known folder is required and must exist on your domain in order for ChatGPT to connect with your plugin. If there is no file found, the plugin cannot be installed. For local development, you can use HTTP but if you are pointing to a remote server, HTTPS is required.

The minimal definition of the required ai-plugin.json file will look like the following:
```
{
    "schema_version": "v1",
    "name_for_human": "TODO Plugin",
    "name_for_model": "todo",
    "description_for_human": "Plugin for managing a TODO list. You can add, remove and view your TODOs.",
    "description_for_model": "Plugin for managing a TODO list. You can add, remove and view your TODOs.",
    "auth": {
        "type": "none"
    },
    "api": {
        "type": "openapi",
        "url": "http://localhost:3333/openapi.yaml",
        "is_user_authenticated": false
    },
    "logo_url": "http://localhost:3333/logo.png",
    "contact_email": "support@example.com",
    "legal_info_url": "http://www.example.com/legal"
}
```
## OpenAPI Definition

* The next step is to build the OpenAPI specification to document the API. The model in ChatGPT does not know anything about your API other than what is defined in the OpenAPI specification and manifest file. This means that if you have an extensive API, you need not expose all functionality to the model and can choose specific endpoints. For example, if you have a social media API, you might want to have the model access content from the site through a GET request but prevent the model from being able to comment on users posts in order to reduce the chance of spam.

The OpenAPI specification is the wrapper that sits on top of your API. A basic OpenAPI specification will look like the following:
```
openapi: 3.0.1
info:
  title: TODO Plugin
  description: A plugin that allows the user to create and manage a TODO list using ChatGPT.
  version: 'v1'
servers:
  - url: http://localhost:3333
paths:
  /todos:
    get:
      operationId: getTodos
      summary: Get the list of todos
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/getTodosResponse'
components:
  schemas:
    getTodosResponse:
      type: object
      properties:
        todos:
          type: array
          items:
            type: string
          description: The list of todos.
```

We start by defining the specification version, the title, description, and version number. When a query is run in ChatGPT, it will look at the description that is defined in the info section to determine if the plugin is relevant for the user query. You can read more about prompting in the writing descriptions section.

Keep in mind the following limits in your OpenAPI specification, which are subject to change:

200 characters max for each API endpoint description/summary field in API specification
200 characters max for each API param description field in API specification
Since we are running this example locally, we want to set the server to point to your localhost URL. The rest of the OpenAPI specification follows the traditional OpenAPI format, you can learn more about OpenAPI formatting through various online resources. There are also many tools that auto generate OpenAPI specifications based on your underlying API code.

## Running a plugin
Once you have created an API, manifest file, and OpenAPI specification for your API, you are now ready to connect the plugin via the ChatGPT UI.

Using a local version of your API running, you can point the plugin interface to your localhost server. To connect the plugin with ChatGPT, navigate to the plugin store and select “Develop your own plugin”. Enter your localhost and port number (e.g localhost:3333). Note that only auth type none is currently supported for localhost development.

## Other Notes
* Make sure to include a requirements.txt file for dependencies