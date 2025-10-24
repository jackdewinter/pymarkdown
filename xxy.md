# xxx

## Base Cases

Very simple base cases.

### `test_link_reference_definitions_161`

```python
    source_markdown = """[foo]: /url "title"

[foo]"""
```

### `test_link_reference_definitions_188x`

- gfm

```python
    source_markdown = """[foo]: /url"""
```

## Basic Whitespace

Each of these should have a similar test in the Tables tests.

### `test_link_reference_definitions_162` - link space nl spaces url spaces nl spaces title spaces nl para link

- test_whitespaces_tables_with_increasing_spaces_before

```python
    source_markdown = """   [foo]:\a
      /url\a\a
           'the title'\a\a

[foo]"""
```

### `test_whitespaces_lrd_with_spaces_before_same` - space link nl space url nl space title bl link

- test_tables_extension_198_enabled_with_leading_same

```python
    source_markdown = """ [fred]:
 /url
 "title"

[fred]"""
```

### `test_whitespaces_lrd_with_spaces_before_different` - space link nl url nl spaces title bl para link

- test_tables_extension_198_enabled_with_leading_different

```python
    source_markdown = """ [fred]:
/url
   "title"

[fred]"""
```

### `test_whitespaces_lrd_with_too_many_spaces_before` - para link nl icb (link-url)

- not an LRD as the link exists in a para
- test_whitespaces_tables_with_too_many_spaces_before

```python
    source_markdown = """[fred]
    [fred]: /url"""
```

### `test_whitespaces_lrd_with_too_many_spaces_before_after_first` - ?? test_link_reference_definitions_162

- too many whitespaces not a problem for LRDs, once started
- test_whitespaces_tables_with_too_many_spaces_before_after_first

```python
    source_markdown = """[fred]:
    /url
    'title'
[fred]"""
```

### `test_whitespaces_lrd_with_spaces_before_x` - ?? test_whitespaces_lrd_with_spaces_before_same

```python
    source_markdown = """   [fred]: /url
[fred]"""
```

### `test_whitespaces_lrd_with_spaces_trailing_single` - link space nl url space nl title space bl para link

- test_tables_extension_198_enabled_with_trailing_single

```python
    source_markdown = """[fred]:\a
/url\a
"title"\a

[fred]"""
```

### `test_whitespaces_lrd_with_spaces_trailing_double` - ?? test_whitespaces_lrd_with_spaces_trailing_single

- test_tables_extension_198_enabled_with_trailing_double

```python
    source_markdown = """[fred]:\a\a
/url\a\a
"title"\a\a

[fred]"""
```

### `test_whitespaces_lrd_with_spaces_trailing_triple` - ?? test_whitespaces_lrd_with_spaces_trailing_single

- test_tables_extension_198_enabled_with_trailing_triple

```python
    source_markdown = """[fred]:\a\a\a
/url\a\a\a
"title"\a\a\a

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_x` - tab link-url nl para link

- tab before makes it an icb
- test_whitespaces_tables_with_tabs_before_x

```python
    source_markdown = """\t[fred]: /url
[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_repeat` - ?? test_whitespaces_lrd_with_tabs_before_x

```python
    source_markdown = """\t[abc]: /url
\t[def]: /url
[abc]
[def]"""
```

### `test_whitespaces_lrd_with_form_feeds_before` - ff link-url nl para link - nm

```python
    source_markdown = """\u000c[fred]: /url
[fred]"""
```

## Internal - Good Cases

These tests have no links to Tables as these are internal to the LRD format itself.

### `test_link_reference_definitions_163`

- crazy stuff still counts towards a valid LRD

```python
    source_markdown = """[Foo*bar\\]]:my_(url) 'title (with parens)'

[Foo*bar\\]]"""
```

### `test_link_reference_definitions_164`

- can be on multiple lines

```python
    source_markdown = """[Foo bar]:
<my url>
'title'

[Foo bar]"""
```

### `test_link_reference_definitions_165`

- the title itself may extend over multiple lines

```python
    source_markdown = """[foo]: /url '
title
line1
line2
'

[foo]"""
```

### `test_link_reference_definitions_169`

- an empty link destination url is okay

```python
    source_markdown = """[foo]: <>

[foo]"""
```

### `test_link_reference_definitions_171`

- url and title can contain backslashes

```python
    source_markdown = """[foo]: /url\\bar\\*baz "foo\\"bar\\baz"

[foo]"""
```

### `test_link_reference_definitions_172`

- order of link and LRD is not important

```python
    source_markdown = """[foo]

[foo]: url"""
```

### `test_link_reference_definitions_173`

- last one wins

```python
    source_markdown = """[foo]

[foo]: first
[foo]: second"""
```

### `test_link_reference_definitions_174`

- link casing not important

```python
    source_markdown = """[FOO]: /url

[Foo]"""
```

### `test_link_reference_definitions_175`

- link casing not important

```python
    source_markdown = """[ΑΓΩ]: /φου

[αγω]"""
```

### `test_link_reference_definitions_176`

- LRDs do not require links

```python
    source_markdown = """[foo]: /url"""
```

### `test_link_reference_definitions_177`

- LRDs do not require links

```python
    source_markdown = """[
foo
]: /url
bar"""
```

### `test_link_reference_definitions_179`

- because of the text after the title, and that it is on a separate line, the first line ONLY is an LRD

```python
    source_markdown = """[foo]: /url
"title" ok"""
```

### `test_whitespaces_lrd_with_spaces_before_label`

- spaces before label are folded

```python
    source_markdown = """[  fred]: /url
[ fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_label`

- tabs before label are folded

```python
    source_markdown = """[\t\tfred]: /url
[ fred]"""
```

### `test_whitespaces_lrd_with_form_feeds_before_label`

- form feeds before label are folded

```python
    source_markdown = """[\u000cfred]: /url
[ fred]"""
```

### `test_whitespaces_lrd_with_spaces_after_label`

- spaces after label are folded

```python
    source_markdown = """[fred  ]: /url
[fred ]"""
```

### `test_whitespaces_lrd_with_tabs_after_label`

- tabs after label are folded

```python
    source_markdown = """[fred\t\t]: /url
[fred ]"""
```

### `test_whitespaces_lrd_with_form_feeds_after_label`

- form feeds after label are folded

```python
    source_markdown = """[fred\u000c]: /url
[fred ]"""
```

### `test_whitespaces_lrd_with_spaces_in_label`

- spaces in label are folded

```python
    source_markdown = """[fred  boy]: /url
[fred boy]"""
```

### `test_whitespaces_lrd_with_tabs_in_label`

- tabs in label are folded

```python
    source_markdown = """[fred\t\tboy]: /url
[fred boy]"""
```

### `test_whitespaces_lrd_with_form_feeds_in_label`

- form feeds in label are folded

```python
    source_markdown = """[fred\u000c\u000cboy]: /url
[fred boy]"""
```

### `test_whitespaces_lrd_with_spaces_before_destination`

- spaces between link start and url are captured

```python
    source_markdown = """[fred]:  /url
[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_destination`

- tabs between link start and url are captured

```python
    source_markdown = """[fred]:\t/url
[fred]"""
```

### `test_whitespaces_lrd_with_form_feeds_before_destination`

- form feeds between link start and url are captured

```python
    source_markdown = """[fred]:\u000c/url
[fred]"""
```

### `test_whitespaces_lrd_with_spaces_after_destination`

- spaces after the destination are captured as part of the LRD

```python
    source_markdown = """[fred]: /url\a\a
[fred]"""
```

### `test_whitespaces_lrd_with_tabs_after_destination`

- tabs after the destination are captured as part of the LRD

```python
    source_markdown = """[fred]: /url\t\t
[fred]"""
```

### `test_whitespaces_lrd_with_form_feeds_after_destination`

- form feeds after the destination are captured as part of the LRD

```python
    source_markdown = """[fred]: /url\u000c\u000c
[fred]"""
```

### `test_whitespaces_lrd_with_spaces_before_title`

- spaces before title are captured

```python
    source_markdown = """[fred]: /url "title"
[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_title`

- tabs before title are captured

```python
    source_markdown = """[fred]: /url\t"title"
[fred]"""
```

### `test_whitespaces_lrd_with_form_feeds_before_title`

- form feeds before title are captured

```python
    source_markdown = """[fred]: /url\u000c"title"
[fred]"""
```

### `test_whitespaces_lrd_with_spaces_after_title`

- spaces after the title are captured as part of the LRD

```python
    source_markdown = """[fred]: /url "title"\a\a\a
[fred]"""
```

### `test_whitespaces_lrd_with_tabs_after_title`

- tabs after the title are captured as part of the LRD

```python
    source_markdown = """[fred]: /url "title"\t\t
[fred]"""
```

### `test_whitespaces_lrd_with_form_feeds_after_title`

- form feeds after the title are captured as part of the LRD

```python
    source_markdown = """[fred]: /url "title"\t\t
[fred]"""
```

### `test_link_reference_definitions_186`

- LRDs without blank lines to separate

```python
    source_markdown = """[foo]: /foo-url "foo"
[bar]: /bar-url
  "bar"
[baz]: /baz-url

[foo],
[bar],
[baz]"""
```

## Internal - Bad Cases

These tests have no links to Tables as these are internal to the LRD format itself.

### `test_link_reference_definitions_165a`

- blank lines break the LRD

```python
    source_markdown = """[foo

bar]: /url 'title'

[foo\n\nbar]"""
```

### `test_link_reference_definitions_166`

- title cannot have blank line

```python
    source_markdown = """[foo]: /url 'title

with blank line'

[foo]"""
```

### `test_link_reference_definitions_166a`

- title has to end with same start character... blank line stops it

```python
    source_markdown = """[foo]: /url 'title
with blank line

[foo]"""
```

### `test_link_reference_definitions_166b`

- title has to end with same start character... blank line stops it

```python
    source_markdown = """[foo]: /url
'title
with blank line

[foo]"""
```

### `test_link_reference_definitions_168`

- url may not be omitted.

```python
    source_markdown = """[foo]:

[foo]"""
```

### `test_link_reference_definitions_170`

- must be space between url and title

```python
    source_markdown = """[foo]: <bar>(baz)

[foo]"""
```

### `test_link_reference_definitions_178`

- not an LRD as characters after title

```python
    source_markdown = """[foo]: /url "title" ok"""
```

### `test_link_reference_definitions_180`

- preceeded by 4 spaces, this is "LRD" type text within an ICB

```python
    source_markdown = """    [foo]: /url "title"

[foo]"""
```

### `test_link_reference_definitions_181`

- "LRD" like inside of FCB

````python
    source_markdown = """```
[foo]: /url
```

[foo]"""
````

### `test_link_reference_definitions_183ga` --- ????

```python
    source_markdown = """- A simple list
foo]: /url
> [Foo]"""
```

### `test_link_reference_definitions_188a`

- only start character

```python
    source_markdown = """["""
```

### `test_link_reference_definitions_188b`

- only start character and start of link text

```python
    source_markdown = """[foo"""
```

### `test_link_reference_definitions_188c`

- looks like link, no trailing `:`

```python
    source_markdown = """[foo]"""
```

### `test_link_reference_definitions_188d`

- no following url

```python
    source_markdown = """[foo]:"""
```

### `test_link_reference_definitions_188e`

- start of title without termination

```python
    source_markdown = """[foo]: /url ("""
```

## LRDs Stopped/Followed By Other Elements

Each of these should have a similar test in the Tables tests.

### `test_link_reference_definitions_167` - blank

- test_tables_extension_202_enabled

```python
    source_markdown = """[foo]:
/url

[foo]"""
```

### `test_link_reference_definitions_185x` - para

- test_tables_extension_202_enabled

```python
    source_markdown = """[foo]: /url
===
[foo]"""
```

### `test_link_reference_definitions_184` - setext

- test_tables_extension_202_enabled

```python
    source_markdown = """[foo]: /url
bar
===
[foo]"""
```

### `test_whitespaces_lrd_with_spaces_followed_by_thematic` - tb

- test_tables_extension_201_enabled_bx

```python
    source_markdown = """[fred]: /url1
---
[fred]
"""
```

### `test_link_reference_definitions_185ax` - atx

- test_tables_extension_201_enabled_ax

```python
    source_markdown = """[foo]: /url
# Abc
[foo]"""
```

### `test_link_reference_definitions_185aa` - atx with incomplete title - special case

```python
    source_markdown = """[foo]: /url
'start of
# Abc
[foo]"""
```

### `test_link_reference_definitions_185b` - fcb

- test_tables_extension_201_enabled_dx

````python
    source_markdown = """[foo]: /url
```text
my text
```
[foo]"""
````

### `test_link_reference_definitions_185c` - icb

- test_tables_extension_201_enabled_cx

```python
    source_markdown = """[foo]: /url
    my text
[foo]"""
```

### `test_link_reference_definitions_185d` - html

- test_tables_extension_201_enabled_ex

```python
    source_markdown = """[foo]: /url
<script>
<~-- javascript comment -->
</script>
[foo]"""
```

### `test_whitespaces_lrd_with_spaces_followed_by_lrd` - lrd

- test_tables_extension_201_enabled_fx

```python
    source_markdown = """[fred]: /url1
[barney]: /url2
[fred]
[barney]
"""
```

### `test_link_reference_definitions_extra_03b` - lrd (partial) - special case

- May seem like 2 LRD starts, but the second LRD start itself qualifies as a link destination https://github.github.com/gfm/#link-destination

```python
    source_markdown = """[foo]:
[foo]:
# abc"""
```

### `test_whitespaces_lrd_with_spaces_followed_by_table` - table

- see "stopped by table" under "Tables Stopped By Other Elements" in other document

```python
    source_markdown = """[fred]: /url1
| abc | def |
|-----|-----|
| ghi | jkl |
[fred]
"""
```

### `test_link_reference_definitions_185e` - bq

- test_tables_extension_201_enabled_x

```python
    source_markdown = """[foo]: /url
> This is a simple block quote
[foo]"""
```

### `test_link_reference_definitions_185fx` - ul

- test_tables_extension_201_enabled_hx

```python
    source_markdown = """[foo]: /url
- This is a simple list
[foo]"""
```

### `test_link_reference_definitions_185fa` - ul - ?? test_link_reference_definitions_185fx

```python
    source_markdown = """[foo]: /url
- This is a simple list
![foo]"""
```

### `test_link_reference_definitions_185gx` - ol

- test_tables_extension_201_enabled_gx

```python
    source_markdown = """[foo]: /url
1. This is a simple list
   [foo]"""
```

## LRDs with elements before

### `test_link_reference_definitions_182` - para

- test_whitespaces_tables_with_paragraph_before
- NOT an LRD, as LRDs cannot interupt a paragraph

```python
    source_markdown = """Foo
[bar]: /baz

[bar]"""
```

### `test_link_reference_definitions_183x` - atx

- test_whitespaces_tables_with_atx_before

```python
    source_markdown = """# [Foo]
[foo]: /url
> bar"""
```

### `test_link_reference_definitions_183a` - tb

- test_whitespaces_tables_with_thematic_before

```python
    source_markdown = """---
[foo]: /url
> [Foo]"""
```

### `test_link_reference_definitions_183b` - setext

- test_whitespaces_tables_with_setext_before

```python
    source_markdown = """abc
---
[foo]: /url
> [Foo]"""
```

### `test_link_reference_definitions_183c` - icb

- test_whitespaces_tables_with_indented_code_block_before

```python
    source_markdown = """    this is indented code
| foo | bar |
| --- | --- |
| baz | bim |
"""
```

### `test_link_reference_definitions_183d` - fcb

- test_whitespaces_tables_with_fenced_code_block_before

````python
    source_markdown = """```text
indented code block
```
[foo]: /url
> [Foo]"""
````

### `test_link_reference_definitions_183e` - html

- test_whitespaces_tables_with_html_block_before

```python
    source_markdown = """<script>
<~-- javascript comment -->
</script>
[foo]: /url
> [Foo]"""
```

### `test_link_reference_definitions_183fx` - bq

- test_whitespaces_tables_with_block_quote_before_with_no_blank_in_bq

```python
    source_markdown = """> A simple block quote
[foo]: /url
> [Foo]"""
```

### `test_link_reference_definitions_183fa` - bq

- test_whitespaces_tables_with_block_quote_before_with_blank_in_bq

```python
    source_markdown = """> this is a block quote
>
[foo]: /url
> [Foo]"""
```

### `test_link_reference_definitions_183fb` - bq

- test_whitespaces_tables_with_block_quote_before_with_only_blank_in_bq

```python
    source_markdown = """>
[foo]: /url
> [Foo]"""
```

### `test_link_reference_definitions_183gxx` - ul

- NOT an LRD, list contents is a paragraph, and LRDs do not interupt paragraphs
- test_whitespaces_tables_with_unordered_before_with_no_blank_in_list

```python
    source_markdown = """- A simple list
[foo]: /url
> [Foo]"""
```

### `test_link_reference_definitions_183gxa` - ul

- test_whitespaces_tables_with_unordered_before_with_only_blank_in_list

```python
    source_markdown = """-
[foo]: /url
> [Foo]"""
```

### `test_link_reference_definitions_183gxb` - ul

- test_whitespaces_tables_with_unordered_list_before_with_blank_in_list

```python
    source_markdown = """- this is a block quote

[foo]: /url
> [Foo]"""
```

### `test_link_reference_definitions_183gxc` - ol

- test_whitespaces_tables_with_ordered_list_before_with_blank_in_list

```python
    source_markdown = """1. this is a block quote

[foo]: /url
> [Foo]"""
```

### `test_link_reference_definitions_183gxd` - ol

- test_whitespaces_tables_with_ordered_before_with_no_blank_in_list

```python
    source_markdown = """1. this is a block quote
[foo]: /url
> [Foo]"""
```

### `test_link_reference_definitions_183gxe` - ol

- test_whitespaces_tables_with_ordered_before_with_only_blank_in_list

```python
    source_markdown = """1.
[foo]: /url
> [Foo]"""
```

### `test_link_reference_definitions_183gb` - ????? test_link_reference_definitions_183gxx

- still not an LRD

```python
    source_markdown = """- A simple list
 [foo]: /url
> [Foo]"""
```

### `test_link_reference_definitions_183gc` - ????? test_link_reference_definitions_183gxd

- still not an LRD

```python
    source_markdown = """1. A simple list
 [foo]: /url
> [Foo]"""
```

### `test_link_reference_definitions_183gg` - ????? test_link_reference_definitions_183gxx

- still not an LRD

```python
    source_markdown = """- A simple list
[foo]: /url
  > [Foo]"""
```

## Within Single UL

### `test_whitespaces_lrd_with_spaces_within_ulist_x` - ul link-url - nm

- test_link_reference_definitions_extra_06a

```python
    source_markdown = """- [fred]: /url
[fred]"""
```

### `test_link_reference_definitions_extra_01ce` - ul link nl indent url - nm

- test_link_reference_definitions_extra_06b

```python
    source_markdown = """- [foo]:
  /url"""
```

### `test_link_reference_definitions_extra_01cn` - ul link nl indent url - nm

- this is not an LRD, as it is split across two list items
- test_link_reference_definitions_extra_01d

```python
    source_markdown = """- [foo]:
- /url"""
```

### `test_whitespaces_lrd_with_spaces_within_ulist_a` - ul link-url-title - nm

- test_link_reference_definitions_extra_06c

```python
    source_markdown = """- [fred]: /url 'abc'
[fred]"""
```

### `test_link_reference_definitions_extra_01cf` - ul link nl indent url nl indent title - nm

- test_link_reference_definitions_extra_06d

```python
    source_markdown = """- [foo]:
  /url
  'title'"""
```

### `test_link_reference_definitions_extra_01cj` - ul link-url nl no-indent link-url - nm

- a pair of LRDs, one in list 1 and one in list 2
- test_link_reference_definitions_extra_06e

```python
    source_markdown = """- [foo]: /url
[foo2]: /url2"""
```

### `test_link_reference_definitions_extra_01ck` - ul link-url nl bq link-url - nm

- a pair of LRDs, one in list 1 and one in list 2
- test_link_reference_definitions_extra_06f

```python
    source_markdown = """- [foo]: /url
> [foo2]: /url2"""
```

### `test_link_reference_definitions_extra_01cl` - ul link-url nl ol link-url - nm

- a pair of LRDs, one in list 1 and one in list 2
- test_link_reference_definitions_extra_06g

```python
    source_markdown = """- [foo]: /url
1. [foo2]: /url2"""
```

### `test_link_reference_definitions_extra_01cm` - ul link-url nl ol link-url - nm

- a pair of LRDs, one in list 1 and one in list 2
- test_link_reference_definitions_extra_06h

```python
    source_markdown = """- [foo]: /url
- [foo2]: /url2"""
```

### `test_whitespaces_lrd_with_spaces_within_ulist_leading_para_x` - ul para blank link-url

- para, blank line, then properly indented LRD
- test_whitespaces_tables_extension_with_spaces_within_ulist
- test_whitespaces_lrd_with_spaces_within_olist

```python
    source_markdown = """- abc

  [fred]: /url
[fred]"""
```

### `test_whitespaces_lrd_with_spaces_extra_within_ulist_leading_para`  - ul para blank extra-sp link-url ?? test_whitespaces_lrd_with_spaces_within_ulist_leading_para_x

- para, blank line, then extra indented LRD
- test_whitespaces_tables_extension_with_spaces_extra_within_ulist

```python
    source_markdown = """- abc

    [fred]: /url
[fred]"""
```

### `test_whitespaces_lrd_with_spaces_within_ulist_leading_para_a` - ul para nl indent link-url - nm

- not an LRD due to leading paragraph
- test_whitespaces_lrd_with_spaces_before_within_olist

```python
    source_markdown = """- abc
  [fred]: /url
[fred]"""
```

### `test_link_reference_definitions_183gd` - ?? test_whitespaces_lrd_with_spaces_within_ulist_leading_para_a

- still not an LRD

```python
    source_markdown = """- A simple list
    [foo]: /url
> [Foo]"""
```

### `test_link_reference_definitions_extra_04a` - ?? test_whitespaces_lrd_with_spaces_within_ulist_leading_para_a

```python
    source_markdown = """- [foo]:
  [foo]:
  # abc"""
```

### `test_whitespaces_lrd_with_spaces_within_ulist_leading_para_b` - ul blank link-url - nm

- test_link_reference_definitions_extra_06j

```python
    source_markdown = """-
  [fred]: /url
[fred]"""
```

### `test_whitespaces_lrd_with_spaces_within_ulist_leading_para_split_two_lines_x` - ul link nl indent url - nm

- LRD split over 2 lines with enough space to keep it in the list
- test_link_reference_definitions_extra_06k

```Python
    source_markdown = """- [foo]:
  /url"""
```

### `test_whitespaces_lrd_with_spaces_within_ulist_leading_para_split_two_lines_minus_all_spaces` - ul link nl no-indent url - nm

- NOT A LRD, as the second line does not have enough spaces to keep it in the list
- test_link_reference_definitions_extra_06l

```Python
    source_markdown = """- [foo]:
/url"""
```

### `test_whitespaces_lrd_with_spaces_within_ulist_leading_para_split_two_lines_minus_some_spaces` - ?? test_whitespaces_lrd_with_spaces_within_ulist_leading_para_split_two_lines_minus_all_spaces

- NOT A LRD, as the second line does not have enough spaces to keep it in the list

```Python
    source_markdown = """- [foo]:
 /url"""
```

### `test_link_reference_definitions_extra_01cd` - ul link-url ul title - nm

- an LRD, but only the link and url, not the title
- test_link_reference_definitions_extra_06m

```python
    source_markdown = """- [foo]: /url
  - 'abc'"""
```

### `test_link_reference_definitions_extra_01cg` - ul link-url ul link-url - nm

- a pair of LRDs, one in list 1 and one in list 2
- test_link_reference_definitions_extra_06n

```python
    source_markdown = """- [foo]: /url
  - [foo2]: /url2"""
```

### `test_link_reference_definitions_extra_01ca` - ul para li link-url - nm

- test_link_reference_definitions_extra_06p

```python
    source_markdown = """- abc
- [foo]: /url"""
```

### `test_link_reference_definitions_extra_01cc` - ul link-url li para - nm

- test_link_reference_definitions_extra_06q

```python
    source_markdown = """- [foo]: /url
- abc"""
```

### `test_link_reference_definitions_extra_01cb` - ul link-url li para-with-apos - nm - ??? test_link_reference_definitions_extra_01cc

```python
    source_markdown = """- [foo]: /url
- 'abc'"""
```

### `test_link_reference_definitions_extra_01ch` - ul link-url li link-url - nm

- a pair of LRDs, one in list 1 and one in list 2
- test_link_reference_definitions_extra_06r

```python
    source_markdown = """- [foo]: /url
- [foo2]: /url2"""
```

### `test_whitespaces_lrd_with_formfeeds_before_within_list_x` - ul para nl space-ff link-uri bl link - nm?

```python
    source_markdown = """- abc
 \u000C \u000C[fred]: /url

[fred]"""
```

### `test_whitespaces_lrd_with_formfeeds_before_within_list_a` - ul para bl para space-ff link-uri bl link - nm?

```python
    source_markdown = """- abc

 \u000C \u000C[fred]: /url

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_unordered_list_x` - ul para nl tab link-url bl link - nm

- not an LRD because of leading para
- test_whitespaces_lrd_with_tabs_before_within_ordered_list_x

```python
    source_markdown = """- abc
\t[fred]: /url

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_unordered_list_single_over_two_lines_x` - ul para bl tab link tab nl spaces url bl link - nm

- a LRD because leading para broken by bl
- test_whitespaces_lrd_with_tabs_before_within_ordered_list_single_over_two_lines_x

```python
    source_markdown = """- abc

\t[fred]:\t
  /url

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_unordered_list_and_single_space` - ul para nl space tab link-url bl link - nm

- not an LRD because of leading para
- test_whitespaces_lrd_with_tabs_before_within_ordered_list_and_single_space

```python
    source_markdown = """- abc
 \t[fred]: /url

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_unordered_list_single_over_two_lines_a` - ul para bl space tab link nl spaces url bl link - nm

- a LRD because leading para broken by bl
- test_whitespaces_lrd_with_tabs_before_within_ordered_list_single_over_two_lines_a

```python
    source_markdown = """- abc

 \t[fred]:
  /url

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_unordered_list_and_spaces_x` - ul para nl spaces tab link-url bl link - nm

- not an LRD because of leading para
- test_whitespaces_lrd_with_tabs_before_within_ordered_list_and_spaces

```python
    source_markdown = """- abc
  \t[fred]: /url

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_unordered_list_and_spaces_a` - ul para bl spaces tab link-url bl link - nm

- a LRD because leading para broken by bl
- test_whitespaces_lrd_with_tabs_before_within_ordered_list_and_spaces_a

```python
    source_markdown = """- abc

  \t[fred]: /url

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_unordered_list_multiple_tabs_xx` - ul para nl tab link tab url tab title-with-tab bl link - nm

- not an LRD because of leading para
- test_whitespaces_lrd_with_tabs_before_within_ordered_list_multiple_tabs_xx

```python
    source_markdown = """- abc
\t[fred]:\t/url\t"bob\t"

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_unordered_list_multiple_tabs_a` - ul para bl tab link tab url tab title-with-tab bl link - nm

- a LRD because leading para broken by nl
- test_whitespaces_lrd_with_tabs_before_within_ordered_list_multiple_tabs_a

```python
    source_markdown = """- abc

\t[fred]:\t/url\t"bob"\t

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_unordered_list_bare_over_two_lines_1ea` - ul para nl tab link tab nl tab url tab bl para link - nm

- test_whitespaces_lrd_with_tabs_before_within_ordered_list_bare_over_two_lines_1ea

```python
    source_markdown = """- abc
\t[fred]:\t
\t/url\t

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_unordered_list_over_two_lines_1ea` - ul para bl tab link tab nl tab url tab bl para link - nm

- test_whitespaces_lrd_with_tabs_before_within_ordered_list_over_two_lines_1ea

```python
    source_markdown = """- abc

\t[fred]:\t
\t/url\t

[fred]"""
```

## Within Single OL

### `test_link_reference_definitions_extra_06a` - ol link-url - nm

- test_whitespaces_lrd_with_spaces_within_ulist_x

```python
    source_markdown = """1. [fred]: /url
[fred]"""
```

### `test_link_reference_definitions_extra_06b` - ol link nl indent url - nm

- test_link_reference_definitions_extra_01ce

```python
    source_markdown = """1. [foo]:
   /url"""
```

### `test_link_reference_definitions_extra_01d` - ol link nl indent url - nm

- not an LRD as it is split across two list items
- test_link_reference_definitions_extra_01cn

```python
    source_markdown = """1. [foo]:
1. /url"""
```

### `test_link_reference_definitions_extra_06c` - ol link-url-title - nm

- test_whitespaces_lrd_with_spaces_within_ulist_a

```python
    source_markdown = """1. [fred]: /url 'abc'
[fred]"""
```

### `test_link_reference_definitions_extra_06d` - ol link nl indent url nl indent title - nm

- test_link_reference_definitions_extra_01cf

```python
    source_markdown = """1. [foo]:
   /url
   'title'"""
```

### `test_link_reference_definitions_extra_06e` - ol link-url nl no-indent link-url - nm

- a pair of LRDs, one in list 1 and one in list 2
- test_link_reference_definitions_extra_01cj

```python
    source_markdown = """1. [foo]: /url
[foo2]: /url2"""
```

### `test_link_reference_definitions_extra_06f` - ol link-url nl bq link-url - nm

- a pair of LRDs, one in list 1 and one in list 2
- test_link_reference_definitions_extra_01ck

```python
    source_markdown = """1. [foo]: /url
> [foo2]: /url2"""
```

### `test_link_reference_definitions_extra_06g` - ol link-url nl ul link-url - nm

- a pair of LRDs, one in list 1 and one in list 2
- test_link_reference_definitions_extra_01cl

```python
    source_markdown = """1. [foo]: /url
- [foo2]: /url2"""
```

### `test_link_reference_definitions_extra_06h` - ol link-url nl ol link-url - nm

- a pair of LRDs, one in list 1 and one in list 2
- test_link_reference_definitions_extra_01cm

```python
    source_markdown = """1. [foo]: /url
1. [foo2]: /url2"""
```

### `test_whitespaces_lrd_with_spaces_within_olist` - ol para blank indent link-url - nm

- para, blank line, then properly indented LRD
- test_whitespaces_lrd_with_spaces_within_ulist_leading_para_x

```python
    source_markdown = """1. abc

   [fred]: /url
[fred]"""
```

### `test_whitespaces_lrd_with_spaces_before_within_olist` - ol para nl indent link-url - nm

- not an LRD due to leading paragraph
- test_whitespaces_lrd_with_spaces_within_ulist_leading_para_a

```python
    source_markdown = """1. abc
    [fred]: /url

[fred]"""
```

### `test_link_reference_definitions_extra_06j` - ol blank link-url - nm

- test_whitespaces_lrd_with_spaces_within_ulist_leading_para_b

```python
    source_markdown = """1.
  [fred]: /url
[fred]"""
```

### `test_link_reference_definitions_extra_06k` - ol link nl indent url - nm

- LRD split over 2 lines with enough space to keep it in the list
- test_whitespaces_lrd_with_spaces_within_ulist_leading_para_split_two_lines_x

```Python
    source_markdown = """1. [foo]:
   /url"""
```

### `test_link_reference_definitions_extra_06l` - ol link nl no-indent url - nm

- NOT A LRD, as the second line does not have enough spaces to keep it in the list
- test_whitespaces_lrd_with_spaces_within_ulist_leading_para_split_two_lines_minus_all_spaces

```Python
    source_markdown = """1. [foo]:
/url"""
```

### `test_link_reference_definitions_extra_06m` - ol link-url ol title - nm

- an LRD, but only the link and url, not the title
- test_link_reference_definitions_extra_01cd

```python
    source_markdown = """1. [foo]: /url
   1. 'abc'"""
```

### `test_link_reference_definitions_extra_06n` - ol link-url ol link-url - nm

- a pair of LRDs, one in list 1 and one in list 2
- test_link_reference_definitions_extra_01cg

```python
    source_markdown = """1. [foo]: /url
   1. [foo2]: /url2"""
```

### `test_link_reference_definitions_extra_06p` - ol para li link-url - nm

- test_link_reference_definitions_extra_01ca

```python
    source_markdown = """1. abc
1. [foo]: /url"""
```

### `test_link_reference_definitions_extra_06q` - ol link-url li para - nm

- test_link_reference_definitions_extra_01cc

```python
    source_markdown = """1. [foo]: /url
1. abc"""
```

### `test_link_reference_definitions_extra_06r` - ul link-url li link-url - nm

- a pair of LRDs, one in list 1 and one in list 2
- test_link_reference_definitions_extra_01ch

```python
    source_markdown = """1. [foo]: /url
1. [foo2]: /url2"""
```

### `test_whitespaces_lrd_with_tabs_before_within_ordered_list_x` - ol para nl tab link-url bl para link - nm

- not an LRD because of leading para
- test_whitespaces_lrd_with_tabs_before_within_unordered_list_x

```python
    source_markdown = """1. abc
\t[fred]: /url

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_ordered_list_single_over_two_lines_x` - ol para bl tab link tab nl spaces url bl link - nm

- a LRD because leading para broken by bl
- test_whitespaces_lrd_with_tabs_before_within_unordered_list_single_over_two_lines_x

```python
    source_markdown = """- abc

\t[fred]:\t
  /url

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_ordered_list_and_single_space` - ol para nl space tab link-url bl link - nm

- not an LRD because of leading para
- test_whitespaces_lrd_with_tabs_before_within_unordered_list_and_single_space

```python
    source_markdown = """1. abc
 \t[fred]: /url

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_ordered_list_single_over_two_lines_a` - ol para bl space tab link nl spaces url bl link - nm

- a LRD because leading para broken by bl
- test_whitespaces_lrd_with_tabs_before_within_unordered_list_single_over_two_lines_a

```python
    source_markdown = """1. abc

 \t[fred]:
   /url

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_ordered_list_and_spaces` - ol para nl spaces tab link-url bl link - nm

- not an LRD because of leading para
- test_whitespaces_lrd_with_tabs_before_within_unordered_list_and_spaces_x

```python
    source_markdown = """1. abc
  \t[fred]: /url

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_ordered_list_and_spaces_a` - ol para bl spaces tab link-url bl link - nm

- a LRD because leading para broken by bl
- test_whitespaces_lrd_with_tabs_before_within_unordered_list_and_spaces_a

```python
    source_markdown = """1. abc

  \t[fred]: /url

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_ordered_list_multiple_tabs_xx` - ol para nl tab link tab url tab title-with-tab bl link - nm

- not an LRD because of leading para
- test_whitespaces_lrd_with_tabs_before_within_unordered_list_multiple_tabs_xx

```python
    source_markdown = """1. abc
\t[fred]:\t/url\t"bob\t"

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_ordered_list_multiple_tabs_a` - ol para bl tab link tab url tab title-with-tab bl link - nm

- a LRD because leading para broken by nl
- test_whitespaces_lrd_with_tabs_before_within_unordered_list_multiple_tabs_a

```python
    source_markdown = """1. abc

\t[fred]:\t/url\t"bob"\t

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_ordered_list_bare_over_two_lines_1ea` - ol para nl tab link tab nl tab url tab bl para link - nm

- not an LRD because of leading para
- test_whitespaces_lrd_with_tabs_before_within_unordered_list_over_two_lines_1ea

```python
    source_markdown = """1. abc
\t[fred]:\t
\t/url\t

[fred]"""
```

## Within Single BQ

### `test_link_reference_definitions_extra_07a` - bq link-url - nm

- simple LRD in a BQ

```python
    source_markdown = """> [foo]: /url"""
```

### `test_link_reference_definitions_187` - para link blank bq link-url - nm

- LRD can be within a bq, with the link outside of the bq

```python
    source_markdown = """[foo]

> [foo]: /url"""
```

### `test_link_reference_definitions_extra_07b` - ?? test_link_reference_definitions_187

- LRD can be within a bq, with the link outside of the bq

```python
    source_markdown = """[foo]
> [foo]: /url"""
```

### `test_whitespaces_lrd_with_spaces_within_block_quote` - bq link-url nl bq link - ?? test_link_reference_definitions_extra_07a

- single line, within bq

```python
    source_markdown = """> [fred]: /url
> [fred]"""
```

### `test_link_reference_definitions_extra_02x` - bq link nl end-bq url - nm

- "LRD" is split within the bq and "outside" of the bq.  as such, line 1 is interpretted as a paragraph, and line 2 a continuation of it

```python
    source_markdown = """> [foo]:
/url"""
```

### `test_link_reference_definitions_extra_02ax` - bq link nl url - nm

- like `test_link_reference_definitions_extra_02x`, but with a bq start character, allowing the LRD to not be split

```python
    source_markdown = """> [foo]:
> /url"""
```

### `test_link_reference_definitions_extra_02aa` - bq link nl url nl title - nm

```python
    source_markdown = """> [foo]:
> /url
> "abc"
"""
```

### `test_whitespaces_lrd_with_spaces_before_within_block_quotes_bare_over_more_lines_3x` - bq para bl link nl url nl para end-bq bl link - nm

- multiline with open title, allowing partial LRD of first two lines

```python
    source_markdown = """> abc
>
> [fred]:
> /url
> "times
> new roman
> abc

[fred]"""
```

### `test_whitespaces_lrd_with_spaces_before_within_block_quotes_bare_over_more_lines_3xa` - ?? test_whitespaces_lrd_with_spaces_before_within_block_quotes_bare_over_more_lines_3x

- like `test_whitespaces_lrd_with_spaces_before_within_block_quotes_bare_over_more_lines_3x`, but link in bq

```python
    source_markdown = """> abc
>
> [fred]:
> /url
> "times
> new roman
> abc
>
> [fred]"""
```

### `test_whitespaces_lrd_with_spaces_extra_within_block_quote` - bq para nl spaces link-url nl spaces title - nm

- single line, within bq, with an extra space before the LRD
- not a LRD because of leading para

```python
    source_markdown = """> abc
>  [fred]: /url
>  [fred]"""
```

### `test_link_reference_definitions_extra_07c` - bq atx link-url para link - nm

```python
    source_markdown = """> # abc
>  [fred]: /url
>  [fred]"""
```

### `test_whitespaces_lrd_with_spaces_after_block_quote` - bq para end-bq space link-url bl link - nm

- without a blank line, the LRD in this case is considered part of the paragraph started on line 2

```python
    source_markdown = """> abc
> def
  [fred]: /url
[fred]"""
```

### `test_whitespaces_lrd_with_spaces_after_blank_line_and_block_quote` - bq para end-bq bl spaces link-url bl link - nm

- the blank line breaks the paragraphs, the LRD is free and clear

```python
    source_markdown = """> abc
> def

  [fred]: /url
[fred]"""
```

### `test_whitespaces_lrd_with_spaces_before_within_block_quote_just_enough` - ?? test_whitespaces_lrd_with_spaces_after_block_quote

```python
    source_markdown = """> abc
> def
   [fred]: /url
[fred]"""
```

### `test_whitespaces_lrd_with_spaces_before_within_block_quotes_bare_repeat_3` - bq link-url nl link-url nl para link nl link - nm

- multiple LRDs, one after another, within bq

```python
    source_markdown = """> [fred]: /url1
> [barney]: /url2
> [fred]
> [barney]"""
```

### `test_whitespaces_lrd_with_spaces_before_within_block_quotes_bare_with_space_repeat_2a` - ?? test_whitespaces_lrd_with_spaces_before_within_block_quotes_bare_repeat_3

- multiple LRDs, one after another, within bq, then out of bq for links

```python
    source_markdown = """> [fred]: /url1
> [barney]: /url2

[fred]
[barney]"""
```

### `test_link_reference_definitions_extra_07e` - bq link-url bq para "title" - nm

- first line is a LRD, second line is para

```python
    source_markdown = """> [fred]: /url1
> > "title"
"""
```

### `test_link_reference_definitions_extra_07fx` - bq link-url ul para "title" - nm

- first line is a LRD, second line is para

```python
    source_markdown = """> [fred]: /url1
> - "title"
"""
```

### `test_link_reference_definitions_extra_07fa` - bq link-url end-bq ul "title" - nm

- first line is a LRD, second line is para

```python
    source_markdown = """> [fred]: /url1
- "title"
"""
```

### `test_link_reference_definitions_extra_07gx` - bq link-url ol para title - nm

- first line is a LRD, second line is para

```python
    source_markdown = """> [fred]: /url1
> 1. "title"
"""
```

### `test_link_reference_definitions_extra_07ga` - bq link-url end-bq ol para title - nm

- first line is a LRD, second line is para

```python
    source_markdown = """> [fred]: /url1
1. "title"
"""
```

### `test_link_reference_definitions_extra_02bx` - bq link bq url - nm

- not an LRD as the second line is in a different container

```python
    source_markdown = """> [foo]:
>> /url"""
```

### `test_link_reference_definitions_extra_03x` - ?? test_link_reference_definitions_extra_02bx

```python
    source_markdown = """> [foo]:
>> [foo]:
>> # abc"""
```

### `test_link_reference_definitions_extra_02ba` - ?? test_link_reference_definitions_extra_02bx

```python
    source_markdown = """> [foo]:
>>> /url"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_x1` - bq para nl tab link-url para link

- LRD continues the para

```python
    source_markdown = """> abc
> def
\t[fred]: /url
[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_x3` - bq para bl tab link-url para link

- blank stops the para, but without any container, a tab means an icb

```python
    source_markdown = """> abc
> def

\t[fred]: /url
[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_x2` - ?? test_whitespaces_lrd_with_tabs_before_within_block_quotes_x1

```python
    source_markdown = """> abc
> def
  \t[fred]: /url

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_repeat` - ?? test_whitespaces_lrd_with_spaces_extra_within_block_quote

```python
    source_markdown = """> abc
> def
>\t[fred]: /url1
>\t[barney]: /url2

[fred]
[barney]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_repeat` - bq tab link-url nl tab link-url nl para link nl link - nm

```python
    source_markdown = """>\t[fred]: /url1
>\t[barney]: /url2
[fred]
[barney]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_space_repeat` - ?? test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_repeat

```python
    source_markdown = """> \t[fred]: /url1
> \t[barney]: /url2
[fred]
[barney]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_many_tabs` - bq tab link tab url tab nl tab link tab url tab nl para link nl link - nm

```python
    source_markdown = """>\t[fred]:\t/url1\t
>\t[barney]:\t/url2\t
[fred]
[barney]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_repeat_1a` - ?? test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_repeat

```python
    source_markdown = """>\t[fred]: /url1
>\t[barney]: /url2

[fred]
[barney]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_repeat_1b` - bq tab link-url-title nl tab link-url-title nl para link nl link - nm

```python
    source_markdown = """>\t[fred]: /url1 "title"
>\t[barney]: /url2 "other title"
[fred]
[barney]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_repeat_1c` - ?? test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_repeat_1b

```python
    source_markdown = """>\t[fred]: /url1 "title"
>\t[barney]: /url2 "other title"

[fred]
[barney]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_repeat_2a` - ?? test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_many_tabs

```python
    source_markdown = """>\t[fred]:\t/url1\t
>\t[barney]:\t/url2\t

[fred]
[barney]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_repeat_2b` - bq tab link tab url tab title tab nl tab link tab url tab title tab nl para link nl link - nm

```python
    source_markdown = """>\t[fred]:\t/url1\t"title"\t
>\t[barney]:\t/url2\t"other title"\t
[fred]
[barney]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_repeat_2c` - ?? test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_repeat_2b

```python
    source_markdown = """>\t[fred]:\t/url1\t"title"\t
>\t[barney]:\t/url2\t"other title"\t

[fred]
[barney]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_repeat_3` - ?? test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_many_tabs

```python
    source_markdown = """>\t[fred]:\t/url1\t
>\t[barney]:\t/url2\t
>\t[fred]
>\t[barney]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_space_repeat_1a` - bq space tab link-url nl space tab link-url nl para link nl link - nm

```python
    source_markdown = """> \t[fred]: /url1
> \t[barney]: /url2

[fred]
[barney]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_space_repeat_1b` - ?? test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_repeat_1b

```python
    source_markdown = """> \t[fred]: /url1 "title"
> \t[barney]: /url2 "other title"
[fred]
[barney]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_space_repeat_1c` - ?? test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_repeat_1b

```python
    source_markdown = """> \t[fred]: /url1 "title"
> \t[barney]: /url2 "other title"

[fred]
[barney]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_space_repeat_2x` - bq space tab link tab url tab nl space tab link tab url tab nl para link nl link - nm

```python
    source_markdown = """> \t[fred]:\t/url1\t
> \t[barney]:\t/url2\t
[fred]
[barney]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_space_repeat_2a` - ?? test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_space_repeat_2x

```python
    source_markdown = """> \t[fred]:\t/url1\t
> \t[barney]:\t/url2\t

[fred]
[barney]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_space_repeat_2b` - bq space tab link tab url tab title tab nl space tab link tab url tab title tab nl para link nl link - nm

```python
    source_markdown = """> \t[fred]:\t/url1\t"title"\t
> \t[barney]:\t/url2\t"other\ttitle"\t
[fred]
[barney]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_space_repeat_2c` - ?? test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_space_repeat_2b

```python
    source_markdown = """> \t[fred]:\t/url1\t"title"\t
> \t[barney]:\t/url2\t"other\ttitle"\t

[fred]
[barney]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_unordered_list_multiple_tabs_xax` - bq text nl tab link tab url tab title-with-tab end-bq bl link - nm

- not an LRD because of leading para

```python
    source_markdown = """> abc
\t[fred]:\t/url\t"bob\t"

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_unordered_list_multiple_tabs_xaa` - bq text end-bq bl tab link tab url tab title-with-tab bl link - nm

- not a LRD because line 3 is not within container

```python
    source_markdown = """> abc

\t[fred]:\t/url\t"bob\t"

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_unordered_list_multiple_tabs_xab` - bq text bl tab link tab url tab title-with-tab end-bq bl link - nm

```python
    source_markdown = """> abc
>
>\t[fred]:\t/url\t"bob\t"

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_space_repeat_3x` - bq space tab link tab url tab title extra tab end-bq para link - nm

- not an LRD because of trailing

```python
    source_markdown = """> \t[fred]:\t/url1\t"abc"def
[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_space_repeat_3a` - ?? test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_space_repeat_3x

```python
    source_markdown = """> \t[fred]:\t/url1\t"abc"def

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_space_repeat_4x` - bq space tab link tab url tab title-open extra tab end-bq para link - nm

- not an LRD as the title is left open

```python
    source_markdown = """> \t[fred]:\t/url1\t"abc
[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_space_repeat_4a` - ?? test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_space_repeat_4x

```python
    source_markdown = """> \t[fred]:\t/url1\t"abc

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_space_repeat_5x` - bq space tab link tab url-open end-bq para link - nm

```python
    source_markdown = """> \t[fred]:\t</url1
[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_space_repeat_5a` - ?? test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_space_repeat_5x

```python
    source_markdown = """> \t[fred]:\t</url1

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_space_repeat_6` - bq space tab link tab end-bq para link - nm

- not and LRD as LRD was started, so line 2 is not a continuation

```python
    source_markdown = """> \t[fred]:\t
[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_space_repeat_6a` - ?? test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_space_repeat_6

```python
    source_markdown = """> \t[fred]:\t

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_over_two_lines_1xx` - bq space tab link tab nl space tab url tab end-bq para link - nm

```python
    source_markdown = """> \t[fred]:\t
> \t/url\t

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_over_two_lines_1xa` - bq space tab link nl space tab url end-bq para link - nm

```python
    source_markdown = """> \t[fred]:
> \t/url

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_over_two_lines_1xb` - bq space link tab nl space url tab end-bq para link - nm

```python
    source_markdown = """> [fred]:\t
> /url\t

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_over_two_lines_1ax` - bq tab link tab nl space tab url tab end-bq para link - nm

```python
    source_markdown = """>\t[fred]:\t
> \t/url\t

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_over_two_lines_1aa` - bq space tab link tab nl space tab url tab end-bq para link - nm

```python
    source_markdown = """> \t[fred]:\t
> \t/url\t

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_over_two_lines_1b` - bq space tab link tab nl tab url tab end-bq para link - nm

```python
    source_markdown = """> \t[fred]:\t
>\t/url\t

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_over_two_lines_1c` - bq tab link tab nl tab url tab end-bq para link - nm

```python
    source_markdown = """>\t[fred]:\t
>\t/url\t

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_over_two_lines_1d` - ?? test_whitespaces_lrd_with_spaces_extra_within_block_quote

```python
    source_markdown = """> abc
>\t[fred]:\t
>\t/url\t

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_over_two_lines_1ea` - bq text bq text end-bq bl tab url tab nl tab url tab end-bq para link - nm

```python
    source_markdown = """> abc
> > def
>
>\t[fred]:\t
>\t/url\t

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_over_two_lines_1f` - bq text bl tab url tab nl tab url tab nl text end-bq para link - nm

```python
    source_markdown = """> abc
>
> \t[fred]:\t
> \t/url\t
> abc

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_over_more_lines_2x` - bq space tab link tab nl space tab url tab nl space tab title tab end-bq bl para link - nm

```python
    source_markdown = """> \t[fred]:\t
> \t/url\t
> \t"title"\t

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_over_more_lines_2a` - bq text bl space tab link tab nl space tab url tab nl space tab title tab bl text end-bq bl para link

```python
    source_markdown = """> abc
>
> \t[fred]:\t
> \t/url\t
> \t"title"\t
> abc

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_over_more_lines_3x` - bq text bl space tab link tab nl space tab url tab nl text - end-bq para link - nm

```python
    source_markdown = """> abc
>
> \t[fred]:\t
> \t/url\t
> \t"times\t
> \tnew\troman\t
> abc

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_over_more_lines_3a` - bq text bl space tab link tab nl text end-bq link - nm

- noy an lrd as the url starts with < but is not terminated

```python
    source_markdown = """> abc
>
> \t[fred]:\t
> \t</url\t
> abc

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_over_more_lines_3b` - bq text bl space tab link tab end-bq link - nm

- not an LRD as no URL

```python
    source_markdown = """> abc
>
> \t[fred]:\t

[fred]"""
```

## ---- Up to here ----

## Within Double BQ

### `test_link_reference_definitions_extra_03a`

```python
    source_markdown = """>> [foo]:
>> [foo]:
>> # abc"""
```

### `test_whitespaces_lrd_with_some_spaces_after_double_block_quotes`

```python
    source_markdown = """> > abc
> > def
  [fred]: /url
[fred]"""
```

### `test_whitespaces_lrd_with_extra_spaces_after_double_block_quotes`

```python
    source_markdown = """> > abc
> > def
    [fred]: /url
[fred]"""
```

### `test_link_reference_definitions_extra_02cx`

```python
    source_markdown = """>> [foo]:
> /url"""
```

### `test_link_reference_definitions_extra_02ca`

```python
    source_markdown = """>>> [foo]:
> /url"""
```

### `test_link_reference_definitions_extra_03c`

```python
    source_markdown = """> # this is a heading
>> [foo]:
>> # abc"""
```

### `test_link_reference_definitions_extra_03d`

```python
    source_markdown = """> this is a heading
> ---------
>> [foo]:
>> # abc"""
```

### `test_link_reference_definitions_extra_03e`

```python
    source_markdown = """>     this is a heading
>> [foo]:
>> # abc"""
```

### `test_link_reference_definitions_extra_03fx`

````python
    source_markdown = """> ```Python
> print("Hello World")
> ```
>> [foo]:
>> # abc"""
````

### `test_link_reference_definitions_extra_03fa`

````python
    source_markdown = """> ```Python
> print("Hello World")
>> [foo]:
>> # abc"""
````

### `test_link_reference_definitions_extra_03gx`

```python
    source_markdown = """> <!-- comment -->
>> [foo]:
>> # abc"""
```

### `test_link_reference_definitions_extra_03ga`

```python
    source_markdown = """> <some-tag>
>> [foo]:
>> # abc"""
```

### `test_link_reference_definitions_extra_03gb`

```python
    source_markdown = """> <some-tag>
>
>> [foo]:
>> # abc"""
```

### `test_link_reference_definitions_extra_03h`

```python
    source_markdown = """> | title1 | title2 |
> | --- | --- |
> | r1c1 | r1c2 |
>> [foo]:
>> # abc"""
```

### `test_whitespaces_lrd_with_spaces_within_single_block_quote_after_double_block_quote`

```python
    source_markdown = """> abc
> > def
>   [fred]: /url
[fred]"""
```

### `test_whitespaces_lrd_with_spaces_before_within_double_block_quotes_with_zero_and_zero_spaces_at_start`

```python
    source_markdown = """> abc
> > def
[fred]: /url

[fred]"""
```

### `test_whitespaces_lrd_with_spaces_before_within_double_block_quotes_with_zero_and_one_space_at_start`

```python
    source_markdown = """> abc
> > def
 [fred]: /url

[fred]"""
```

### `test_whitespaces_lrd_with_spaces_before_within_double_block_quotes_with_zero_and_two_spaces_at_start`

```python
    source_markdown = """> abc
> > def
  [fred]: /url

[fred]"""
```

### `test_whitespaces_lrd_with_spaces_before_within_double_block_quotes_with_zero_and_three_spaces_at_start`

```python
    source_markdown = """> abc
> > def
   [fred]: /url

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_double_block_quotes`

```python
    source_markdown = """> abc
> > def
\t[fred]: /url
[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_double_block_quotes_with_single`

```python
    source_markdown = """> abc
> > def
>\t[fred]: /url
[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_double_block_quotes_with_single_and_space`

```python
    source_markdown = """> abc
> > def
> \t[fred]: /url
[fred]"""
```

## Within Unordered-Unordered

### `test_link_reference_definitions_extra_04x`

```python
    source_markdown = """- [foo]:
  - [foo]:
    # abc"""
```

### `test_link_reference_definitions_extra_04b`

```python
    source_markdown = """- # heading
  - [foo]:
    # abc"""
```

### `test_link_reference_definitions_extra_04c`

```python
    source_markdown = """- heading
  ==========
  - [foo]:
    # abc"""
```

### `test_link_reference_definitions_extra_04d`

```python
    source_markdown = """-     icb
  - [foo]:
    # abc"""
```

### `test_link_reference_definitions_extra_04ex`

````python
    source_markdown = """- ```Python
  print("Hello World")
  ```
  - [foo]:
    # abc"""
````

### `test_link_reference_definitions_extra_04ea`

````python
    source_markdown = """- ```Python
  print("Hello World")
  - [foo]:
    # abc"""
````

### `test_link_reference_definitions_extra_04fx`

```python
    source_markdown = """- <!-- comment -->
  - [foo]:
    # abc"""
```

### `test_link_reference_definitions_extra_04fa`

```python
    source_markdown = """- <some-tag>
  - [foo]:
    # abc"""
```

### `test_link_reference_definitions_extra_04fb`

```python
    source_markdown = """- <some-tag>

  - [foo]:
    # abc"""
```

### `test_link_reference_definitions_extra_04g`

```python
    source_markdown = """- | title1 | title2 |
  | --- | --- |
  | r1c1 | r1c2 |
  - [foo]:
    # abc"""
```

### `test_link_reference_definitions_extra_05ax`

```python
    source_markdown = """- # heading
  - ## heading
    - [foo]:
      # abc"""
```

### `test_link_reference_definitions_extra_05aa`

```python
    source_markdown = """1. # heading
   1. # heading
      - [foo]:
      # abc"""
```

### `test_link_reference_definitions_extra_05ab`

```python
    source_markdown = """1. # heading
   1. # heading
      1. [foo]:
         # abc"""
```

### `test_link_reference_definitions_extra_05cx`

```python
    source_markdown = """- # heading
  > ## heading
  > - [foo]:
  >   # abc"""
```

### `test_whitespaces_lrd_with_tabs_before_within_ordered_double_list_only_spaces`

```python
    source_markdown = """1. abc
   1. def
    [fred]: /url

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_list_single_over_two_lines_b`

```python
    source_markdown = """- abc
  - def

  \t[fred]:
    /url

[fred]"""
```

## Within Ordered-Ordered

--- NEW ---

### `test_whitespaces_lrd_with_tabs_before_within_ordered_double_list_x`

```python
    source_markdown = """1. abc
   1. def
\t  [fred]: /url

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_ordered_double_list_no_spaces`

```python
    source_markdown = """1. abc
   1. def
\t[fred]: /url

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_ordered_double_list_tab_after_indent`

```python
    source_markdown = """1. abc
   1. def
   \t[fred]:\t/url\t

[fred]"""
```

### `test_whitespaces_lrd_with_tabs_before_within_ordered_double_list_one_space`

```python
    source_markdown = """1. abc
   1. def
\t [fred]: /url

[fred]"""
```

## Others

### `test_link_reference_definitions_extra_05bx`

```python
    source_markdown = """> # heading
> - ## heading
>   - [foo]:
>     # abc"""
```

### `test_whitespaces_lrd_with_tabs_before_within_unordered_double_list`

```python
    source_markdown = """- abc
  - def
\t[fred]: /url

[fred]"""
```

### `test_link_reference_definitions_183ge` - ?????

- still not an LRD

```python
    source_markdown = """- A simple list
*foo*: /url
> [Foo]"""
```

### `test_link_reference_definitions_183gf` - ?????

- still not an LRD

```python
    source_markdown = """- A simple list
items
> [Foo]"""
```
