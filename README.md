# RecipeRadar Quantity Parser

The RecipeRadar Quantity Parser takes a set of free-text quantity descriptions, and extracts magnitude and unit information from them.

This functionality is provided to the [crawler](https://codeberg.org/openculinary/crawler) service so that it can extract additional data from each recipe crawled.

## Install dependencies

Make sure to follow the RecipeRadar [infrastructure](https://codeberg.org/openculinary/infrastructure) setup to ensure all cluster dependencies are available in your environment.

## Development

To install development tools and run linting and tests locally, execute the following commands:

```sh
$ make lint tests
```

## Local Deployment

To deploy the service to the local infrastructure environment, execute the following commands:

```sh
$ make
$ make deploy
```
