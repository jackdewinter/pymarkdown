diff

- original did not detect atx inside of list or block quote, this does
- original did not take setext into account, if para is setext this does not fire
- original fired even if line had the start of an inline token, this doesnt