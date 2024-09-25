# Reflex-AI

`reflex-ai` is a package to bring AI agent capabilities to your local development environment.

## 1. Install the Package

Install the package with pip:

```bash
pip install reflex-ai
```

NOTE: `reflex-ai` requires `reflex` 0.6.0 or later. Before this is out, make sure to run the following:

```bash
pip install git+https://github.com/reflex-dev/reflex.git@main
pip uninstall watchfiles
```

## 2. Create a Reflex Project

`reflex-ai` works with both new and existing Reflex projects. To create a new project, create a directory for your app and run:

```bash
reflex init
```     

See the [reflex docs](https://github.com/reflex-dev/reflex) for more information on creating Reflex projects.

## 3. Enable AI

To enable AI in your project, add the following to your main app file.

```bash
# Import the reflex-ai package (you MUST import it exactly like this)
from reflex_ai import enable

app = rx.App()
# Enable AI BEFORE you call any `add_page`.
enable(app)

# Add your pages as usual.
app.add_page(index)
```

## 4. Run the App

Run your app as usual:

While we're in beta, you need to take the following steps:

Export the backend URL for the AI agent:
```
export FLEXGEN_BACKEND_URL=https://rxh-prod-flexgen-agent.fly.dev/
```

Install `

Then run your app as usual:

```bash
reflex run
```

NOTE: You must be logged in to Reflex to use `reflex-ai`.

## 5. Access the AI Editor at `/edit`

Every page in your app will have an additional route by adding `/edit` to the end of the URL. For example, if your index page is at `localhost:3000`, you can access the AI editor at `localhost:3000/edit`. Similarly, if your about page is at `localhost:3000/about`, you can access the AI editor at `localhost:3000/about/edit`.

When `reflex-ai` is enabled, a scratch copy of your app will be created in the `.web/reflex-ai-tmp` directory for the AI to make changes without affecting your main app.

## 6. Select and Edit Elements

On an edit page, you can select elements by clicking on them. The selected element will be highlighted in the editor and the toolbar will show the selected code.

You can enter prompts in the toolbar input to generate new content for the selected element. The AI will generate new content based on the prompt and update the element in the editor.

### Caveats