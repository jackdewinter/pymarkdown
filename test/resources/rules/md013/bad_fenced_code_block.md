```Python
def next_line(self, context, line):
    """
    Event that a new line is being processed.
    """
    if self.__leaf_token_index + 1 < len(self.__leaf_tokens) and self.__line_index == self.__leaf_tokens[self.__leaf_token_index + 1].line_number:
        self.__leaf_token_index+=1
```
