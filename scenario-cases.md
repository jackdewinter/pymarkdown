# Scenarios

Legend:

- `\a` space character
- `\\` backslash character
- `\n` newline character

- Series A - Starts with inline
- Series B - Contains inline
- Series C - Ends with inline
- Series D - Only inline
- Series E - Newline in the middle of newline
- Series F - Link/image with newline (and whitespace) in various parts of link
- Series G - Link/image with backslash and character entity in various parts of link
- Series H - Link/image with text/code span/raw html in label of various link types
- Series J - Link/image with various combinations with other inline tokens
- Series K - use of `&#xa;` instead of \n (all verified against babelmark)
- Series L - link/image inside of link/image

## Series A

| t | s | x | y | z |
| -- | --- | --- | --- | --- |
| Ab | starts with a backslash escape | `\\\\this is a fun day` | test_paragraph_series_a_b |
| Abh| starts with a backslash hard line break | `\\\n` | test_paragraph_series_a_bh |
| Ash| starts with spaces hard line break | `\a\a\a\n---` | test_paragraph_series_a_sh |
| Acs| starts with a code span | `` `this` is a fun day `` | test_paragraph_series_a_cs |
| Acr| starts with a character reference | `&amp; the band played on` | test_paragraph_series_a_cr |
| Arh| starts with a raw html | `<there it='is'>, really` | test_paragraph_series_a_rh |
| Aua| starts with an URI autolink | `<http://google.com> to look` | test_paragraph_series_a_ua |
| Aea| starts with an email autolink | `<foo@r.com> for info` | test_paragraph_series_a_ea |
| Ae | starts with an emphasis | `*it's* me!` | test_paragraph_series_a_e |
| Al | starts with a link | `[Foo](/uri "t") is a link` | test_paragraph_series_a_l |
| Ai | starts with an image | `![foo](/url "t") is an image` | test_paragraph_series_a_i |

## Series B

| t | s | x | y | z |
| --- | --- | --- | --- | --- |
| Bb | contains a backslash | `a \\\\fun\\\\ day` | test_paragraph_series_b_b |
| Bcs| contains a code span | `a ``fun`` day` | test_paragraph_series_b_cs |
| Bcr| contains a character reference | `fun &amp; joy` | test_paragraph_series_b_cr |
| Brh| contains a raw html | `where <there it='is'> it` | test_paragraph_series_b_rh |
| Bua| contains an URI autolink | `look <http://www.com> for` | test_paragraph_series_b_ua |
| Bea| contains an email autolink | `email <foo@bar.com> for` | test_paragraph_series_b_ea |
| Be | contains emphasis | `really! *it's me!* here!` | test_paragraph_series_b_e |
| Bl | contains a link | `at [Foo](/uri "t") more` | test_paragraph_series_b_l |
| Bi | contains an image | `my ![foo](/url "t") image` | test_paragraph_series_b_i |

## Series C

| t | s | x | y | z |
| --- | --- | --- | --- | --- |
|Cb |ends with a backslash | `a fun day\\\\` | test_paragraph_series_c_b |
|Cbh|ends with a backslash hard line break | `this was \\\n` | test_paragraph_series_c_bh |
|Csh|ends with spaces hard line break | `no line break?\a\a\a\n` | test_paragraph_series_c_sh |
|Ccs|ends with a code span | ` a fun ``day`` ` | test_paragraph_series_c_cs |
|Ccr|ends with a character reference | `played on &amp;` | test_paragraph_series_c_cr |
|Crh|ends with a raw html | `really, <there it='is'>` | test_paragraph_series_c_rh |
|Cua |ends with an URI autolink | `at <http://www.google.com>` | test_paragraph_series_c_ua |
|Cea |ends with an email autolink | `contact <foo@bar.com>` | test_paragraph_series_c_ea |
|Ce  |ends with an emphasis | `it's *me*` | test_paragraph_series_c_e |
|Cl  |ends with a link | `like [Foo](/uri "t")` | test_paragraph_series_c_l |
|Ci  |ends with an image | `an ![foo](/url "t")` | test_paragraph_series_c_i |

## Series D

| t | s | x | y | z |
| --- | --- | --- | --- | --- |
|Db  |only a backslash| `\\\\` | test_paragraph_series_d_b |
|Dbh |only backslash hard line break| ` \\\n` | test_paragraph_series_d_bh |
|Dsh |only spaces hard line break| `\a\a\a\a\n` | test_paragraph_series_d_sh |
|Dcs |only code span| ` ``day`` ` | test_paragraph_series_d_cs |
|Dcr |only character reference| `&amp;` | test_paragraph_series_d_cr |
|Drh |only raw html (html block)| `<there it='is'>` | test_paragraph_series_d_rh |
|Dua |only an URI autolink| `<http://www.google.com>` | test_paragraph_series_d_ua |
|Dea |only an email autolink| `<foo@bar.com>` | test_paragraph_series_d_ea |
|De  |only an emphasis| `*me*` | test_paragraph_series_d_e |
|Dlt |only a link & title| `[Foo](/uri "title")` | test_paragraph_series_d_l_t |
|Dlnt|only a link no title| `[Foo](/uri)` | test_paragraph_series_d_l_nt |
|Dit |only an image & title| `![foo](/url "title")` | test_paragraph_series_d_i_t |
|Dint|only an image no title| `![foo](/url)` | test_paragraph_series_d_i_nt |

## Series E

| t | s | x | y | z |
| --- | --- | --- | --- | --- |
|Ecs |code span with newline| ` a``code\nspan``a ` | test_paragraph_series_e_cs |
|Erh |raw html with newline| `a<raw\nhtml='cool'>a` | test_paragraph_series_e_rh |
|Eua |URI autolink with newline| `a<http://www.\ngoogle.com>a` | test_paragraph_series_e_ua |
|Eea |email autolink with newline| `a<foo@bar\n.com>a` | test_paragraph_series_e_ea |
|Eem |emphasis with newline| `a*foo\nbar*a` | test_paragraph_series_e_em |

## Unverified F

| t | s | x | y | z |
| --- | --- | --- | --- | --- |
|F1  |inline link with newline in link label| `a[Fo\no](/uri "testing")a` | test_paragraph_extra_47 |
|F1a |inline link with newline in link label| `a[Fo\no](/uri "testing")` | test_paragraph_extra_47a |
|F1i |inline image with newline in link label| `a![Fo\no](/uri "title")a` | test_paragraph_extra_61 |
|F1i |inline image with newline in link label| `a![Fo\no](/uri "title")` | test_paragraph_extra_61j |
|F2  |inline link with newline in pre-url| `a[Foo](\n/uri "testing")a` | test_paragraph_extra_48x |
|F2a |F2 with whitespace before newline| `a[Foo](\a\a\n/uri "testing")` | test_paragraph_extra_48d |
|F2i |inline image with newline in pre-url| `a![Foo](\n/uri "testing")a` | test_paragraph_extra_62 |
|F2ia |inline image with newline in pre-url| `a![Foo](\n/uri "testing")` | test_paragraph_extra_62f |
|F2b |F2 with whitespace after newline| `a[Foo](\n   /uri "testing")a` | test_paragraph_extra_48b |
|F2ba|F2 with whitespace after newline| `a[Foo](\n   /uri "testing")` | test_paragraph_extra_48ba |
|F2bi|F2i with whitespace after newline| `a![Foo](\n   /uri "testing")a` | test_paragraph_extra_62b |
|F2bia|F2i with whitespace after newline| `a![Foo](\n   /uri "testing")` | test_paragraph_extra_62ba |
|F2c |F2 with whitespace before & after newline| `a[Foo](  \n   /uri "testing")a` | test_paragraph_extra_48c |
|F2ca |F2 with whitespace before & after newline| `a[Foo](  \n   /uri "testing")` | test_paragraph_extra_48ca |
|F2ci|F2i with whitespace before & after newline| `a![Foo](  \n   /uri "testing")a` | test_paragraph_extra_62c |
|F2cia|F2i with whitespace before & after newline| `a![Foo](  \n   /uri "testing")` | test_paragraph_extra_62ca |
|F3  |inline link with newline in url (invalid) | `a[Foo](/ur\ni "testing")a` | test_paragraph_extra_49 |
|F3a |inline link with newline in url (invalid) | `a[Foo](/ur\ni "testing")` | test_paragraph_extra_49a |
|F3i |inline image with newline in url (invalid) | `a![Foo](/ur\ni "title")a` | test_paragraph_extra_63 |
|F3ia |inline image with newline in url (invalid) | `a![Foo](/ur\ni "title")` | test_paragraph_extra_63e |
|F4  |inline link with newline in post-url | `a[Foo](/uri\a\n"testing")a` | test_paragraph_extra_50x |
|F4a |F4 with whitespace before newline | `a[Foo](/uri\a\a\n"testing")` | test_paragraph_extra_50d |
|F4i |inline image with newline in post-url | `a![Foo](/uri\n"testing")a` | test_paragraph_extra_64x |
|F4ai|F4i with whitespace before newline | `a![Foo](/uri\n"testing")` | test_paragraph_extra_64xa |
|F4b |F4 with whitespace after newline | `a[Foo](/uri\n   "testing")a` | test_paragraph_extra_50b |
|F4ba |F4 with whitespace after newline | `a[Foo](/uri\n   "testing")` | test_paragraph_extra_50ba |
|F4bi|F4i with whitespace after newline | `a![Foo](/uri\n   "testing")a` | test_paragraph_extra_64b |
|F4bia|F4i with whitespace after newline | `a![Foo](/uri\n   "testing")` | test_paragraph_extra_64ba |
|F4c |F4 with whitespace before & after newline | `a[Foo](/uri\a\a\n   "testing")a` | test_paragraph_extra_50c |
|F4ca |F4 with whitespace before & after newline | `a[Foo](/uri\a\a\n   "testing")` | test_paragraph_extra_50ca |
|F4ci|F4i with whitespace before & after newline | `a![Foo](/uri\a\a\n   "testing")a` | test_paragraph_extra_64c |
|F4cia|F4i with whitespace before & after newline | `a![Foo](/uri\a\a\n   "testing")` | test_paragraph_extra_64ca |
|F5x  |inline link with newline in title| `a[Foo](/uri "test\ning")a` | test_paragraph_extra_51 |
|F5xa  |inline link with newline in title| `a[Foo](/uri "test\ning")` | test_paragraph_extra_51c |
|F5i |inline image with newline in title| `a![Foo](/uri "test\ning")a` | test_paragraph_extra_66x |
|F5ia |inline image with newline in title| `a![Foo](/uri "test\ning")` | test_paragraph_extra_66xa |
|F5a  |inline link with newline in title| `a[Foo](</uri> "test\ning")a` | test_paragraph_extra_51a |
|F5aa |inline link with newline in title| `a[Foo](</uri> "test\ning")` | test_paragraph_extra_51aa |
|F5ai |inline image with newline in title| `a![Foo](</uri> "test\ning")a` | test_paragraph_extra_66c |
|F5aia |inline image with newline in title| `a![Foo](</uri> "test\ning")` | test_paragraph_extra_66ca |
|F5b  |inline link with newline in title| `a[Foo](</uri> "te\\\\st\ning")a` | test_paragraph_extra_51b |
|F5ba  |inline link with newline in title| `a[Foo](</uri> "te\\\\st\ning")` | test_paragraph_extra_51ba |
|F5bi |inline image with newline in title| `a![Foo](</uri> "te\\\\st\ning")a` | test_paragraph_extra_66d |
|F5bia|inline image with newline in title| `a![Foo](</uri> "te\\\\st\ning")` | test_paragraph_extra_66da |
|F6x |inline link with newline in post-title| `a[Foo](/uri "testing"\n)a` | test_paragraph_extra_52x |
|F6xa|inline link with newline in post-title| `a[Foo](/uri "testing"\n)` | test_paragraph_extra_52d |
|F6i |inline image with newline in post-title| `a![Foo](/uri "testing"\n)a` | test_paragraph_extra_67x |
|F6ix |inline image with newline in post-title| `a![Foo](/uri "testing"\n)` | test_paragraph_extra_67xa |
|F6a |F6 with whitespace before newline| `a[Foo](/uri "testing"\a\a\n)a` | test_paragraph_extra_52a |
|F6aa |F6 with whitespace before newline| `a[Foo](/uri "testing"\a\a\n)` | test_paragraph_extra_52aa |
|F6ai|F6i with whitespace before newline| `a![Foo](/uri "testing"\a\a\n)a` | test_paragraph_extra_67a |
|F6aia|F6i with whitespace before newline| `a![Foo](/uri "testing"\a\a\n)` | test_paragraph_extra_67aa |
|F6b |F6 with whitespace after newline| `a[Foo](/uri "testing"\n  )a` | test_paragraph_extra_52b |
|F6ba |F6 with whitespace after newline| `a[Foo](/uri "testing"\n  )` | test_paragraph_extra_52ba |
|F6bi|F6i with whitespace after newline| `a![Foo](/uri "testing"\n  )a` | test_paragraph_extra_67b |
|F6bia|F6i with whitespace after newline| `a![Foo](/uri "testing"\n  )` | test_paragraph_extra_67ba |
|F6c |F6 with whitespace before & after newline| `a[Foo](/uri "testing"\a\a\n  )a` | test_paragraph_extra_52c |
|F6ca |F6 with whitespace before & after newline| `a[Foo](/uri "testing"\a\a\n  )` | test_paragraph_extra_52ca |
|F6ci|F6i with whitespace before & after newline| `a![Foo](/uri "testing"\a\a\n  )a` | test_paragraph_extra_67c |
|F6cia|F6i with whitespace before & after newline| `a![Foo](/uri "testing"\a\a\n  )` | test_paragraph_extra_67ca |
|F7  |inline link with newline in label no title| `a[Fo\no](/uri)a` | test_paragraph_extra_60 |
|F7a  |inline link with newline in label no title| `a[Fo\no](/uri)` | test_paragraph_extra_60b |
|F7i |inline image with newline in label no title| `a![Fo\no](/uri)a` | test_paragraph_extra_60a |
|F7ia |inline image with newline in label no title| `a![Fo\no](/uri)` | test_paragraph_extra_60aa |
|F8  |inline link with newline in post-url no title| `a[Foo](/uri\n)a` | test_paragraph_extra_65a |
|F8a |inline link with newline in post-url no title| `a[Foo](/uri\n)` | test_paragraph_extra_65b |
|F8i |inline image with newline in post-url no title| `a![Foo](/uri\n)a` | test_paragraph_extra_65x |
|F8ia |inline image with newline in post-url no title| `a![Foo](/uri\n)` | test_paragraph_extra_65xa |
|F9i |inline image with newline in preface (link)| `a!\n[Foo](/uri "testing")a` | test_paragraph_extra_59 |
|F9ia |inline image with newline in preface (link)| `a!\n[Foo](/uri "testing")` | test_paragraph_extra_59a |
|F10 |full link with newline in link label| `a[foo\nbar][bar]a` | test_paragraph_extra_53 |
|F10a |full link with newline in link label| `a[foo\nbar][bar]` | test_paragraph_extra_53d |
|F10i|full image with newline in link label| `a![foo\nbar][bar]a` | test_paragraph_extra_53a |
|F10ia|full image with newline in link label| `a![foo\nbar][bar]` | test_paragraph_extra_53aa |
|F11 |full link with newline in link reference| `a[foo][ba\nr]a` | test_paragraph_extra_54 |
|F11a |full link with newline in link reference| `a[foo][ba\nr]` | test_paragraph_extra_54d |
|F11i|full image with newline in link reference| `a![foo][ba\nr]a` | test_paragraph_extra_54a |
|F11ia|full image with newline in link reference| `a![foo][ba\nr]a` | test_paragraph_extra_54aa |
|F12 |full link with newline starting link reference| `a[foo][\nbar]a` | test_paragraph_extra_58 |
|F12a |full link with newline starting link reference| `a[foo][\nbar]` | test_paragraph_extra_58b |
|F12i|full image with newline starting link reference| `a![foo][\nbar]a` | test_paragraph_extra_58a |
|F20 |shortcut link with newline in link label| `a[ba\nr]a` | test_paragraph_extra_55 |
|F20a |shortcut link with newline in link label| `a[ba\nr]` | test_paragraph_extra_55d |
|F20i|shortcut image with newline in link label| `a![ba\nr]a` | test_paragraph_extra_55a |
|F20ia|shortcut image with newline in link label| `a![ba\nr]a` | test_paragraph_extra_55aa |
|F30 |collapsed link with newline in link label| `a[ba\nr][]a` | test_paragraph_extra_56 |
|F30a |collapsed link with newline in link label| `a[ba\nr][]` | test_paragraph_extra_56d |
|F30i|collapsed image with newline in link label| `a![ba\nr][]a` | test_paragraph_extra_56a |
|F30ia|collapsed image with newline in link label| `a![ba\nr][]` | test_paragraph_extra_56aa |
|F31 |collapsed link with newline starting link label| `a[\nbar][]a` | test_paragraph_extra_57 |
|F31a |collapsed link with newline starting link label| `a[\nbar][]` | test_paragraph_extra_57b |
|F31i|collapsed image with newline starting link label  | `a![\nbar][]a` | test_paragraph_extra_57a |
|F31ia|collapsed image with newline starting link label  | `a![\nbar][]` | test_paragraph_extra_57aa |

|F40 |inline link with newlines around elements| `abc\n[link](\n/uri\n"title"\n)\ndef` | test_paragraph_extra_h9 |
|F40a |inline link with newlines around elements| `abc\n[link](\n/uri\n"title"\n)` | test_paragraph_extra_h9b |
|F40i|inline image with newline around elements| `abc\n![link](\n/uri\n"title"\n)\ndef` | test_paragraph_extra_h9a |
|F40ia|inline image with newline around elements| `abc\n![link](\n/uri\n"title"\n)\ndef` | test_paragraph_extra_h9aa |

|F41 |inline link with newlines and ws around elements| `abc\n[link](  \n  /uri  \n   "title"   \n )\ndef` | test_paragraph_extra_j0 |
|F41i|inline image with newline and ws around elements| `abc\n![link](  \n  /uri  \n   "title"   \n )\ndef` | test_paragraph_extra_j0a |
|F41a |inline link with newlines and ws around elements| `abc\n[link](  \n  /uri  \n   "title"   \n ) \ndef` | test_paragraph_extra_j0b |
|F41ai|inline image with newline and ws around elements| `abc\n![link](  \n  /uri  \n   "title"   \n ) \ndef` | test_paragraph_extra_j0c |
|F41b |inline link with newlines and ws around elements| `abc\n[link](  \n  /uri  \n   "title"   \n )` | test_paragraph_extra_j0d |

## Unverified G

| t | s | x | y | z |
| --- | --- | --- | --- | --- |
|G1   |inline link baseline| `a[Foo](/uri "title")a` | test_paragraph_extra_68a |
|G1i  |inline image baseline| `a![Foo](/uri "testing")a` | test_paragraph_extra_73a |
|G2   |inline link with replacement in link label| `a[Fo&beta;o](/uri "title")a` | test_paragraph_extra_68x |
|G2i  |inline image with replacement in link label| `a![Fo&beta;o](/uri "testing")a` | test_paragraph_extra_73 |
|G2a  |G2 with newline before replacement| `a[Fo\n&beta;o](/uri "testing")a` | test_paragraph_extra_68b |
|G2ai |G2i with newline before replacement| `a![Fo\n&beta;o](/uri "testing")a` | test_paragraph_extra_73b |
|G3   |inline link with backslash in link label| `a[Fo\\]o](/uri "testing")a` | test_paragraph_extra_69 |
|G3i  |inline image with backslash in link label| `a![Fo\\]o](/uri "testing")a` | test_paragraph_extra_74 |
|G3a  |G3 with newline before backslash| `a[Fo\n\\]o](/uri "testing")a` | test_paragraph_extra_69a |
|G3ai |G3i with newline before backslash| `a![Fo\n\\]o](/uri "testing")a` | test_paragraph_extra_74a |
|G4   |inline link containing uri with space| `a[Foo](</my uri> "testing")a` | test_paragraph_extra_70 |
|G4i  |inline image containing uri with space| `a![Foo](</my uri> "testing")a` | test_paragraph_extra_75 |
|G4a  |G4 with newline before space| `a[Foo](</my\n uri> "testing")a` | test_paragraph_extra_70a |
|G4ai |G4i with newline before space| `a![Foo](</my\n uri> "testing")a` | test_paragraph_extra_75a |
|G5   |inline link with replacement in title| `a[Foo](/uri "test&beta;ing")a` | test_paragraph_extra_71x |
|G5i  |inline image with replacement in title| `a![Foo](/uri "test&beta;ing")a` | test_paragraph_extra_76 |
|G5a  |G5 with newline before replacement| `a[Foo](/uri "test\n&beta;ing")a` | test_paragraph_extra_71a |
|G5ai |G5i with newline before replacement| `a![Foo](/uri "test\n&beta;ing")a` | test_paragraph_extra_76a |
|G6   |inline link with backslash in title| `a[Foo](/uri "test\\#ing")a` | test_paragraph_extra_72 |
|G6i  |inline image with backslash in title| `a![Foo](/uri "test\\#ing")a` | test_paragraph_extra_77 |
|G6a  |G6 with newline before backslash| `a[Foo](/uri "test\n\\#ing")a` | test_paragraph_extra_72a |
|G6ai |G6i with newline before backslash| `a![Foo](/uri "test\n\\#ing")a` | test_paragraph_extra_77a |
|G13  |full link with backslash in label| `a[foo\\#bar][bar]a` | test_paragraph_extra_78 |
|G13i |full image with backslash in label| `a![foo\\#bar][bar]a` | test_paragraph_extra_90 |
|G13a |G13 with newline before backslash| `a[foo\n\\#bar][bar]a` | test_paragraph_extra_78a |
|G13ai|G13i with newline before backslash| `a![foo\n\\#bar][bar]a` | test_paragraph_extra_90a |
|G14  |full link with replacement in label| `a[foo&beta;bar][bar]a` | test_paragraph_extra_79 |
|G14i |full image with replacement in label| `a![foo&beta;bar][bar]a` | test_paragraph_extra_91x |
|G14a |G14 with newline before replacement| `a[foo\n&beta;bar][bar]a` | test_paragraph_extra_79a |
|G14ai|G14i with newline before replacement| `a![foo\n&beta;bar][bar]a` | test_paragraph_extra_91a |
|G15  |full link with replacement in reference| `a[foo][ba&beta;r]a` | test_paragraph_extra_80 |
|G15i |full image with replacement in reference| `a![foo][ba&beta;r]a` | test_paragraph_extra_92 |
|G15a |G15 with newline before replacement| `a[foo][ba\n&beta;r]a` | test_paragraph_extra_80a |
|G15ai|G15i with newline before replacement| `a![foo][ba\n&beta;r]a` | test_paragraph_extra_92a |
|G16  |full link with backslash in reference| `a[foo][ba\\]r]a` | test_paragraph_extra_81 |
|G16i |full image with backslash in reference| `a![foo][ba\\]r]a` | test_paragraph_extra_93x |
|G16a |G16 with newline before replacement| `a[foo][ba\n\\]r]a` | test_paragraph_extra_81a |
|G16ai|G16i with newline before replacement| `a![foo][ba\n\\]r]a` | test_paragraph_extra_93a |
|G17  |shortcut link with replacement in label| `a[ba&beta;r]a` | test_paragraph_extra_82 |
|G17i |shortcut image with replacement in label| `a![ba&beta;r]a` | test_paragraph_extra_94x |
|G17a |G17 with newline before replacement| `a[ba\n&beta;r]a` | test_paragraph_extra_82a |
|G17ai|G17i with newline before replacement| `a![ba\n&beta;r]a` | test_paragraph_extra_94a |
|G18  |shortcut link with backslash in label| `a[ba\\]r]a` | test_paragraph_extra_83 |
|G18i |shortcut link with backslash in label| `a![ba\\]r]a` | test_paragraph_extra_95x |
|G18a |G18 with newline before replacement| `a[ba\n\\]r]a` | test_paragraph_extra_83a |
|G18ai|G18i with newline before replacement| `a![ba\n\\]r]a` | test_paragraph_extra_95a |
|G19  |collapsed link with replacement in label| `a[ba&beta;r][]a` | test_paragraph_extra_84 |
|G19i |collapsed link with replacement in label| `a![ba&beta;r][]a` | test_paragraph_extra_96 |
|G19a |G19 with newline before replacement| `a[ba\n&beta;r][]a` | test_paragraph_extra_84a |
|G19ai|G19 with newline before replacement| `a![ba\n&beta;r][]a` | test_paragraph_extra_96a |
|G20  |collapsed link with backslash in label| `a[ba\\]r][]a` | test_paragraph_extra_85 |
|G20i |collapsed link with backslash in label| `a![ba\\]r][]a` | test_paragraph_extra_97 |
|G20a |G20 with newline before replacement| `a[ba\n\\]r][]a` | test_paragraph_extra_85a |
|G20ai|G20 with newline before replacement| `a![ba\n\\]r][]a` | test_paragraph_extra_97a |

## Unverified H

| t | s | x | y | z |
| --- | --- | --- | --- | --- |
|H1  |inline link label split text token| `abc\n[li\nnk](/uri "title" )\n  def` | test_paragraph_extra_a3 |
|H1i |inline image label split text token| `abc\n![li\nnk](/uri "title" )\n def` | test_paragraph_extra_b5 |
|H1a |inline link label split span token| ``abc\n[li`de\nfg`nk](/uri "title" )\n def`` | test_paragraph_extra_a4 |
|H1ai|inline image label split span token| ``abc\n![li`de\nfg`nk](/uri "title" )\n def`` | test_paragraph_extra_b6 |
|H1b |inline link label split html token| ``abc\n[li<de\nfg>nk](/uri "title" )\n def`` | test_paragraph_extra_a5 |
|H1bi|inline image label split html token| ``abc\n![li<de\nfg>nk](/uri "title" )\n def`` | test_paragraph_extra_b7 |
|H2  |full link label split text token| `a[li\nnk][bar]a` | test_paragraph_extra_a6 |
|H2i |full image label split text token| `a![li\nnk][bar]a` | test_paragraph_extra_b8 |
|H2a |full link label split span token| ``a[li`de\nfg`nk][bar]a`` | test_paragraph_extra_a7 |
|H2ai|full image label split span token| ``a![li`de\nfg`nk][bar]a`` | test_paragraph_extra_b9 |
|H2b |full link label split html token| ``a[li<de\nfg>nk][bar]a`` | test_paragraph_extra_a8 |
|H2bi|full image label split html token| ``a![li<de\nfg>nk][bar]a`` | test_paragraph_extra_c0 |
|H3  |collapsed link label split text token| `a[li\nnk][]a` | test_paragraph_extra_a9 |
|H3i |collapsed image label split text token| `a![li\nnk][]a` | test_paragraph_extra_c1 |
|H3a |collapsed link label split span token| ``a[li`de\nfg`nk][]a`` | test_paragraph_extra_b0 |
|H3ai|collapsed image label split span token| ``a![li`de\nfg`nk][]a`` | test_paragraph_extra_c2 |
|H3b |collapsed link label split html token| ``a[li<de\nfg>nk][bar]a`` | test_paragraph_extra_b1 |
|H3bi|collapsed image label split html token| ``a![li<de\nfg>nk][]a`` | test_paragraph_extra_c3 |
|H4  |shortcut link label split text token| `a[li\nnk]a` | test_paragraph_extra_b2 |
|H4i |shortcut image label split text token| `a![li\nnk]a` | test_paragraph_extra_c4 |
|H4a |shortcut link label split span token| ``a[li`de\nfg`nk]a`` | test_paragraph_extra_b3 |
|H4ai|shortcut image label split span token| ``a![li`de\nfg`nk]a`` | test_paragraph_extra_c5 |
|H4b |shortcut link label split html token| ``a[li<de\nfg>nk]a`` | test_paragraph_extra_b4 |
|H4bi|shortcut image label split html token| ``a![li<de\nfg>nk]a`` | test_paragraph_extra_c6 |

## Unverified J

| t | s | x | y | z |
| --- | --- | --- | --- | --- |
|J1  |inline link label split before text split| `a[li<de\nfg>nk](/url)a\nb` | test_paragraph_extra_c7 |
|J1i |inline link label split before text split| `a![li<de\nfg>nk](/url)a\nb` | test_paragraph_extra_c8 |
|J2  |inline link label split before span split| `` a[li<de\nfg>nk](/url)`a\nb` `` | test_paragraph_extra_c9 |
|J2a  |inline link label before span split| `` a[li<de fg>nk](/url)`a\nb` `` | test_paragraph_extra_c9a |
|J2i |inline image label split before span split| `` a![li<de\nfg>nk](/url)`a\nb` `` | test_paragraph_extra_d0 |
|J2ai |inline image label before span split| `` a![li<de fg>nk](/url)`a\nb` `` | test_paragraph_extra_d0a |
|J3  |inline link label split before html split| `a[li<de\nfg>nk](/url)<a\nb>` | test_paragraph_extra_d1 |
|J3i |inline image label split before html split| `a![li<de\nfg>nk](/url)<a\nb>` | test_paragraph_extra_d2 |
|J4  |inline link label split before emphasis split| `a[li<de\nfg>nk](/url)*a\nb*` | test_paragraph_extra_d3 |
|J4i |inline image label split before emphasis split| `a![li<de\nfg>nk](/url)*a\nb*` | test_paragraph_extra_d4 |
|J5  |inline link label split at whitespace| `abc\n[link](\n /uri\n  "title"\n   )\n  def` | test_paragraph_extra_d5 |
|J5i  |inline image label split at whitespace| `abc\n![link](\n /uri\n  "title"\n   )\n  def` | test_paragraph_extra_d6 |
|J6  |inline link surrounded by emphasis| `abc\n*[link](/uri "title")*\ndef` | test_paragraph_extra_d7 |
|J6i |inline image surrounded by emphasis| `abc\n*![link](/uri "title")*\ndef` | test_paragraph_extra_d8 |
|J7  |inline link with emphasis in label| `abc\n[*link*](/uri "title")\ndef` | test_paragraph_extra_d9 |
|J7i |inline image with emphasis in label| `abc\n![*link*](/uri "title")\ndef` | test_paragraph_extra_e0 |
|J8  |inline link without title newline label| `a[fo\no](</my url>)a` | test_paragraph_extra_a2 |
|J8i |inline image without title newline label| `a![fo\no](</my url>)a` | test_paragraph_extra_a2 |
|J9  |inline link with split emphasis in label| `abc\n[a*li\nnk*a](/uri "title")\ndef` | test_paragraph_extra_e1 |
|J9i |inline image with split emphasis in label| `abc\n![a*li\nnk*a](/uri "title")\ndef` | test_paragraph_extra_e2 |
|J10  |inline link with emphasis in label| `abc\n[a*li nk*a](/uri "title")\ndef` | test_paragraph_extra_h3 |
|J10i |inline image with emphasis in label| `abc\n![a*li nk*a](/uri "title")\ndef` | test_paragraph_extra_h3a |
|J11  |inline link with code span in label| ``abc\n[a`li nk`a](/uri "title")\ndef`` | test_paragraph_extra_h4 |
|J11i |inline image with code span in label| ``abc\n![a`li nk`a](/uri "title")\ndef`` | test_paragraph_extra_h4a |
|J12  |inline link with raw html in label| ``abc\n[a<li nk>a](/uri "title")\ndef`` | test_paragraph_extra_h5 |
|J12i |inline image with raw html in label| ``abc\n![a<li nk>a](/uri "title")\ndef`` | test_paragraph_extra_h5a |
|J13  |inline link with URI autolink in label| ``abc\n[a<http://google.com>a](/uri "title")\ndef`` | test_paragraph_extra_h6 |
|J13i |inline image with URI autolink in label| ``abc\n![a<http://google.com>a](/uri "title")\ndef`` | test_paragraph_extra_h6a |
|J14  |inline link with email autolink in label| ``abc\n[a<li nk>a](/uri "title")\ndef`` | test_paragraph_extra_h7 |
|J14i |inline image with email autolink in label| ``abc\n![a<li nk>a](/uri "title")\ndef`` | test_paragraph_extra_h7a |
|J15  |inline link with hard break in label| ``abc\n[foo\\\ncom](/uri "title")\ndef`` | test_paragraph_extra_h8 |
|J15i |inline image with hard break in label| ``abc\n![foo\\\ncom](/uri "title")\ndef`` | test_paragraph_extra_h8a |
|J15a |inline link with hard break in label| ``abc\n[foo  \ncom](/uri "title")\ndef`` | test_paragraph_extra_h8b |
|J15ai|inline image with hard break in label| ``abc\n![foo  \ncom](/uri "title")\ndef`` | test_paragraph_extra_h8c |

## Unverified K

| t | s | x | y | z |
| --- | --- | --- | --- | --- |
|K1  |inline link with CE newline in label| `a[fo&#xa;o](/url "title")a` | test_paragraph_extra_61a |
|K1i |inline image with CE newline in label| `a![fo&#xa;o](/url "title")a` | test_paragraph_extra_61b |
|K1a |inline link with large-X CE newline in label| `a[fo&#Xa;o](/url "title")a` | test_paragraph_extra_61c |
|K1ai|inline image with large-X CE newline in label| `a![fo&#Xa;o](/url "title")a` | test_paragraph_extra_61ca |
|K1b |inline link with large-A CE newline in label| `a[fo&#xA;o](/url "title")a` | test_paragraph_extra_61h |
|K1bi|inline image with large-A CE newline in label| `a![fo&#xA;o](/url "title")a` | test_paragraph_extra_61ha |
|K1c |inline link with leading hex zeroes CE newline in label| `a[fo&#x00000a;o](/url "title")a` | test_paragraph_extra_61d |
|K1ci|inline image with leading hex zeroes CE newline in label| `a![fo&#x00000a;o](/url "title")a` | test_paragraph_extra_61da |
|K1d |inline link with decimal CE newline in label| `a[fo&#10;o](/url "title")a` | test_paragraph_extra_61e |
|K1di|inline image with decimal CE newline in label| `a![fo&#10;o](/url "title")a` | test_paragraph_extra_61ea |
|K1e |inline link with leading decimal zeroes CE newline in label| `a[fo&#0000010;o](/url "title")a` | test_paragraph_extra_61f |
|K1ei|inline image with leading decimal zeroes CE newline in label| `a![fo&#0000010;o](/url "title")a` | test_paragraph_extra_61fa |
|K1f |inline link with named CE newline in label| `a[fo&NewLine;o](/url "title")a` | test_paragraph_extra_61g |
|K1fa|inline image with named CE newline in label| `a![fo&NewLine;o](/url "title")a` | test_paragraph_extra_61ga |
|K2  |inline link with CE newline instead of pre-url ws| `a[Foo](&#xa;/uri "testing")a` | test_paragraph_extra_62d |
|K2i |inline image with CE newline instead of pre-url ws| `a![Foo](&#xa;/uri "testing")a` | test_paragraph_extra_62e |
|K3  |inline link with CE newline in url| `a[Foo](/ur&#xa;i "testing")a` | test_paragraph_extra_63a |
|K3i |inline image with CE newline in url| `a![Foo](/ur&#xa;i "testing")a` | test_paragraph_extra_63b |
|K3a |inline link with CE newline in bounded url| `a[Foo](</ur&#xa;i> "testing")a` | test_paragraph_extra_63c |
|K3ai|inline image with CE newline in bounded url| `a![Foo](</ur&#xa;i> "testing")a` | test_paragraph_extra_63d |
|K4  |inline link with CE newline instead of post-url ws| `a[Foo](/uri&#xa;"testing")a` | test_paragraph_extra_64d |
|K4i |inline image with CE newline instead of post-url ws| `a![Foo](/uri&#xa;"testing")a` | test_paragraph_extra_64e |
|K5  |inline link with CE newline in title| `a[Foo](/uri "test&#xa;ing")a` | test_paragraph_extra_66a |
|K5i |inline image with CE newline in title| `a![Foo](/uri "test&#xa;ing")a` | test_paragraph_extra_66b |
|K6  |inline link with CE newline instead of post-title ws| `a[Foo](/uri "testing"&#xa;)a` | test_paragraph_extra_67d |
|K6i |inline image with CE newline instead of post-title ws| `a![Foo](/uri "testing"&#xa;)a` | test_paragraph_extra_67e |
|K7  |full link with CE newline in label| `a[foo&#xa;bar][bar]a` | test_paragraph_extra_53b |
|K7i |full image with CE newline in label| `a![foo&#xa;bar][bar]a` | test_paragraph_extra_53c |
|K8  |full link with CE newline in reference| `a[foo][ba&#xa;r]a` | test_paragraph_extra_54b |
|K8i |full image with CE newline in reference| `a![foo][ba&#xa;r]a` | test_paragraph_extra_54c |
|K9  |shortcut link with CE newline in label| `a[ba&#xa;r]a` | test_paragraph_extra_55b |
|K9i |shortcut image with CE newline in label| `a![ba&#xa;r]a` | test_paragraph_extra_55c |
|K10 |collapsed link with CE newline in label| `a[ba&#xa;r][]a` | test_paragraph_extra_56b |
|K10i|collapsed image with CE newline in label| `a![ba&#xa;r][]a` | test_paragraph_extra_56c |
|K11 |emphasis with newline| `a*foo&#xa;bar*a` | test_paragraph_extra_46c |
|K12 |code span with newline| ` a``code&#xa;span``a ` | test_paragraph_extra_43a |
|K12a|code span with char entity newline| `` a`code &#xa; span`a `` | test_paragraph_extra_43b |
|K13 |raw html with newline| `a<raw&#xa;html='cool'>a` | test_paragraph_extra_44a |
|K13a|raw html with char entity newline 1| `a<raw &#xa; html='cool'>a` | test_paragraph_extra_44b |
|K13b|raw html with char entity newline 2| `a<raw html='cool &#xa; man'>a` | test_paragraph_extra_44c |
|K14 |URI autolink with newline| `a<http://www.&#xa;google.com>a` | test_paragraph_extra_45a |
|K15 |email autolink with newline| `a<foo@bar&#xa;.com>a` | test_paragraph_extra_46a |

## Unverified L

| t | s | x | y | z |
| --- | --- | --- | --- | --- |
|L1   |inline link within inline link| `a[foo [bar](/uri)](/uri)a` | test_paragraph_extra_e3 |
|L1i  |inline image within inline link| `a[foo ![bar](/uri)](/uri)a` | test_paragraph_extra_e3a |
|L1ii |inline image within inline image| `a![foo ![bar](/uri)](/uri)a` | test_paragraph_extra_e3b |
|L1li |inline link within inline image| `a![foo [bar](/uri)](/uri)a` | test_paragraph_extra_e3b |
|L2   |Full link w/ matching label inside of inline link| `a[foo [bar][barx]](/uri)a` | test_paragraph_extra_e4 |
|L2i  |Full image w/ matching label inside of inline link| `a[foo ![bar][barx]](/uri)a` | test_paragraph_extra_e4a |
|L2ii |Full image w/ matching label inside of inline image| `a![foo ![bar][barx]](/uri)a` | test_paragraph_extra_e4b |
|L2li |Full link w/ matching label inside of inline image| `a![foo [bar][barx]](/uri)a` | test_paragraph_extra_e4c |
|L2a  |Full link w/ matching reference inside of inline link| `a[foo [barx][bar]](/uri)a` | test_paragraph_extra_e5 |
|L2ai |Full image w/ matching reference inside of inline link| `a[foo ![barx][bar]](/uri)a` | test_paragraph_extra_e5a |
|L2aii|Full image w/ matching reference inside of inline image| `a![foo ![barx][bar]](/uri)a` | test_paragraph_extra_e5b |
|L2ali|Full link w/ matching reference inside of inline image| `a![foo [barx][bar]](/uri)a` | test_paragraph_extra_e5c |
|L3   |Collapsed link w/ matching reference inside of inline link| `a[foo [bar][]](/uri)a` | test_paragraph_extra_e6 |
|L3i  |Collapsed image w/ matching reference inside of inline link| `a[foo ![bar][]](/uri)a` | test_paragraph_extra_e6a |
|L3ii |Collapsed image w/ matching reference inside of inline image| `a![foo ![bar][]](/uri)a` | test_paragraph_extra_e6b |
|L3li |Collapsed link w/ matching reference inside of inline image| `a![foo [bar][]](/uri)a` | test_paragraph_extra_e6c |
|L3a  |Collapsed link w/o matching reference inside of inline link| `a[foo [barx][]](/uri)a` | test_paragraph_extra_e7 |
|L3ai |Collapsed image w/o matching reference inside of inline link| `a[foo ![barx][]](/uri)a` | test_paragraph_extra_e7a |
|L3aii|Collapsed image w/o matching reference inside of inline image| `a![foo ![barx][]](/uri)a` | test_paragraph_extra_e7b |
|L3ali|Collapsed link w/o matching reference inside of inline image| `a![foo [barx][]](/uri)a` | test_paragraph_extra_e7c |
|L4   |Shortcut link w/ matching reference inside of inline link| `a[foo [bar]](/uri)a` | test_paragraph_extra_e8 |
|L4i  |Shortcut image w/ matching reference inside of inline link| `a[foo ![bar]](/uri)a` | test_paragraph_extra_e8a |
|L4ii |Shortcut image w/ matching reference inside of inline image| `a![foo ![bar]](/uri)a` | test_paragraph_extra_e8b |
|L4li |Shortcut link w/ matching reference inside of inline image| `a![foo [bar]](/uri)a` | test_paragraph_extra_e8c |
|L4a  |Shortcut link w/o matching reference inside of inline link| `a[foo [barx]](/uri)a` | test_paragraph_extra_e9 |
|L4ai |Shortcut image w/o matching reference inside of inline link| `a[foo ![barx]](/uri)a` | test_paragraph_extra_e9a |
|L4aii|Shortcut image w/o matching reference inside of inline image| `a![foo ![barx]](/uri)a` | test_paragraph_extra_e9b |
|L4ali|Shortcut link w/o matching reference inside of inline image| `a![foo [barx]](/uri)a` | test_paragraph_extra_e9c |
|L5   |Inline link inside of full link| `a[foo [bar2](/url2)][bar]a` | test_paragraph_extra_f0 |
|L5i  |Inline image inside of full link| `a[foo ![bar2](/url2)][bar]a` | test_paragraph_extra_f0a |
|L5ii |Inline image inside of full image| `a![foo ![bar2](/url2)][bar]a` | test_paragraph_extra_f0b |
|L5li |Inline link inside of full image| `a![foo [bar2](/url2)][bar]a` | test_paragraph_extra_f0c |
|L6   |Full link w/ matching reference inside of full link| `a[foo [bar2][bar]][bar]a` | test_paragraph_extra_f1 |
|L6i  |Full image w/ matching reference inside of full link| `a[foo ![bar2][bar]][bar]a` | test_paragraph_extra_f1a |
|L6ii |Full image w/ matching reference inside of full image| `a![foo ![bar2][bar]][bar]a` | test_paragraph_extra_f1b |
|L6li |Full link w/ matching reference inside of full image| `a![foo [bar2][bar]][bar]a` | test_paragraph_extra_f1c |
|L6a  |Full link w/o matching reference inside of full link| `a[foo [bar][bar2]][bar]a` | test_paragraph_extra_f2 |
|L6ai |Full image w/o matching reference inside of full link| `a[foo ![bar][bar2]][bar]a` | test_paragraph_extra_f2a |
|L6aii|Full image w/o matching reference inside of full image| `a![foo ![bar][bar2]][bar]a` | test_paragraph_extra_f2b |
|L6ali|Full link w/o matching reference inside of full image| `a![foo [bar][bar2]][bar]a` | test_paragraph_extra_f2c |
|L7   |Collapsed link w/ matching reference inside of full link| `a[foo [bar2][]][bar]a` | test_paragraph_extra_f3 |
|L7i  |Collapsed image w/ matching reference inside of full link| `a[foo ![bar2][]][bar]a` | test_paragraph_extra_f3a |
|L7ii |Collapsed image w/ matching reference inside of full image| `a![foo ![bar2][]][bar]a` | test_paragraph_extra_f3b |
|L7li |Collapsed link w/ matching reference inside of full image| `a![foo [bar2][]][bar]a` | test_paragraph_extra_f3c |
|L7a  |Collapsed link w/o matching reference inside of full link| `a[foo [bar][]][bar]a` | test_paragraph_extra_f4 |
|L7ai |Collapsed image w/o matching reference inside of full link| `a[foo ![bar][]][bar]a` | test_paragraph_extra_f4a |
|L7aii|Collapsed image w/o matching reference inside of full image| `a![foo ![bar][]][bar]a` | test_paragraph_extra_f4b |
|L7ali|Collapsed link w/o matching reference inside of full image| `a![foo [bar][]][bar]a` | test_paragraph_extra_f4c |
|L8   |Shortcut link w/ matching reference inside of full link| `a[foo [bar]][bar]a` | test_paragraph_extra_f6 |
|L8i  |Shortcut image w/ matching reference inside of full link| `a[foo ![bar]][bar]a` | test_paragraph_extra_f6a |
|L8ii |Shortcut image w/ matching reference inside of full image| `a![foo ![bar]][bar]a` | test_paragraph_extra_f6b |
|L8li |Shortcut link w/ matching reference inside of full image| `a![foo [bar]][bar]a` | test_paragraph_extra_f6c |
|L8a  |Shortcut link w/o matching reference inside of full link| `a[foo [bar2]][bar]a` | test_paragraph_extra_f5 |
|L8ai |Shortcut image w/o matching reference inside of full link| `a[foo ![bar2]][bar]a` | test_paragraph_extra_f5a |
|L8aii|Shortcut image w/o matching reference inside of full image| `a![foo ![bar2]][bar]a` | test_paragraph_extra_f5b |
|L8ali|Shortcut link w/o matching reference inside of full image| `a![foo [bar2]][bar]a` | test_paragraph_extra_f5c |
|L9   |Inline link w/o matching label inside of collapsed link| `a[foo [bar2](/url2)][]a` | test_paragraph_extra_f7 |
|L9i  |Inline image w/o matching label inside of collapsed link| `a[foo ![bar2](/url2)][]a` | test_paragraph_extra_f7a |
|L9ii |Inline image w/o matching label inside of collapsed image| `a![foo ![bar2](/url2)][]a` | test_paragraph_extra_f7b |
|L9li |Inline link w/o matching label inside of collapsed image| `a![foo [bar2](/url2)][]a` | test_paragraph_extra_f7c |
|L9a  |Inline link w/ matching label inside of collapsed link| `a[foo [bar](/url2)][]a` | test_paragraph_extra_f8 |
|L9ai |Inline image w/ matching label inside of collapsed link| `a[foo ![bar](/url2)][]a` | test_paragraph_extra_f8a |
|L9aii|Inline image w/ matching label inside of collapsed image| `a![foo ![bar](/url2)][]a` | test_paragraph_extra_f8b |
|L9ali|Inline link w/ matching label inside of collapsed image| `a![foo [bar](/url2)][]a` | test_paragraph_extra_f8c |
|L10  |Full link w/ matching reference inside of collapsed link| `a[foo [bar2][bar]][]a` | test_paragraph_extra_f9 |
|L10i |Full image w/ matching reference inside of collapsed link| `a[foo ![bar2][bar]][]a` | test_paragraph_extra_f9a |
|L10ii|Full image w/ matching reference inside of collapsed image| `a![foo ![bar2][bar]][]a` | test_paragraph_extra_f9b |
|L10li|Full link w/ matching reference inside of collapsed image| `a![foo [bar2][bar]][]a` | test_paragraph_extra_f9c |
|L10a  |Full link w/o matching reference inside of collapsed link| `a[foo [bar2][bar3]][]a` | test_paragraph_extra_g0 |
|L10ai |Full image w/o matching reference inside of collapsed link| `a[foo ![bar2][bar3]][]a` | test_paragraph_extra_g0a |
|L10aii|Full image w/o matching reference inside of collapsed image| `a![foo ![bar2][bar3]][]a` | test_paragraph_extra_g0b |
|L10ali|Full link w/o matching reference inside of collapsed image| `a![foo [bar2][bar3]][]a` | test_paragraph_extra_g0c |
|L11   |Collapsed link w/ matching reference inside of collapsed link| `a[foo [bar][]][]a` | test_paragraph_extra_g2 |
|L11i  |Collapsed image w/ matching reference inside of collapsed link| `a[foo ![bar][]][]a` | test_paragraph_extra_g2a |
|L11ii |Collapsed image w/ matching reference inside of collapsed image| `a![foo ![bar][]][]a` | test_paragraph_extra_g2b |
|L11li |Collapsed link w/ matching reference inside of collapsed image| `a![foo [bar][]][]a` | test_paragraph_extra_g2c |
|L11a  |Collapsed link w/o matching reference inside of collapsed link| `a[foo [bar2][]][]a` | test_paragraph_extra_g1 |
|L11ai |Collapsed image w/o matching reference inside of collapsed link| `a[foo ![bar2][]][]a` | test_paragraph_extra_g1a |
|L11aii|Collapsed image w/o matching reference inside of collapsed image| `a![foo ![bar2][]][]a` | test_paragraph_extra_g1b |
|L11ali|Collapsed link w/o matching reference inside of collapsed image| `a![foo [bar2][]][]a` | test_paragraph_extra_g1c |
|L12   |Shortcut link w/ matching reference inside of collapsed link| `a[foo [bar]][]a` | test_paragraph_extra_g4 |
|L12i  |Shortcut image w/ matching reference inside of collapsed link| `a[foo ![bar]][]a` | test_paragraph_extra_g4a |
|L12ii |Shortcut image w/ matching reference inside of collapsed image| `a![foo ![bar]][]a` | test_paragraph_extra_g4b |
|L12li |Shortcut link w/ matching reference inside of collapsed image| `a![foo [bar]][]a` | test_paragraph_extra_g4c |
|L12a  |Shortcut link w/o matching reference inside of collapsed link| `a[foo [bar2]][]a` | test_paragraph_extra_g3 |
|L12ai |Shortcut image w/o matching reference inside of collapsed link| `a[foo ![bar2]][]a` | test_paragraph_extra_g3a |
|L12aii|Shortcut image w/o matching reference inside of collapsed image| `a![foo ![bar2]][]a` | test_paragraph_extra_g3b |
|L12ali|Shortcut link w/o matching reference inside of collapsed image| `a![foo [bar2]][]a` | test_paragraph_extra_g3c |
|L13   |Inline link w/o matching label inside of shortcut link| `a[foo [bar2](/url2)]a` | test_paragraph_extra_g5 |
|L13i  |Inline image w/o matching label inside of shortcut link| `a[foo ![bar2](/url2)]a` | test_paragraph_extra_g5a |
|L13ii |Inline image w/o matching label inside of shortcut link| `a![foo ![bar2](/url2)]a` | test_paragraph_extra_g5b |
|L13li |Inline image w/o matching label inside of shortcut link| `a![foo [bar2](/url2)]a` | test_paragraph_extra_g5c |
|L13a  |Inline link w/ matching label inside of shortcut link| `a[foo [bar](/url2)]a` | test_paragraph_extra_g6 |
|L13ai |Inline image w/ matching label inside of shortcut link| `a[foo ![bar](/url2)]a` | test_paragraph_extra_g6a |
|L13aii|Inline image w/ matching label inside of shortcut image| `a![foo ![bar](/url2)]a` | test_paragraph_extra_g6b |
|L13ali|Inline link w/ matching label inside of shortcut image| `a![foo [bar](/url2)]a` | test_paragraph_extra_g6c |
|L14  |Full link w/ matching reference inside of shortcut link| `a[foo [bar2][bar]]a` | test_paragraph_extra_g7 |
|L14i |Full image w/ matching reference inside of shortcut link| `a[foo ![bar2][bar]]a` | test_paragraph_extra_g7a |
|L14ii|Full image w/ matching reference inside of shortcut image| `a[foo ![bar2][bar]]a` | test_paragraph_extra_g7b |
|L14li|Full link w/ matching reference inside of shortcut image| `a![foo [bar2][bar]]a` | test_paragraph_extra_g7c |
|L14a  |Full link w/o matching reference inside of shortcut link| `a[foo [bar][bar]]a` | test_paragraph_extra_g8 |
|L14ai |Full image w/o matching reference inside of shortcut link| `a[foo ![bar][bar]]a` | test_paragraph_extra_g8a |
|L14aii|Full image w/o matching reference inside of shortcut image| `a![foo ![bar][bar]]a` | test_paragraph_extra_g8b |
|L14ali|Full link w/o matching reference inside of shortcut image| `a![foo [bar][bar]]a` | test_paragraph_extra_g8c |
|L15   |Collapsed link w/ matching reference inside of shortcut link| `a[foo [bar][]]a` | test_paragraph_extra_h0 |
|L15i  |Collapsed image w/ matching reference inside of shortcut link| `a[foo ![bar][]]a` | test_paragraph_extra_h0a |
|L15ii |Collapsed image w/ matching reference inside of shortcut image| `a![foo ![bar][]]a` | test_paragraph_extra_h0b |
|L15li |Collapsed image w/ matching reference inside of shortcut image| `a![foo [bar][]]a` | test_paragraph_extra_h0c |
|L15a  |Collapsed link w/o matching reference inside of shortcut link| `a[foo [bar2][]]a` | test_paragraph_extra_g9 |
|L15ai |Collapsed image w/o matching reference inside of shortcut link| `a[foo ![bar2][]]a` | test_paragraph_extra_g9a |
|L15aii|Collapsed image w/o matching reference inside of shortcut image| `a![foo ![bar2][]]a` | test_paragraph_extra_g9b |
|L15ali|Collapsed link w/o matching reference inside of shortcut image| `a![foo [bar2][]]a` | test_paragraph_extra_g9c |
|L16   |Shortcut link w/ matching reference inside of shortcut link| `a[foo [bar]]a` | test_paragraph_extra_h2 |
|L16i  |Shortcut image w/ matching reference inside of shortcut link| `a[foo ![bar]]a` | test_paragraph_extra_h2a |
|L16ii |Shortcut image w/ matching reference inside of shortcut image| `a![foo ![bar]]a` | test_paragraph_extra_h2b |
|L16li |Shortcut link w/ matching reference inside of shortcut image| `a![foo [bar]]a` | test_paragraph_extra_h2c |
|L16a  |Shortcut link w/o matching reference inside of shortcut link| `a[foo [bar2]]a` | test_paragraph_extra_h1 |
|L16ai |Shortcut image w/o matching reference inside of shortcut link| `a[foo ![bar2]]a` | test_paragraph_extra_h1a |
|L16aii|Shortcut image w/o matching reference inside of shortcut image| `a![foo ![bar2]]a` | test_paragraph_extra_h1b |
|L16ali|Shortcut link w/o matching reference inside of shortcut image| `a![foo [bar2]]a` | test_paragraph_extra_h1c |
