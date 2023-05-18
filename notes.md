Issues with Plugin Generator
* sometimes it gets the file structure wrong 
  we fix this by specifying the file structure more concretely

* sometimes it get the dependencies wrong
  we will try making sure it doesn't use specific versions that don't exists

* frequently there is a divergence between the openapi.yaml spec and the actual
routes defined in app.py
  a possible fix is generate the openapi.yaml first, then generate app.py from the routes?

* operationId in openapi.yaml is required and should be mentioned in prompt

Last commit Working: 957ec8f42f090cb95bb32321ada02642d645a0ce

Next Steps
* Create a template for all plugins that just require: `app name` & `description`
* In the future use web scraper to automatically fill out `description` based on scraped API docs