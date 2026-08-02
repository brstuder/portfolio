# MkDocs Formatting Demo

!!! info "Author's Note"

    The purpose of this document is to showcase miscellaneous MkDocs formatting functionality. You can see lots of functionality supported by MkDocs which is particularly useful for developer docs. While many WYSIWYG content editors and CMS tools provide much of this functionality out of the box, developer-built environments in repositories with static site generators will still write their content like this. Each tool or content type comes with an additional section for integrating it into your own MkDocs site. Some features may specifically require Material for MkDocs.

## Better Code Blocks

There are several additions to our code blocks we can make that improve their display and interactability.

### Color Coding

In order for code blocks to display with color-coded syntax, we must tell MkDocs what type of content is being to our code block. In this example, we're adding color coding to an example of Python code like:

```py
print("Hello, World!")
```

This is written by using the code or syntax shorthand in the top row of backticks that creates the code block:

````
```py
print("Hello, World!")
```
````

We use `py` as shorthand for Python, but this also supports `html`, `css`, `yaml`, `json`, and other formats we may need to display. We will continue to use this method throughout the article with different formats to better demonstrate.

### Copy to Clipboard

You'll notice in every code block on this page, we can select an icon in the top right to copy the code to our clipboard. To enable this sitewide, add this to your `mkdocs.yml`:

```yaml
theme:
  features:
    - content.code.copy
```

### Adding Titles to Code Blocks

We've made some great additions to our code blocks, but now suppose we want to add more context to our code blocks. This can be useful for labeling API payloads by their response code, for example:

```title="404: Not Found"
{
  "status": 404,
  "error": "Not Found",
  "message": "The requested resource was not found on this server.",
  "path": "/brett/fake-api"
}
```

A title can be added at the top of your code block by adding `title="Name of Code Block"`.

## Collapsible Tabs

??? "Here is a collapsible tab!"
    
    Here is an example of content that is hidden within an interactable tab.

Collapsible tabs are supported by MkDocs Material, a powerful MkDocs theme, by default. Collapsible tabs can be formatted in your article like:

``` title="Collapsible Tab Template"

??? "Here is a collapsible tab!"
    
    Here is an example of content that is hidden within an interactable tab.

```

Collapsible tabs are an example of MkDocs Material's extensive admonitions functionality. You can learn more about using admonitions in your MkDocs Material project by visiting their [documentation](https://squidfunk.github.io/mkdocs-material/reference/admonitions/).

## Better Tables

Through a very basic plugin and some CSS, tables can be a little more pleasing to the eye. Add the following into your `mkdocs.yml` file under `markdown_extensions`:

    ```yaml
    markdown_extensions:
        tables
    ```

This will create a clean layout for your tables, and highlight table rows when you hover over them with your cursor. From here, you can apply additional CSS to your tables to build a style that's cohesive with your brand or webpage.

### Example: Ingredients for Korean ground beef and rice recipe

| Ingredient | Amount |
|---|---|
| Ground beef | 1 lb |
| Garlic | 3 cloves |
| Brown sugar | 1/4 cup |
| Soy sauce | 1/4 cup |
| Sesame oil | 2 tsp |
| Ground ginger | 1/4 tsp |
| Red pepper flakes | 1/4 tsp |
| Pepper | 1/4 tsp |
| White rice | 2 cups |