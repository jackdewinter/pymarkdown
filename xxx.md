# xxx

## Base case

Very simple base cases.

### `test_tables_extension_198_enabled_x`

```python
    source_markdown = """| foo | bar |
| --- | --- |
| baz | bim |"""
```

## Basic Whitespace

Each of these should have a similar test in the LRD tests.

### `test_tables_extension_198_enabled_with_leading_same`

- test_whitespaces_lrd_with_spaces_before_same

```python
    source_markdown = """ | foo | bar |
 | --- | --- |
 | baz | bim |"""
```

### `test_tables_extension_198_enabled_with_leading_different`

- test_whitespaces_lrd_with_spaces_before_different

```python
    source_markdown = """ | foo | bar |
  | --- | --- |
| baz | bim |"""
```

### `test_whitespaces_tables_with_too_many_spaces_before`

- test_whitespaces_lrd_with_too_many_spaces_before

```python
    source_markdown = """    | foo | bar |
    | --- | --- |
    | baz | bim |"""
```

### `test_whitespaces_tables_with_too_many_spaces_before_after_first`

- test_whitespaces_lrd_with_too_many_spaces_before_after_first

```python
    source_markdown = """| foo | bar |
    | --- | --- |
    | baz | bim |"""
```

### `test_whitespaces_tables_with_increasing_spaces_before`

- test_link_reference_definitions_162
- unlike LRD test, tables have no text specifying that "unlimited" whitespace at start of newlines within the table are permitted

```python
    source_markdown = """   | foo | bar |\a
      | --- | --- |\a\a
           | baz | bim |\a\a
"""
```

### `test_whitespaces_tables_with_tabs_before_x`

- test_whitespaces_lrd_with_tabs_before_x

```python
    source_markdown = """\t| foo | bar |
\t| --- | --- |
\t| baz | bim |
"""
```

### `test_tables_extension_198_enabled_with_trailing_single`

- test_whitespaces_lrd_with_spaces_trailing_single

```python
    source_markdown = """| foo | bar |\a
| --- | --- |\a
| baz | bim |\a"""
```

### `test_tables_extension_198_enabled_with_trailing_double`

```python
    source_markdown = """| foo | bar |\a\a
| --- | --- |\a\a
| baz | bim |\a\a"""
```

### `test_tables_extension_198_enabled_with_trailing_triple`

```python
    source_markdown = """| foo | bar |\a\a\a
| --- | --- |\a\a\a
| baz | bim |\a\a\a"""
```

## Internal - Good Cases

These tests have no links to LRDs as these are internal to the table format itself.

### `test_tables_extension_198_enabled_with_empty_columns`

- table columns do not need to have content to be valid

```python
    source_markdown = """| foo | bar |
| --- | --- |
|||"""
```

### `test_tables_extension_198_enabled_with_internal_tabs`

- tabs can exist within table columns, with leading and trailing spaces/tabs treated as whitespace

```python
    source_markdown = """|\tfoo |\tbar |
|\t--- |\t--- |
|\tbaz |\tbim |"""
```

### `test_tables_extension_199_enabled`

- leading and trailing `|` characters are not required after the first line

```python
    source_markdown = """| abc | defghi |
:-: | -----------:
bar | baz"""
```

### `test_tables_extension_199_enabled_all_three`

- table columns do not need to have a consistent length

```python
    source_markdown = """| abc | defghi | jkl |
| :-: | -----------: | :--- |
| bar | baz | bam |"""
```

### `test_tables_extension_200_enabled`

- `\` can be used to escape a bar

```python
    source_markdown = """| f\\|oo  |
| ------ |
| b `\\|` az |
| b **\\|** im |"""
```

### `test_tables_extension_200_enabled_trailing_escaped_bar`

- even the final `|` can be escaped

```python
    source_markdown = """| f\\|oo  |
| ------ |
| b `\\|` az \\|
| b **\\|** im |"""
```

### `test_tables_extension_200_enabled_trailing_escaped_bar_2` - duplicate of `test_tables_extension_200_enabled_trailing_escaped_bar` ?

```python
    source_markdown = """| f\\|oo  |
| ------ |
| b `\\|` az \\|\a\a
| b **\\|** im |"""
```

### `test_tables_extension_200_enabled_only_escaped_bar`

- other variations on escaping parts of a table

```python
    source_markdown = """|\\||
| ------ |
|\\|
|\\||"""
```

### `test_tables_extension_200_enabled_a` - duplicate of `test_tables_extension_200_enabled_trailing_escaped_bar` ?

```python
    source_markdown = """| b `\\|` oo  |
| ------ |

b `\\|` oo

"""
```

### `test_tables_extension_200_enabled_b` - duplicate of `test_tables_extension_200_enabled_trailing_escaped_bar` ?

```python
    source_markdown = """| b `a\\|b` oo  |
| ------ |
| b `a\\|b` az |
"""
```

### `test_tables_extension_204_enabled`

- after first two rows, columns are inserted or omitted as needed

```python
    source_markdown = """| abc | def |
| --- | --- |
| bar |
| bar | baz | boo |"""
```

### `test_tables_extension_205_enabled`

- tables can exist without any "body" rows, in which case, they are not generated

```python
    source_markdown = """| abc | def |
| --- | --- |"""
```

## Internal - Bad Cases

These tests have no links to LRDs as these are internal to the table format itself.

### `test_tables_extension_199_enabled_bad_center`

- center must have 3 characters, `:-:`

```python
    source_markdown = """| abc | defghi | jkl |
| :: | -----------: | :--- |
| bar | baz | bam |"""
```

### `test_tables_extension_199_enabled_bad_right_length`

- right must have 2 characters, `-:`

```python
    source_markdown = """| abc | defghi | jkl |
| :-: | : | :--- |
| bar | baz | bam |"""
```

### `test_tables_extension_199_enabled_bad_right_character`

- right must have 2 characters, `-:`, any other character than whitespace (before and after), `-` and `:` on the outsides is illegal

```python
    source_markdown = """| abc | defghi | jkl |
| :-: | --; | :--- |
| bar | baz | bam |"""
```

### `test_tables_extension_199_enabled_bad_left_length`

- left must have 2 characters, `:-`

```python
    source_markdown = """| abc | defghi | jkl |
| :-: | ---: | : |
| bar | baz | bam |"""
```

### `test_tables_extension_199_enabled_bad_left_character`

- left must have 2 characters, `:-`, any other character than whitespace (before and after), `-` and `:` on the outsides is illegal

```python
    source_markdown = """| abc | defghi | jkl |
| :-: | ---: | ;--- |
| bar | baz | bam |"""
```

### `test_tables_extension_203_enabled`

- number of columns in first two rows must match

```python
    source_markdown = """| abc | def |
| --- |
| bar |"""
```

## Tables Stopped By Other Elements

Each of these should have a similar test in the Tables tests.

### `test_tables_extension_202_enabled` - blank

- test_link_reference_definitions_167

```python
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |
bar

bar"""
```

### Stopped by Paragraph

- see test_tables_extension_202_enabled
- test_link_reference_definitions_185x
- table definition eats up each new line to a blank line

### Stopped by SetExt

- see test_tables_extension_202_enabled
- see test_link_reference_definitions_184
- table definition eats up each new line to a blank line

### `test_tables_extension_201_enabled_ax` - atx

- test_link_reference_definitions_185ax

```python
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |
# bar"""
```

### `test_tables_extension_201_enabled_aa` - blank with atx, duplicate of `test_tables_extension_201_enabled_ax` ?

- stopped by blank + atx

```python
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |

# bar"""
```

### `test_tables_extension_201_enabled_ab` - atx with spaces, duplicate of `test_tables_extension_201_enabled_ax` ?

```python
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |
  # bar"""
```

### `test_tables_extension_201_enabled_bx` - tb

- test_whitespaces_lrd_with_spaces_followed_by_thematic

```python
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |
-----"""
```

### `test_tables_extension_201_enabled_ba` - blank with tb, duplicate of `test_tables_extension_201_enabled_bx` ?

```python
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |

-----"""
```

### `test_tables_extension_201_enabled_bb` - tb with spaces, duplicate of `test_tables_extension_201_enabled_bx` ?

```python
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |
  -----"""
```

### `test_tables_extension_201_enabled_cx` - icb

- test_link_reference_definitions_185c

```python
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |
    abc"""
```

### `test_tables_extension_201_enabled_ca` - duplicate of `test_tables_extension_201_enabled_cx` ?

```python
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |

    abc"""
```

### `test_tables_extension_201_enabled_dx` - fcb

- test_link_reference_definitions_185b

````python
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |
```python"""
````

### `test_tables_extension_201_enabled_da` - blank fcb - duplicate of `test_tables_extension_201_enabled_dx` ?

````python
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |

```python"""
````

### `test_tables_extension_201_enabled_db` - duplicate of `test_tables_extension_201_enabled_dx` ?

````python
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |
  ```python"""
````

### `test_tables_extension_201_enabled_ex` - html

- test_link_reference_definitions_185d

```python
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |
<!-- comment -->"""
```

### `test_tables_extension_201_enabled_ea` - block html - duplicate of `test_tables_extension_201_enabled_ex` ?

```python
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |

<!-- comment -->"""
```

### `test_tables_extension_201_enabled_eb` - duplicate of `test_tables_extension_201_enabled_ex` ?

```python
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |
   <!-- comment -->"""
```

### `test_tables_extension_201_enabled_fx` - lrd

- test_whitespaces_lrd_with_spaces_followed_by_lrd

```python
    source_markdown = """| abc | def |
| --- | --- |
| bar | [baz] |
[baz]: /url"""
```

### `test_tables_extension_201_enabled_fa` - block lrd - duplicate of `test_tables_extension_201_enabled_fx` ?

```python
    source_markdown = """| abc | def |
| --- | --- |
| bar | [baz] |

[baz]: /url"""
```

### `test_tables_extension_201_enabled_fb` - duplicate of `test_tables_extension_201_enabled_fx` ?

```python
    source_markdown = """| abc | def |
| --- | --- |
| bar | [baz] |
  [baz]: /url"""
```

### Stopped by Table

- test_whitespaces_lrd_with_spaces_followed_by_table
- table definition eats up each new line to a blank line
- having two tables, one after the another without any elements separating them results in a single table

### `test_tables_extension_201_enabled_x` - bq

- test_link_reference_definitions_185e

```python
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |
> bar"""
```

### `test_tables_extension_201_enabled_xa` - duplicate of `test_tables_extension_201_enabled_x` ?

- stopped by blank + bq

```python
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |

> bar"""
```

### `test_tables_extension_201_enabled_xb` - duplicate of `test_tables_extension_201_enabled_x` ?

```python
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |
  > bar"""
```

### `test_tables_extension_201_enabled_gx` - ol

- test_link_reference_definitions_185gx

```python
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |
1. bar"""
```

### `test_tables_extension_201_enabled_ga` - blank ol - duplicate of `test_tables_extension_201_enabled_gx` ?

- stopped by blank + ol

```python
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |

1. bar"""
```

### `test_tables_extension_201_enabled_gb` - duplicate of `test_tables_extension_201_enabled_gx` ?

```python
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |
  1. bar"""
```

### `test_tables_extension_201_enabled_hx` - ul

- test_link_reference_definitions_185fx

```python
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |
- bar"""
```

### `test_tables_extension_201_enabled_ha` - duplicate of `test_tables_extension_201_enabled_hx` ?

```python
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |

- bar"""
```

## Tables with elements before

### `test_whitespaces_tables_with_paragraph_before` - para

- test_link_reference_definitions_182

```python
    source_markdown = """this is a paragraph
| foo | bar |
| --- | --- |
| baz | bim |
"""
```

### `test_whitespaces_tables_with_atx_before` - atx

- test_link_reference_definitions_183x

```python
    source_markdown = """# this is a heading
| foo | bar |
| --- | --- |
| baz | bim |
"""
```

### `test_whitespaces_tables_with_thematic_before` - tb

- test_link_reference_definitions_183a

```python
    source_markdown = """# this is a heading
| foo | bar |
| --- | --- |
| baz | bim |
"""
```

### `test_whitespaces_tables_with_setext_before` - setext

- test_link_reference_definitions_183b

```python
    source_markdown = """abcde
=====
| foo | bar |
| --- | --- |
| baz | bim |
"""
```

### `test_whitespaces_tables_with_indented_code_block_before` - icb

- test_link_reference_definitions_183c

```python
    source_markdown = """abcde
=====
| foo | bar |
| --- | --- |
| baz | bim |
"""
```

### `test_whitespaces_tables_with_fenced_code_block_before` - fcb

- test_link_reference_definitions_183d

````python
    source_markdown = """```text
this is indented code
```
| foo | bar |
| --- | --- |
| baz | bim |
"""
````

### `test_whitespaces_tables_with_html_block_before` - html

- test_link_reference_definitions_183e

````python
    source_markdown = """<script>
<~-- javascript comment -->
</script>
| foo | bar |
| --- | --- |
| baz | bim |
"""
````

### `test_whitespaces_tables_with_block_quote_before_with_blank_in_bq` - bq

- test_link_reference_definitions_183fa

````python
    source_markdown = """> this is a block quote
>
| foo | bar |
| --- | --- |
| baz | bim |
"""
````

### `test_whitespaces_tables_with_block_quote_before_with_only_blank_in_bq` - bq

- test_link_reference_definitions_183fb

````python
    source_markdown = """>
| foo | bar |
| --- | --- |
| baz | bim |
"""
````

### `test_whitespaces_tables_with_block_quote_before_with_no_blank_in_bq` - bq

- test_link_reference_definitions_183fx

````python
    source_markdown = """> this is a block quote
| foo | bar |
| --- | --- |
| baz | bim |
"""
````

### `test_whitespaces_tables_with_unordered_list_before_with_blank_in_list` - ul

- test_link_reference_definitions_183gxb

````python
    source_markdown = """- this is a block quote

| foo | bar |
| --- | --- |
| baz | bim |
"""
````

### `test_whitespaces_tables_with_unordered_before_with_only_blank_in_list` - ul

- test_link_reference_definitions_183gxa

````python
    source_markdown = """-
| foo | bar |
| --- | --- |
| baz | bim |
"""
````

### `test_whitespaces_tables_with_unordered_before_with_no_blank_in_list` - ul

- test_link_reference_definitions_183gxx

````python
    source_markdown = """- this is a block quote
| foo | bar |
| --- | --- |
| baz | bim |
"""
````

### `test_whitespaces_tables_with_ordered_list_before_with_blank_in_list` - ol

- test_link_reference_definitions_183gxc

````python
    source_markdown = """- this is a block quote

| foo | bar |
| --- | --- |
| baz | bim |
"""
````

### `test_whitespaces_tables_with_ordered_before_with_only_blank_in_list` - ol

- test_link_reference_definitions_183gxe

````python
    source_markdown = """-
| foo | bar |
| --- | --- |
| baz | bim |
"""
````

### `test_whitespaces_tables_with_ordered_before_with_no_blank_in_list` - ol

- test_link_reference_definitions_183gxd

````python
    source_markdown = """- this is a block quote
| foo | bar |
| --- | --- |
| baz | bim |
"""
````

## Within Single UL

### `test_whitespaces_tables_extension_with_spaces_within_ulist` - ul para blank nm

- test_whitespaces_lrd_with_spaces_within_ulist_leading_para_x

```python
    source_markdown = """+ abc
  | foo | bar |
  | --- | --- |
  | baz | bim |"""
```

### `test_whitespaces_tables_extension_with_spaces_extra_within_ulist`

- test_whitespaces_lrd_with_spaces_extra_within_ulist_leading_para

```python
    source_markdown = """+ abc
    | foo | bar |
    | --- | --- |
    | baz | bim |"""
```

## ---- Up to here ----

## XX

### `test_whitespaces_tables_extension_with_spaces_before_within_ulist`

```python
    source_markdown = """+ abc
  | foo | bar |
  | --- | --- |
  | baz | bim |"""
```

### `test_whitespaces_tables_extension_with_spaces_extra_before_within_ulist`

```python
    source_markdown = """+ abc
    | foo | bar |
    | --- | --- |
    | baz | bim |"""
```

### `test_whitespaces_tables_extension_with_spaces_before_within_olist`

```python
    source_markdown = """1. | foo | bar |
   | --- | --- |
   | baz | bim |"""
```

### `test_whitespaces_tables_extension_with_spaces_extra_before_within_olist`

```python
    source_markdown = """1. abc
    | foo | bar |
    | --- | --- |
    | baz | bim |"""
```

### `test_whitespaces_tables_extension_with_spaces_within_block_quote`

```python
    source_markdown = """> abc
> | foo | bar |
> | --- | --- |
"""
```

### `test_whitespaces_tables_extension_with_spaces_extra_within_block_quote`

```python
    source_markdown = """> abc
>  | foo | bar |
>  | --- | --- |
"""
```

### `test_whitespaces_tables_extension_with_spaces_after_block_quote`

```python
    source_markdown = """> abc
> def
  | foo | bar |
  | --- | --- |
"""
```

### `test_whitespaces_tables_extension_with_some_spaces_after_double_block_quotes`

```python
    source_markdown = """> > abc
> > def
  | foo | bar |
  | --- | --- |
"""
```

### `test_whitespaces_tables_extension_with_extra_spaces_after_double_block_quotes`

```python
    source_markdown = """> > abc
> > def
    | foo | bar |
    | --- | --- |
"""
```

### `test_whitespaces_tables_extension_with_spaces_within_single_block_quote_after_double_block_quote`

```python
    source_markdown = """> abc
> > def
>   | foo | bar |
>   | --- | --- |
"""
```

### `test_tables_extension_extra_in_block`

```python
    source_markdown = """> | foo | bar |
> | --- | --- |
> | baz | bim |"""
```

### `test_tables_extension_extra_in_block_in_block_after_first_line`

```python
    source_markdown = """> | foo | bar |
>> | --- | --- |
>> | baz | bim |"""
```

### `test_tables_extension_extra_in_block_in_block_after_first_line_xx`

```python
    source_markdown = """> | --- | --- |
> | baz | bim |"""
```

### `test_tables_extension_extra_in_block_in_block_after_first_line_xa`

```python
    source_markdown = """>> | --- | --- |
>> | baz | bim |"""
```

### `test_tables_extension_extra_in_block_in_block_after_first_line_xb`

```python
    source_markdown = """> | abc | def |
> | -:- | -:- |"""
```

### `test_tables_extension_extra_in_block_in_block_after_first_line_xc`

```python
    source_markdown = """>> | foo | bar |
> | --- | --- |
> | baz | bim |"""
```

### `test_tables_extension_extra_in_block_in_block_after_first_line_xd`

```python
    source_markdown = """> | foo | bar |
>> | --- | --- |
>> | baz | bim |"""
```

### `test_tables_extension_extra_in_block_in_block_after_first_line_xe`

```python
    source_markdown = """> abc
> def
> | foo | bar |
>> | --- | --- |
>> | baz | bim |"""
```

### `test_whitespaces_tables_extension_with_spaces_within_olist`

```python
    source_markdown = """1. | foo | bar |
   | --- | --- |
   | baz | bim |"""
```

### `test_whitespaces_tables_extension_with_spaces_extra_within_olist`

```python
    source_markdown = """1. abc
    | foo | bar |
    | --- | --- |
    | baz | bim |"""
```

### `test_tables_extension_extra_in_block_in_block_xx`

```python
    source_markdown = """>> | foo | bar |
> | --- | --- |
> | baz | bim |"""
```

### `test_tables_extension_extra_in_block_in_block_xa`

```python
    source_markdown = """>>> | foo | bar |
> | --- | --- |
> | baz | bim |"""
```

### `test_tables_extension_extra_in_list_header_line_only`

```python
    source_markdown = """- | foo | bar |
- some text
some other text
"""
```

### `test_tables_extension_extra_in_block_quote_header_line_only_x`

```python
    source_markdown = """> | foo | bar |
>
> some text
> some other text
"""
```

### `test_tables_extension_extra_in_block_quote_header_line_only_a`

```python
    source_markdown = """> | foo | bar |
>
> some text
> some other text
"""
```

### `test_tables_extension_extra_in_list_header_line_only_with_separator_in_seperate_list_item`

```python
    source_markdown = """- | foo | bar |
- | --- | --- |
- some text
some other text
"""
```

### `test_tables_extension_extra_in_list_header_and_separator_only`

```python
    source_markdown = """- | foo | bar |
  | --- | --- |
- some text
some other text
"""
```

### `test_tables_extension_extra_in_list_header_and_separator_only_lrd_in_next_list_item`

```python
    source_markdown = """- | foo | bar |
  | --- | --- |
- [foo]: /url
- [foo]
"""
```

### `test_tables_extension_extra_in_list_header_and_separator_only_lrd_in_previous_list_item`

```python
    source_markdown = """- [foo]: /url
- | foo | bar |
  | --- | --- |
- [foo]
```

### `test_tables_extension_extra_in_list_followed_by_new_line_and_atx`

```python
    source_markdown = """- | foo | bar |
  | -- | -- |
  | baz | bim |

  # bac
"""
```

### `test_tables_extension_extra_in_block_quote_followed_by_new_line_and_atx`

```python
    source_markdown = """> | foo | bar |
> | -- | -- |
> | baz | bim |
>
> # bac
```

### `test_tables_extension_extra_in_list_header_only_after_text_and_new_line`

```python
    source_markdown = """- abc

  | foo | bar |
"""
```

### `test_tables_extension_extra_in_block_quote_header_only_after_text_and_new_line`

```python
    source_markdown = """> abc
>
> | foo | bar |
"""
```

### `test_tables_extension_extra_in_list_after_paragraph`

```python
    source_markdown = """+ this is text
  | foo | bar |
  | --- | --- |
  | foo | bar |
"""
```

### `test_tables_extension_extra_in_block_quote_after_paragraph`

```python
    source_markdown = """> this is text
> | foo | bar |
> | --- | --- |
> | foo | bar |
"""
```

### `test_tables_extension_extra_in_list_after_atx`

```python
    source_markdown = """+ # Heading
  | foo | bar |
  | --- | --- |
  | foo | bar |
"""
```

### `test_tables_extension_extra_in_block_quote_after_atx`

```python
    source_markdown = """> # Heading
> | foo | bar |
> | --- | --- |
> | foo | bar |
"""
```

### `test_tables_extension_extra_in_list_followed_atx`

```python
    source_markdown = """+ | foo | bar |
  | --- | --- |
  | foo | bar |
  # Heading
"""
```

### `test_tables_extension_extra_in_block_quote_followed_atx`

```python
    source_markdown = """> | foo | bar |
> | --- | --- |
> | foo | bar |
> # Heading
"""
```

### `test_tables_extension_extra_in_list_after_thematic`

```python
    source_markdown = """+ ----
  | foo | bar |
  | --- | --- |
  | foo | bar |
"""
```

### `test_tables_extension_extra_in_block_quote_after_thematic`

```python
    source_markdown = """> ----
> | foo | bar |
> | --- | --- |
> | foo | bar |
"""
```

### `test_tables_extension_extra_in_list_followed_thematic`

```python
    source_markdown = """+ | foo | bar |
  | --- | --- |
  | foo | bar |
  ----
"""
```

### `test_tables_extension_extra_in_block_quote_followed_thematic`

```python
    source_markdown = """> | foo | bar |
> | --- | --- |
> | foo | bar |
> ----
"""
```

### `test_tables_extension_extra_in_list_after_indented_block`

```python
    source_markdown = """-     indented
      code block
  | foo | bar |
  | --- | --- |
  | foo | bar |
"""
```

### `test_tables_extension_extra_in_block_quote_after_indented_block`

```python
    source_markdown = """>     indented
>     code block
> | foo | bar |
> | --- | --- |
> | foo | bar |
"""
```

### `test_tables_extension_extra_in_list_followed_indented_block`

```python
    source_markdown = """+ | foo | bar |
  | --- | --- |
  | foo | bar |
      indented
      code block
"""
```

### `test_tables_extension_extra_in_block_quote_followed_indented_block`

```python
    source_markdown = """> | foo | bar |
> | --- | --- |
> | foo | bar |
>     indented
>     code block
"""
```

### `test_tables_extension_extra_in_list_after_fenced_block`

````python
    source_markdown = """+ ```sh
  echo foo
  ```
  | foo | bar |
  | --- | --- |
  | foo | bar |
"""
````

### `test_tables_extension_extra_in_block_quote_after_fenced_block`

````python
    source_markdown = """> ```sh
> echo foo
> ```
> | foo | bar |
> | --- | --- |
> | foo | bar |
"""
````

### `test_tables_extension_extra_in_list_followed_fenced_block`

````python
    source_markdown = """+ | foo | bar |
  | --- | --- |
  | foo | bar |
  ```sh
  echo foo
  ```
"""
````

### `test_tables_extension_extra_in_block_quote_followed_fenced_block`

````python
    source_markdown = """> | foo | bar |
> | --- | --- |
> | foo | bar |
> ```sh
> echo foo
> ```
"""
````

### `test_tables_extension_extra_in_list_after_html_block`

```python
    source_markdown = """+ <!-- comment -->
  | foo | bar |
  | --- | --- |
  | foo | bar |
"""
```

### `test_tables_extension_extra_in_block_quote_after_html_block`

```python
    source_markdown = """> <!-- comment -->
> | foo | bar |
> | --- | --- |
> | foo | bar |
"""
```

### `test_tables_extension_extra_in_list_followed_html_block`

```python
    source_markdown = """+ | foo | bar |
  | --- | --- |
  | foo | bar |
  <!-- comment -->
"""
```

### `test_tables_extension_extra_in_block_quote_followed_html_block`

```python
    source_markdown = """> | foo | bar |
> | --- | --- |
> | foo | bar |
> <!-- comment -->
"""
```

### `test_tables_extension_extra_in_list_after_lrd`

```python
    source_markdown = """+ [boo]: /url
  | foo | bar |
  | --- | --- |
  | foo | bar |

  [boo]
"""
```

### `test_tables_extension_extra_in_block_quote_after_lrd`

```python
    source_markdown = """> [boo]: /url
> | foo | bar |
> | --- | --- |
> | foo | bar |
>
> [boo]
"""
```

### `test_tables_extension_extra_in_block_quote_after_lrd_a`

```python
    source_markdown = """> abc
>
> [boo]: /url
> | foo | bar |
> | --- | --- |
> | foo | bar |
>
> [boo]
"""
```

### `test_tables_extension_extra_in_list_followed_lrd`

```python
    source_markdown = """+ [boo]
  | foo | bar |
  | --- | --- |
  | foo | bar |
  [boo]: /url
"""
```

### `test_tables_extension_extra_in_block_quote_followed_lrd`

```python
    source_markdown = """> [boo](/url)
> | foo | bar |
> | --- | --- |
> | foo | bar |
> [boo]: /url
"""
```

### `test_tables_extension_extra_in_list_chxb`

```python
    source_markdown = """>\a
> | foo | bar |
> | --- | --- |
> | foo | bar |
>
> [boo](/url)
"""
```

### `test_tables_extension_extra_in_list_cha`

```python
    source_markdown = """> [boo]
> | foo | bar |
> | --- | --- |
> | foo | bar |
>
> [boo]: /url
"""
```

### `test_tables_extension_extra_in_block_chb`

```python
    source_markdown = """> | foo | bar |
> | --- | --- |
> | foo | bar |
> [boo](/url)
>
> [boo](/url)
"""
```

### `test_whitespaces_tables_with_tabs_before_within_unordered_list_x`

```python
    source_markdown = """- abc
\t| foo | bar |
\t| --- | --- |
\t| baz | bim |

"""
```

### `test_whitespaces_tables_with_tabs_before_within_unordered_list_and_single_space`

```python
    source_markdown = """- abc
 \t| foo | bar |
 \t| --- | --- |
 \t| baz | bim |

"""
```

### `test_whitespaces_tables_with_tabs_before_within_unordered_list_and_spaces`

```python
    source_markdown = """- abc
  \t| foo | bar |
  \t| --- | --- |
  \t| baz | bim |

"""
```

### `test_whitespaces_tables_with_tabs_before_within_unordered_double_list`

```python
    source_markdown = """- abc
  - def
\t| foo | bar |
\t| --- | --- |
\t| baz | bim |
"""
```

### `test_whitespaces_tables_with_tabs_before_within_ordered_list_x`

```python
    source_markdown = """1. abc
\t| foo | bar |
\t| --- | --- |
\t| baz | bim |
"""
```

### `test_whitespaces_tables_with_tabs_before_within_ordered_list_and_single_space`

```python
    source_markdown = """1. abc
 \t| foo | bar |
 \t| --- | --- |
 \t| baz | bim |
"""
```

### `test_whitespaces_tables_with_tabs_before_within_ordered_list_and_spaces`

```python
    source_markdown = """1. abc
  \t| foo | bar |
  \t| --- | --- |
  \t| baz | bim |
"""
```

### `test_whitespaces_tables_with_tabs_before_within_ordered_double_list_x`

```python
    source_markdown = """1. abc
   1. def
\t  | foo | bar |
\t  | --- | --- |
\t  | baz | bim |
"""
```

### `test_whitespaces_tables_with_tabs_before_within_ordered_double_list_no_spaces`

```python
    source_markdown = """1. abc
   1. def
\t| foo | bar |
\t| --- | --- |
\t| baz | bim |
"""
```

### `test_whitespaces_tables_with_tabs_before_within_ordered_double_list_tab_after_indent`

```python
    source_markdown = """1. abc
   1. def
   \t| foo | bar |
   \t| --- | --- |
   \t| baz | bim |
"""
```

### `test_whitespaces_tables_with_tabs_before_within_ordered_double_list_one_space`

```python
    source_markdown = """1. abc
   1. def
\t | foo | bar |
\t | --- | --- |
\t | baz | bim |
"""
```

### `test_whitespaces_tables_with_tabs_before_within_ordered_double_list_two_spaces`

```python
    source_markdown = """1. abc
   1. def
\t  | foo | bar |
\t  | --- | --- |
\t  | baz | bim |
"""
```

### `test_whitespaces_tables_with_tabs_before_within_block_quotes_x1`

```python
    source_markdown = """> abc
> def
\t| foo | bar |
\t| --- | --- |
\t| baz | bim |
"""
```

### `test_whitespaces_tables_with_tabs_before_within_block_quotes_x2`

```python
    source_markdown = """> abc
> def
  \t| foo | bar |
  \t| --- | --- |
  \t| baz | bim |
"""
```

### `test_whitespaces_tables_with_tabs_before_within_block_quotes_repeat`

```python
    source_markdown = """> abc
> def
>\t| foo | bar |
>\t| --- | --- |
>\t| baz | bim |

"""
```

### `test_whitespaces_tables_with_tabs_before_within_block_quotes_bare_repeat`

```python
    source_markdown = """>\t| foo | bar |
>\t| --- | --- |
>\t| baz | bim |

"""
```

### `test_whitespaces_tables_with_tabs_before_within_block_quotes_bare_with_many_tabs`

```python
    source_markdown = """>\t|\tfoo\t|\tbar\t|
>\t|\t---\t|\t---\t|
>\t|\tbaz\t|\tbim\t|"""
```

### `test_whitespaces_tables_with_tabs_before_within_block_quotes_bare_with_space_repeat_1a`

```python
    source_markdown = """> \t| foo | bar |
> \t| --- | --- |
> \t| baz | bim |

"""
```

### `test_whitespaces_tables_with_tabs_before_within_double_block_quotes`

```python
    source_markdown = """> abc
> > def
\t| foo | bar |
\t| --- | --- |
\t| baz | bim |
"""
```

### `test_whitespaces_tables_with_tabs_before_within_double_block_quotes_with_single_x`

```python
    source_markdown = """> abc
> > def
>\t| foo | bar |
>\t| --- | --- |
>\t| baz | bim |
"""
```

### `test_whitespaces_tables_with_tabs_before_within_double_block_quotes_with_single_a`

```python
    source_markdown = """> abc
> > def
>\t# heading
"""
```

### `test_whitespaces_tables_with_tabs_before_within_list_single_over_two_lines_b`

```python
    source_markdown = """- abc
  - def

  \t| foo | bar |
  \t| --- | --- |
  \t| baz | bim |

[fred]"""
```
