# Spec Kit Agent

The general agent has been updated to include a `spec` command to interact with `spec-kit`.

## `spec new <description>`

This command creates a new feature specification using `spec-kit`.

### Usage

```
spec new "your feature description here"
```

### Example

```
spec new "add a login page with username and password"
```

### Implementation Details

The `create_new_feature` function in `general_agent.py` implements the logic for this command. It follows the steps outlined in the `speckit.specify.toml` file to create a new feature.

### TODOs

The following parts of the `create_new_feature` function are not yet fully implemented:

- **Spec Content Generation**: The content of the specification is currently a placeholder. The logic to generate the full specification based on the user's description needs to be implemented.
- **Quality Validation**: The steps to validate the quality of the generated specification are not yet implemented.
