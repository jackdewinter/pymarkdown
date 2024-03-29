# Scenarios

Legend:

- `\a` space character
- `\\` backslash character
- `\n` newline character

L Link
I Image
nt No title in link/image
Ha Atx Heading
Hs SetExt Heading

Nl newline
S Previous element contains newline
T Text
Cs code span
Rh raw html
Em emphasis
Ua url auto
Ea email auto
Bh backslash hard break
Sh space hard break

- Series A - Starts with inline
- Series B - Contains inline
- Series C - Ends with inline
- Series D - Only inline
- Series E - Newline in the middle of inline
- Series H - Link/image with text/code span/raw html in label of various link types
- Series J - Link/image with various combinations with other inline tokens

- Series F - Link/image with newline (and whitespace) in various parts of link
- Series G - Link/image with backslash and character entity in various parts of link
- Series K - use of `&#xa;` instead of \n
- Series L - link/image inside of link/image
- Series M - lists with various leaf tokens following
- Series N - block quotes with various leaf tokens following

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

## Series H

| t | s | x | y | z |
| --- | --- | --- | --- | --- |
|HILT|inline link label split text token| `a[li\nnk](/uri "title" )a` | test_paragraph_series_h_i_l_t |
|HIIT|inline image label split text token| `a![li\nnk](/uri "title" )a` | test_paragraph_series_h_i_i_t |
|HILC|inline link label split span token| ``a[li`de\nfg`nk](/uri "title" )a`` | test_paragraph_series_h_i_l_cs |
|HIIC|inline image label split span token| ``a![li`de\nfg`nk](/uri "title" )a`` | test_paragraph_series_h_i_i_cs |
|HILR|inline link label split html token| ``a[li<de\nfg>nk](/uri "title" )a`` | test_paragraph_series_h_i_l_rh |
|HIIR|inline image label split html token| ``a![li<de\nfg>nk](/uri "title" )a`` | test_paragraph_series_h_i_i_rh |
|HFLT|full link label split text token| `a[li\nnk][bar]a` | test_paragraph_series_h_f_l_t |
|HFIT|full image label split text token| `a![li\nnk][bar]a` | test_paragraph_series_h_f_i_t |
|HFLC|full link label split span token| ``a[li`de\nfg`nk][bar]a`` | test_paragraph_series_h_f_l_cs |
|HFIC|full image label split span token| ``a![li`de\nfg`nk][bar]a`` | test_paragraph_series_h_f_i_cs |
|HFLR|full link label split html token| ``a[li<de\nfg>nk][bar]a`` | test_paragraph_series_h_f_l_rh |
|HFIR|full image label split html token| ``a![li<de\nfg>nk][bar]a`` | test_paragraph_series_h_f_i_rh |
|HCLT|collapsed link label split text token| `a[li\nnk][]a` | test_paragraph_series_h_c_l_t |
|HCIT|collapsed image label split text token| `a![li\nnk][]a` | test_paragraph_series_h_c_i_t |
|HCLC|collapsed link label split span token| ``a[li`de\nfg`nk][]a`` | test_paragraph_series_h_c_l_cs |
|HCIC|collapsed image label split span token| ``a![li`de\nfg`nk][]a`` | test_paragraph_series_h_c_i_cs |
|HCLR|collapsed link label split html token| ``a[li<de\nfg>nk][bar]a`` | test_paragraph_series_h_c_l_rh |
|HCIR|collapsed image label split html token| ``a![li<de\nfg>nk][]a`` | test_paragraph_series_h_c_i_rh |
|HSLT|shortcut link label split text token| `a[li\nnk]a` | test_paragraph_series_h_s_l_t |
|HSIT|shortcut image label split text token| `a![li\nnk]a` | test_paragraph_series_h_s_i_t |
|HSLC|shortcut link label split span token| ``a[li`de\nfg`nk]a`` | test_paragraph_series_h_s_l_cs |
|HSIC|shortcut image label split span token| ``a![li`de\nfg`nk]a`` | test_paragraph_series_h_s_i_cs |
|HSLR|shortcut link label split html token| ``a[li<de\nfg>nk]a`` | test_paragraph_series_h_s_l_rh |
|HSIR|shortcut image label split html token| ``a![li<de\nfg>nk]a`` | test_paragraph_series_h_s_i_rh |

## Series J

| t | s | x | y | z |
| --- | --- | --- | --- | --- |
|JLTT|inline link text in label| `a[foo](</my url> "title")a` | test_paragraph_series_j_l_t_t |
|JITT|inline image text in label| `a![foo](</my url>"title")a` | test_paragraph_series_j_i_t_t |
|JLntTT|inline link without title text in label| `a[foo](</my url>)a` | test_paragraph_series_j_l_nt_t_t |
|JIntTT|inline image without title text in label| `a![foo](</my url>)a` | test_paragraph_series_j_i_nt_t_t |
|JLCsT|inline link with code span in label| ``a[a`li nk`a](/uri "title")a`` | test_paragraph_series_j_l_cs_t |
|JICsT|inline image with code span in label| ``a![a`li nk`a](/uri "title")a`` | test_paragraph_series_j_i_cs_t |
|JLRhT|inline link with raw html in label| ``a[a<li nk>a](/uri "title")a`` | test_paragraph_series_j_l_rh_t |
|JIRhT|inline image with raw html in label| ``a![a<li nk>a](/uri "title")a`` | test_paragraph_series_j_i_rh_t |
|JLEmT|inline link with emphasis in label| `a[*link*](/uri "title")a` | test_paragraph_series_j_l_em_t |
|JIEmT|inline image with emphasis in label| `a![*link*](/uri "title")a` | test_paragraph_series_j_i_em_t |
|JLUaT|inline link with URI autolink in label| ``a[a<http://google.com>a](/uri "title")a`` | test_paragraph_series_j_l_ua_t |
|JIUaT|inline image with URI autolink in label| ``a![a<http://google.com>a](/uri "title")a`` | test_paragraph_series_j_i_ua_t |
|JLEaT|inline link with email autolink in label| ``a[a<foo@r.com>a](/uri "title")a`` | test_paragraph_series_j_l_ea_t |
|JIEaT|inline image with email autolink in label| ``a![a<foo@r.com>a](/uri "title")a`` | test_paragraph_series_j_i_ea_t |
|JLTST|inline link text split label| `a[fo\no](</my url> "title")a` | test_paragraph_series_j_l_t_s_t |
|JITST|inline image text split label| `a![fo\no](</my url> "title")a` | test_paragraph_series_j_i_t_s_t |
|JLntTST|inline link without title text split label| `a[fo\no](</my url>)a` | test_paragraph_series_j_l_nt_t_s_t |
|JIntTST|inline image without title text split label| `a![fo\no](</my url>)a` | test_paragraph_series_j_i_nt_t_s_t |
|JLBhST|inline link with hard break (split) in label| ``a[foo\\\ncom](/uri "title")a`` | test_paragraph_series_j_l_bh_s_t |
|JIBhST|inline image with hard break (split) in label| ``a![foo\\\ncom](/uri "title")a`` | test_paragraph_series_j_i_bh_s_t |
|JLShST|inline link with hard break (split) in label| ``a[foo  \ncom](/uri "title")a`` | test_paragraph_series_j_l_sh_t |
|JIShST|inline image with hard break (split) in label| ``a![foo  \ncom](/uri "title")a`` | test_paragraph_series_j_i_sh_t |
|JLRhST|inline link with split raw html in label| `a[li<de\nfg>nk](/url)a` | test_paragraph_series_j_l_rh_s_t |
|JIRhST|inline image with split raw html in label| `a![li<de\nfg>nk](/url)a` | test_paragraph_series_j_i_rh_s_t |
|JLEmST|inline link with split emphasis in label| `a[a*li\nnk*a](/uri "title")a` | test_paragraph_series_j_l_em_s_t |
|JIEmST|inline image with split emphasis in label| `a![a*li\nnk*a](/uri "title")a` | test_paragraph_series_j_i_em_s_t |
|JLCsST|inline link with split code span in label| ``a[a`li\nnk`a](/uri "title")a`` | test_paragraph_series_j_l_cs_s_t |
|JICsST|inline image with split code span in label| ``a![a`li\nnk`a](/uri "title")a`` | test_paragraph_series_j_i_cs_s_t |
|JLTTS|inline link text in label| `a[foo](</my url> "title")a\nb` | test_paragraph_series_j_l_t_t_s |
|JITTS|inline image text in label| `a![foo](</my url>"title")a\nb` | test_paragraph_series_j_i_t_t_s |
|JLTCs|inline link label split before span split| `` a[link](/url "title")`ab` `` | test_paragraph_series_j_l_t_cs |
|JITCs|inline link label before span split| `` a![link](/url "title")`ab` `` | test_paragraph_series_j_i_t_cs |
|JLTCsS|inline link label split before span split| `` a[link](/url "title")`a\nb` `` | test_paragraph_series_j_l_t_cs_s |
|JITCsS|inline link label before span split| `` a![link](/url "title")`a\nb` `` | test_paragraph_series_j_i_t_cs_s |
|JLTRh|inline link label split before html | `a[link](/url "title")<a\nb>` | test_paragraph_series_j_l_t_rh |
|JITRh|inline image label split before html | `a![link](/url "title")<a\nb>` | test_paragraph_series_j_i_t_rh |
|JLTRhS|inline link label split before html split| `a[link](/url "title")<a\nb>` | test_paragraph_series_j_l_t_rh_s |
|JITRhS|inline image label split before html split| `a![link](/url "title")<a\nb>` | test_paragraph_series_j_i_t_rh_s |
|JLTEm|inline link label split before emphasis| `a[link](/url "title")*a b*` | test_paragraph_series_j_l_t_em |
|JITEm|inline image label split before emphasis| `a![link](/url "title")*a b*` | test_paragraph_series_j_i_t_em |
|JLTEmS|inline link label split before emphasis split| `a[link](/url "title")*a\nb*` | test_paragraph_series_j_l_t_em_s |
|JITEmS|inline image label split before emphasis split| `a![link](/url "title")*a\nb*` | test_paragraph_series_j_i_t_em_s |
|JLTUa|inline link label split before uri autolink| `a[link](/url "title")<http://google.com>a` | test_paragraph_series_j_l_t_ua |
|JITUa|inline image label split before uri autolink| `a![link](/url "title")<http://google.com>a` | test_paragraph_series_j_i_t_ua |
|JLTEa|inline link label split before email autolink| `a[link](/url "title")<foo@r.com>a` | test_paragraph_series_j_l_t_ea |
|JITEa|inline image label split before email autolink| `a![link](/url "title")<foo@r.com>a` | test_paragraph_series_j_i_t_ea |
|JLTBh|inline link label split before backslash hardbreak| `a[link](/url "title")\\\na` | test_paragraph_series_j_l_t_bh |
|JITBh|inline image label split before backslash hardbreak| `a![link](/url "title")\\\na` | test_paragraph_series_j_i_t_bh |
|JLTSh|inline link label split before spaces hardbreak| `a[link](/url "title")   \na` | test_paragraph_series_j_l_t_sh |
|JITSh|inline image label split before spaces hardbreak| `a![link](/url "title")   \na` | test_paragraph_series_j_i_t_sh |
|JEmLTT|inline link surrounded by emphasis| `a*[link](/uri "title")*a` | test_paragraph_series_j_em_l_t_t |
|JEmITT|inline image surrounded by emphasis| `a*![link](/uri "title")*a` | test_paragraph_series_j_em_i_t_t |

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

## Series M

| t | s | x | y | z |
| --- | --- | --- | --- | --- |
|MOlNlTb        |Ordered list newline thematic break| `1.\n---\n` | test_paragraph_series_m_tb_ol_nl_tb |
|MOlNlI2Tb      |Ordered list new line indent of 2 thematic break| `1.\n  ---\n` | test_paragraph_series_m_tb_ol_nl_i2_tb |
|MOlNlI3Tb      |Ordered list new line indent of 3 thematic break| `1.\n   ---\n` | test_paragraph_series_m_tb_ol_nl_i3_tb |
|MOlTNlTb       |Ordered list text new line thematic break| `1. abc\n---\n` | test_paragraph_series_m_tb_ol_t_nl_tb |
|MOlTNlI2Tb     |Ordered list text newline indent of 2 thematic break| `1. abc\n  ---\n` | test_paragraph_series_m_tb_ol_t_nl_i2_tb |
|MOlTNlI3Tb     |Ordered list text newline indent of 3 thematic break| `1. abc\n   ---\n` test_paragraph_series_m_tb_ol_t_nl_i3_tb |
|MOlOLNlTb      |Ordered list x2 text new line thematic break| `1. 1.\n---\n` | test_paragraph_series_m_tb_ol_ol_nl_tb |
|MOlOLTNlTb     |Ordered list x2 text new line thematic break| `1. 1. abc\n---\n` | test_paragraph_series_m_tb_ol_ol_t_nl_tb |
|MOlNlOLNlTb    |Ordered list newline ordered list new line thematic break| `1.\n   1.\n---\n` | test_paragraph_series_m_tb_ol_nl_ol_nl_tb |
|MOlNlOLTNlTb   |Ordered list newline ordered list text new line thematic break| `1.\n   1. abc\n---\n` | test_paragraph_series_m_tb_ol_nl_ol_t_nl_tb |
|MOlTNlOLNlTb   |Ordered list text newline ordered list new line thematic break| `1. abc\n   1.\n---\n` | test_paragraph_series_m_tb_ol_t_nl_ol_nl_tb |
|MUlTNlUlNlTb   |Unordered list text newline unordered list new line thematic break| `- abc\n  -\n---` | test_paragraph_series_m_tb_ul_t_nl_ul_nl_tb |
|MUlTNlUlbNlTb   |Unordered list text newline unordered list (b) new line thematic break| `- abc\n  def\n  *\n---\n` | test_paragraph_series_m_tb_ul_t_nl_ulb_nl_tb |
|MOlTNlOLTNlTb  |Ordered list text newline ordered list text new line thematic break| `1. abc\n   1. abc\n---\n` | test_paragraph_series_m_tb_ol_t_nl_ol_t_nl_tb |
|MOlNlOLNlI2Tb  |Ordered list newline ordered list new line indent of 2 thematic break| `1.\n   1.\n  ---\n` | test_paragraph_series_m_tb_ol_nl_ol_nl_i2_tb |
|MOlNlOLTNlI2Tb |Ordered list newline ordered list text new line indent of 2 thematic break| `1.\n   1. abc\n  ---\n` | test_paragraph_series_m_tb_ol_nl_ol_t_nl_i2_tb |
|MOlNlOLNlI2Tb  |Ordered list text newline ordered list new line indent of 2 thematic break| `1. abc\n   1.\n  ---\n` | test_paragraph_series_m_tb_ol_t_nl_ol_nl_i2_tb |
|MUlNlULNlI1Tb  |Unordered list text newline unordered list new line indent of 1 thematic break| `- abc\n  -\n ---\n` | test_paragraph_series_m_tb_ul_t_nl_ul_nl_i1_tb |
|MUlNlULbNlI1Tb  |Unordered list text newline unordered list (b) new line indent of 1 thematic break| `- abc\n  *\n ---\n` | test_paragraph_series_m_tb_ul_t_nl_ulb_nl_i1_tb |
|MOlNlOLTNlI2Tb |Ordered list text newline ordered list text new line indent of 2 thematic break| `1. abc\n   1. abc\n  ---\n` | test_paragraph_series_m_tb_ol_t_nl_ol_t_nl_i2_tb |
|MOlNlOLNlI3Tb  |Ordered list newline ordered list new line indent of 3 thematic break| `1.\n   1.\n   ---\n` | test_paragraph_series_m_tb_ol_nl_ol_nl_i3_tb |
|MOlNlOLTNlI3Tb |Ordered list newline ordered list text new line indent of 3 thematic break| `1.\n   1. abc\n   ---\n` | test_paragraph_series_m_tb_ol_nl_ol_t_nl_i3_tb |
|MOlTNlOLNlI3Tb |Ordered list text newline ordered list new line indent of 3 thematic break| `1. abc\n   1.\n   ---\n` | test_paragraph_series_m_tb_ol_t_nl_ol_nl_i3_tb |
|MUlTNlULNlI2Tb |Unordered list text newline unordered list new line indent of 2 thematic break| `- abc\n  -\n  ---\n` | test_paragraph_series_m_tb_ul_t_nl_ul_nl_i2_tb |
|MUlTNlULbNlI2Tb |Unordered list text newline unordered list (b) new line indent of 2 thematic break| `- abc\n  *\n  ---\n` | test_paragraph_series_m_tb_ul_t_nl_ulb_nl_i2_tb |
|MOlTNlOLTNlI3Tb|Ordered list text newline ordered list text new line indent of 3 thematic break| `1. abc\n   1. abc\n   ---\n` | test_paragraph_series_m_tb_ol_t_nl_ol_t_nl_i3_tb |

| t | s | x | y | z |
| --- | --- | --- | --- | --- |
|MOlNlHaT       |Ordered list newline atx heading text| `1.\n# foo\n` | test_paragraph_series_m_ha_ol_nl_ha_t |
|MOlNlI2HaT     |Ordered list newline indent of 2 atx heading text| `1.\n  # foo\n` | test_paragraph_series_m_ha_ol_nl_i2_ha_t |
|MOlNlI3HaT     |Ordered list newline indent of 3 atx heading text| `1.\n   # foo\n` | test_paragraph_series_m_ha_ol_nl_i3_ha_t |
|MOlTNlHaT      |Ordered list text newline atx heading text| `1. abc\n# foo\n` | test_paragraph_series_m_ha_ol_t_nl_ha_t |
|MOlTNlI2HaT    |Ordered list text newline indent of 2 atx heading text| `1. abc\n  # foo\n` | test_paragraph_series_m_ha_ol_t_nl_i2_ha_t |
|MOlTNlI3HaT    |Ordered list text newline indent of 3 atx heading text| `1. abc\n   # foo\n` | test_paragraph_series_m_ha_ol_t_nl_i3_ha_t |
|MOlOLNlHaT     |Ordered list x2 newline atx heading text| `1. 1.\n# foo\n` | test_paragraph_series_m_ha_ol_ol_nl_ha_t |
|MOlOLTNlHaT    |Ordered list x2 text newline atx heading text| `1. 1. abc\n# foo\n` | test_paragraph_series_m_ha_ol_ol_t_nl_ha_t |
|MOlNlOLNlHaT   |Ordered list newline ordered list new line atx heading text| `1.\n   1.\n# foo\n` | test_paragraph_series_m_ha_ol_nl_ol_nl_ha_t |
|MOlNlOLTNlHaT  |Ordered list newline ordered list text new line atx heading text| `1.\n   1. abc\n# foo\n` | test_paragraph_series_m_ha_ol_nl_ol_t_nl_ha_t |
|MOlTNlOLNlHaT   |Ordered list text newline ordered list new line atx heading text| `1. abc\n   1.\n# foo\n` | test_paragraph_series_m_ha_ol_t_nl_ol_nl_ha_t |
|MUlTNlUlNlHaT   |Unordered list text newline unordered list new line atx heading text| `- abc\n  -\n# foo\n` | test_paragraph_series_m_ha_ul_t_nl_ul_nl_ha_t |
|MUlTNlUlbNlHaT   |Unordered list text newline unordered list (b) new line atx heading text| `- abc\n  *\n# foo\n` | test_paragraph_series_m_ha_ul_t_nl_ulb_nl_ha_t |
|MOlTNlOLTNlHaT  |Ordered list text newline ordered list text new line atx heading text| `1. abc\n   1. abc\n# foo\n` | test_paragraph_series_m_ha_ol_t_nl_ol_t_nl_ha_t |
|MOlNlOLNlI2HaT |Ordered list newline ordered list new line indent of 2 atx heading text| `1.\n   1.\n  # foo\n` | test_paragraph_series_m_ha_ol_nl_ol_nl_i2_ha_t |
|MOlNlOLTNlI2HaT|Ordered list newline ordered list text new line indent of 2 atx heading text| `1.\n   1. abc\n  # foo\n` | test_paragraph_series_m_ha_ol_nl_ol_t_nl_i2_ha_t |
|MOlTNlOLNlI2HaT |Ordered list text newline ordered list new line indent of 2 atx heading text| `1. abc\n   1.\n  # foo\n` | test_paragraph_series_m_ha_ol_t_nl_ol_nl_i2_ha_t |
|MUlTNlUlNlI1HaT |Unordered list text newline unordered list new line indent of 1 atx heading text| `- abc\n  -\n # foo\n` | test_paragraph_series_m_ha_ul_t_nl_ul_nl_i1_ha_t |
|MUlTNlUlbNlI1HaT |Unordered list text newline unordered list (b) new line indent of 1 atx heading text| `- abc\n  *\n  # foo\n` | test_paragraph_series_m_ha_ul_t_nl_ulb_nl_i2_ha_t |
|MOlTNlOLTNlI2HaT|Ordered list text newline ordered list text new line indent of 2 atx heading text| `1. abc\n   1. abc\n  # foo\n` | test_paragraph_series_m_ha_ol_t_nl_ol_t_nl_i2_ha_t |
|MOlNlOLNlI3HaT |Ordered list newline ordered list new line indent of 3 atx heading text| `1.\n   1.\n   # foo\n` | test_paragraph_series_m_ha_ol_nl_ol_nl_i3_ha_t |
|MOlNlOLTNlI3HaT|Ordered list newline ordered list text new line indent of 3 atx heading text| `1.\n   1. abc\n   # foo\n` | test_paragraph_series_m_ha_ol_nl_ol_t_nl_i3_ha_t |
|MOlTNlOLNlI3HaT |Ordered list text newline ordered list new line indent of 3 atx heading text| `1. abc\n   1.\n   # foo\n` | test_paragraph_series_m_ha_ol_t_nl_ol_nl_i3_ha_t |
|MUlTNlUlNlI2HaT |Unordered list text newline unordered list new line indent of 2 atx heading text| `- abc\n  -\n  # foo\n` | test_paragraph_series_m_ha_ul_t_nl_ul_nl_i2_ha_t |
|MUlTNlUlbNlI2HaT |Unordered list text newline unordered list (b) new line indent of 2 atx heading text| `- abc\n  *\n  # foo\n` | test_paragraph_series_m_ha_ul_t_nl_ulb_nl_i2_ha_t |
|MOlTNlOLTNlI3HaT|Ordered list text newline ordered list text new line indent of 3 atx heading text| `1. abc\n   1. abc\n   # foo\n` | test_paragraph_series_m_ha_ol_t_nl_ol_t_nl_i3_ha_t |

| t | s | x | y | z |
| --- | --- | --- | --- | --- |
|MOlNlTNlHs     |Ordered list newline text new line setext heading| `1.\nfoo\n---\n` | test_paragraph_series_m_hs_ol_nl_t_nl_hs |
|MOlNlTNlAllHs     |Ordered list newline text new line (all indented) setext heading| `1.\n   foo\n   ---` | test_paragraph_series_m_hs_ol_nl_t_nl_all_hs |
|MOlNlI2THs     |Ordered list newline indent of 2 text new line setext heading| `1.\n  foo\n---\n` | test_paragraph_series_m_hs_ol_nl_i2_t_nl_hs |
|MOlNlI3THs     |Ordered list newline indent of 3 text new line setext heading| `1.\n   foo\n---\n` | test_paragraph_series_m_hs_ol_nl_i3_t_nl_hs |
|MOlNlI3TI3Hs   |Ordered list newline indent of 3 text new line indent of 3 setext heading| `1.\n   foo\n   ---` | test_paragraph_series_m_hs_ol_nl_i3_t_nl_i3_hs |
|MOlTNlTNLHs    |Ordered list text newline text new line setext heading| `1. abc\nfoo\n---` | test_paragraph_series_m_hs_ol_t_nl_t_nl_hs |
|MOlTNlTNLAllHs    |Ordered list text newline text new line (all indented) setext heading| `1. abc\n   foo\n   ---` | test_paragraph_series_m_hs_ol_t_nl_t_nl_all_hs |
|MOlTNlI2TNlHs  |Ordered list text newline indent of 2 text new line setext heading| `1. abc\n  foo\n---` | test_paragraph_series_m_hs_ol_t_nl_i2_t_nl_hs|
|MOlTNlI3TNlHs  |Ordered list text newline indent of 3 text new line setext heading| `1. abc\n   foo\n---` | test_paragraph_series_m_hs_ol_t_nl_i3_t_nl_hs|
|MOlTNlI3TNlI3Hs|Ordered list text newline indent of 3 text new line indent of 3 setext heading| `1. abc\n   foo\n   ---` | test_paragraph_series_m_hs_ol_t_nl_i3_t_nl_i3_hs|
|MOlOLNlTNLHs   |Ordered list x2 text newline new line setext heading| `1. 1.\nfoo\n---` | test_paragraph_series_m_hs_ol_ol_nl_t_nl_hs |
|MOlOLNlTNLAllHs   |Ordered list x2 text newline new line (all indented) setext heading| `1. 1.\n      foo\n      ---` | test_paragraph_series_m_hs_ol_ol_nl_t_nl_all_hs |
|MOlOLTNlTNLHs  |Ordered list x2 text newline text new line setext heading| `1. 1. abc\nfoo\n---` | test_paragraph_series_m_hs_ol_ol_t_nl_t_nl_hs |
|MOlOLTNlTNLAllHs  |Ordered list x2 text newline text new line (all indented) setext heading| `1. 1. abc\n      foo\n      ---` | test_paragraph_series_m_hs_ol_ol_t_nl_t_nl_all_hs |
|MOlNlI3OLNlTNlHs|Ordered list newline indent of 3 ordered list new line text newline setext heading| `1.\n   1.\nfoo\n---` | test_paragraph_series_m_hs_ol_nl_i3_ol_nl_t_nl_hs |
|MOlNlI3OLTNlTNlHs|Ordered list newline indent of 3 ordered list text new line text newline setext heading| `1.\n   1. def\nfoo\n---` | test_paragraph_series_m_hs_ol_nl_i3_ol_t_nl_t_nl_hs |
|MOlTNlI3OLNlTNlHs|Ordered list text newline indent of 3 ordered list new line text newline setext heading| `1. abc\n   1.\nfoo\n---` | test_paragraph_series_m_hs_ol_t_nl_i3_ol_nl_t_nl_hs |
|MUlTNlI2UlNlTNlHs|Unordered list text newline indent of 2 unordered list new line text newline setext heading| `- abc\n  -\nfoo\n---` | test_paragraph_series_m_hs_ul_t_nl_i2_ul_nl_t_nl_hs |
|MUlTNlI2UlbNlTNlHs|Unordered list text newline indent of 2 unordered list (b) new line text newline setext heading| `- abc\n  *\nfoo\n---` | test_paragraph_series_m_hs_ul_t_nl_i2_ulb_nl_t_nl_hs |
|MOlTNlI3OLTNlTNlHs|Ordered list text newline indent of 3 ordered list text new line text newline setext heading| `1. abc\n   1. def\nfoo\n---` | test_paragraph_series_m_hs_ol_t_nl_i3_ol_t_nl_t_nl_hs |
|MOlNlI3OLNlI2TNlI2Hs|Ordered list newline indent of 3 ordered list new line indent of 2 text newline indent of 2 setext heading| `1.\n   1.\n  foo\n  ---` | test_paragraph_series_m_hs_ol_nl_i3_ol_nl_i2_t_nl_i2_hs |
|MOlNlI3OLTNlI2TNlI2Hs|Ordered list newline indent of 3 ordered list text new line indent of 2 text newline indent of 2 setext heading| `1.\n   1. def\n  foo\n  ---` | test_paragraph_series_m_hs_ol_nl_i3_ol_t_nl_i2_t_nl_i2_hs |
|MOlTNlI3OLNlI2TNlI2Hs|Ordered list text newline indent of 3 ordered list new line indent of 2 text newline indent of 2 setext heading| `1. abc\n   1.\n  foo\n  ---` | test_paragraph_series_m_hs_ol_t_nl_i3_ol_nl_i2_t_nl_i2_hs |
|MUlTNlI2UlNlI1TNlI1Hs|Unordered list text newline indent of 2 unordered list new line indent of 1 text newline indent of 1 setext heading| `- abc\n  -\n foo\n ---\n` | test_paragraph_series_m_hs_ul_t_nl_i2_ul_nl_i1_t_nl_i1_hs |
|MUlTNlI2UlbNlI1TNlI1Hs|Unordered list text newline indent of 2 unordered list (b) new line indent of 1 text newline indent of 1 setext heading| `- abc\n  *\n foo\n ---\n` | test_paragraph_series_m_hs_ul_t_nl_i2_ulb_nl_i1_t_nl_i1_hs |
|MOlTNlI3OLTNlI2TNlI2Hs|Ordered list text newline indent of 3 ordered list text new line indent of 2 text newline indent of 2 setext heading| `1. abc\n   1. def\n  foo\n  ---` | test_paragraph_series_m_hs_ol_t_nl_i3_ol_t_nl_i2_t_nl_i2_hs |
|MOlNlI3OLNlI3TNlI3Hs|Ordered list newline indent of 3 ordered list new line indent of 3 text newline indent of 3 setext heading| `1.\n   1.\n   foo\n   ---` | test_paragraph_series_m_hs_ol_nl_i3_ol_nl_i3_t_nl_i3_hs |
|MOlNlI3OLTNlI3TNlI3Hs|Ordered list newline indent of 3 ordered list text new line indent of 3 text newline indent of 3 setext heading| `1.\n   1. def\n   foo\n   ---` | test_paragraph_series_m_hs_ol_nl_i3_ol_t_nl_i3_t_nl_i3_hs |
|MOlTNlI3OLNlI3TNlI3Hs|Ordered list text newline indent of 3 ordered list new line indent of 3 text newline indent of 3 setext heading| `1. abc\n   1.\n   foo\n   ---` | test_paragraph_series_m_hs_ol_t_nl_i3_ol_nl_i3_t_nl_i3_hs |
|MUlTNlI2UlNlI2TNlI2Hs|Unordered list text newline indent of 2 unordered list new line indent of 2 text newline indent of 2 setext heading| `- abc\n  -\n  foo\n  ---\n` | test_paragraph_series_m_hs_ul_t_nl_i2_ul_nl_i2_t_nl_i2_hs |
|MUlTNlI2UlNlI2TNlI2Hs|Unordered list text newline indent of 2 unordered list (b) new line indent of 2 text newline indent of 2 setext heading| `- abc\n  *\n  foo\n  ---\n` | test_paragraph_series_m_hs_ul_t_nl_i2_ulb_nl_i2_t_nl_i2_hs |
|MOlTNlI3OLTNlI3TNlI3Hs|Ordered list text newline indent of 3 ordered list text new line indent of 3 text newline indent of 3 setext heading| `1. abc\n   1. def\n   foo\n   ---` | test_paragraph_series_m_hs_ol_t_nl_i3_ol_t_nl_i3_t_nl_i3_hs |

| t | s | x | y | z |
| --- | --- | --- | --- | --- |
|MOlNlFb        |Ordered list newline fenced block| ` 1.\n```\nfoo\n``` ` | test_paragraph_series_m_fb_ol_nl_fb |
|MOlNlAllFb        |Ordered list newline (all indented) fenced block| ````` 1.\n   ```\n   foo\n   ``` ````` | test_paragraph_series_m_fb_ol_nl_all_i3_fb |
|MOlNlI2Fb      |Ordered list newline indent of 2 fenced block| ` 1.\n  ```\nfoo\n``` ` | test_paragraph_series_m_fb_ol_nl_i2_fb |
|MOlNlI3Fb      |Ordered list newline indent of 3 fenced block| ` 1.\n   ```\nfoo\n``` ` | test_paragraph_series_m_fb_ol_nl_i3_fb |
|MOlTNlFb       |Ordered list text newline fenced block| ` 1.  abc\n```\nfoo\n``` ` | test_paragraph_series_m_fb_ol_t_nl_fb |
|MOlTNlAllFb       |Ordered list text newline (all indented) fenced block| ````` 1.\n  abc\n    ```\n    foo\n    ``` ````` | test_paragraph_series_m_fb_ol_t_nl_all_i4_fb |
|MOlTNlI2Fb     |Ordered list text newline indent of 2 fenced block| ` 1.  abc\n  ```\nfoo\n``` ` | test_paragraph_series_m_fb_ol_t_nl_i2_fb |
|MOlTNlI3Fb     |Ordered list text newline indent of 3 fenced block| ` 1.  abc\n   ```\nfoo\n``` ` | test_paragraph_series_m_fb_ol_t_nl_i3_fb |
|MOlOLNlFb      |Ordered list x2 newline fenced block| ` 1. 1.\n```\nfoo\n``` ` | test_paragraph_series_m_fb_ol_ol_nl_fb |
|MOlOLNlAllFb   |Ordered list x2 newline (all indented) fenced block| ```` 1. 1. \n     ```\n      foo\n      ``` ```` | test_paragraph_series_m_fb_ol_ol_nl_all_i6_fb |
|MOlOLTNlFb     |Ordered list x2 text newline fenced block| ` 1. 1. abc\n```\nfoo\n``` ` | test_paragraph_series_m_fb_ol_ol_t_nl_fb |
|MOlOLTNlAllFb     |Ordered list x2 text newline (all indented) fenced block| ```` 1. 1. abc\n      ```\n      foo\n      ``` ```` | test_paragraph_series_m_fb_ol_ol_t_nl_all_i6_fb |
|MOlNlI3OLNlFb  |Ordered list newline indent of 3 ordered list newline fenced block| ` 1.\n   1.\n```\nfoo\n``` ` | test_paragraph_series_m_fb_ol_nl_i3_ol_nl_fb |
|MOlNlI3OLTNlFb |Ordered list newline indent of 3 ordered list text newline fenced block| ` 1.\n   1. abc\n```\nfoo\n``` ` | test_paragraph_series_m_fb_ol_nl_i3_ol_t_nl_fb |
|MOlNlI3OLNlFb  |Ordered list text newline indent of 3 ordered list newline fenced block| ` 1. abc\n   1.\n```\nfoo\n``` ` | test_paragraph_series_m_fb_ol_t_nl_i3_ol_nl_fb |
|MUlNlI2UlNlFb  |Unordered list text newline indent of 2 unordered list newline fenced block| ` - abc\n  -\n```\nfoo\n``` ` | test_paragraph_series_m_fb_ul_t_nl_i2_ul_nl_fb |
|MUlNlI2UlbNlFb  |Unordered list text newline indent of 2 unordered list (b) newline fenced block| ` - abc\n  *\n```\nfoo\n``` ` | test_paragraph_series_m_fb_ul_t_nl_i2_ulb_nl_fb |
|MOlNlI3OLTNlFb |Ordered list text newline indent of 3 ordered list text newline fenced block| ` 1. abc\n   1. abc\n```\nfoo\n``` ` | test_paragraph_series_m_fb_ol_t_nl_i3_ol_t_nl_fb |
|MOlNlI3OLNlI2Fb|Ordered list newline indent of 3 ordered list newline indent of 2 fenced block | ` 1.\n   1.\n  ```\nfoo\n``` ` | test_paragraph_series_m_fb_ol_nl_i3_ol_nl_i2_fb |
|MOlNlI3OLTNlI2Fb|Ordered list newline indent of 3 ordered list text newline indent of 2 fenced block | ` 1.\n   1. abc\n  ```\nfoo\n``` ` | test_paragraph_series_m_fb_ol_nl_i3_ol_t_nl_i2_fb |
|MOlTNlI3OLNlI2Fb|Ordered list text newline indent of 3 ordered list newline indent of 2 fenced block | ` 1. abc\n   1.\n  ```\nfoo\n``` ` | test_paragraph_series_m_fb_ol_t_nl_i3_ol_nl_i2_fb |
|MUlTNlI2UlNlI1Fb|Unordered list text newline indent of 2 unordered list newline indent of 1 fenced block | ` - abc\n  -\n ```\nfoo\n``` ` | test_paragraph_series_m_fb_ul_t_nl_i2_ul_nl_i1_fb |
|MUlTNlI2UlbNlI1Fb|Unordered list text newline indent of 2 unordered list (b) newline indent of 1 fenced block | ` - abc\n  *\n ```\nfoo\n``` ` | test_paragraph_series_m_fb_ul_t_nl_i2_ul_nl_i1_fb |
|MOlTNlI3OLTNlI2Fb|Ordered list text newline indent of 3 ordered list text newline indent of 2 fenced block | ` 1. abc\n   1. abc\n  ```\nfoo\n``` ` | test_paragraph_series_m_fb_ol_t_nl_i3_ol_t_nl_i2_fb |
|MOlNlI3OLNlI3Fb|Ordered list newline indent of 3 ordered list newline indent of 3 fenced block| ` 1.\n   1.\n   ```\nfoo\n``` ` | test_paragraph_series_m_fb_ol_nl_i3_ol_nl_i3_fb |
|MOlNlI3OLTNlI3Fb|Ordered list newline indent of 3 ordered list text newline indent of 3 fenced block| ` 1.\n   1. abc\n   ```\nfoo\n``` ` | test_paragraph_series_m_fb_ol_nl_i3_ol_t_nl_i3_fb |
|MOlTNlI3OLNlI3Fb|Ordered list text newline indent of 3 ordered list newline indent of 3 fenced block| ` 1. abc\n   1.\n   ```\nfoo\n``` ` | test_paragraph_series_m_fb_ol_t_nl_i3_ol_nl_i3_fb |
|MUlTNlI2UlNlI2Fb|Unordered list text newline indent of 2 unordered list newline indent of 2 fenced block| ` - abc\n  -\n  ```\nfoo\n``` ` | test_paragraph_series_m_fb_ul_t_nl_i2_ul_nl_i2_fb |
|MUlTNlI2UlbNlI2Fb|Unordered list text newline indent of 2 unordered list (b) newline indent of 2 fenced block| ` - abc\n  *\n  ```\nfoo\n``` ` | test_paragraph_series_m_fb_ul_t_nl_i2_ul_nl_i2_fb |
|MOlTNlI3OLTNlI3Fb|Ordered list text newline indent of 3 ordered list text newline indent of 3 fenced block| ` 1. abc\n   1. abc\n   ```\nfoo\n``` ` | test_paragraph_series_m_fb_ol_t_nl_i3_ol_t_nl_i3_fb |

| t | s | x | y | z |
| --- | --- | --- | --- | --- |
|MI3OlNlI4TIb   |Indent of 3 ordered list newline indent of 4 text (indented block)| `   1.\n    foo` | test_paragraph_series_m_ib_i3_ol_nl_i4_t_ib |
|MI3OlNlI7TAllIb |Indent of 3 ordered list newline indent of 7 text (indented block)| `1.\n       foo` | test_paragraph_series_m_ib_i3_ol_nl_i7_t_all_ib |
|MI3OlNlI5TIb   |Indent of 3 ordered list newline indent of 5 text (indented block)| `   1.\n     foo` | test_paragraph_series_m_ib_i3_ol_nl_i5_t_ib |
|MI3OlNlI6TIb   |Indent of 3 ordered list newline indent of 6 text (indented block)| `   1.\n      foo` | test_paragraph_series_m_ib_i3_ol_nl_i6_t_fb |
|MI3OlTNlI4TIb  |Indent of 3 ordered list text newline indent of 4 text (indented block)| `   1. abc\n    foo` | test_paragraph_series_m_ib_i3_ol_t_nl_i4_t_ib |
|MI3OlTNlNlI4TAllIb  |Indent of 3 ordered list text newline indent of 4 text (indented block)| `   1. abc\n    foo` | test_paragraph_series_m_ib_i3_ol_t_nl_i4_t_all_ib |
|MI3OlTNlNlNlI4TAllIb  |Indent of 3 ordered list text newline newline indent of 4 text (indented block)| `   1. abc\n\n          foo` | test_paragraph_series_m_ib_i3_ol_t_nl_nl_i10_t_all_ib |
|MI3OlTNlI10TAllIb  |Indent of 3 ordered list text newline indent of 10 text (indented block)| `   1. abc\n          foo` | test_paragraph_series_m_ib_i3_ol_t_nl_i10_t_all_ib |
|MI3OlTNlI5TIb  |Indent of 3 ordered list text newline indent of 5 text (indented block)| `   1. abc\n     foo` | test_paragraph_series_m_ib_i3_ol_t_nl_i5_t_ib |
|MI3OlTNlI6TIb  |Indent of 3 ordered list text newline indent of 6 text (indented block)| `   1. abc\n      foo` | test_paragraph_series_m_ib_i3_ol_t_nl_i6_t_ib |
|MOlOLNlI4TIb   |Ordered list x2 newline indent of 4 text (indented block)| `1. 1.\n    foo` | test_paragraph_series_m_ib_ol_ol_nl_i4_t_ib |
|MOlOLNlI4TAllIb   |Ordered list x2 newline indent of 10 text (indented block)| `1. 1.\n    foo` | test_paragraph_series_m_ib_ol_ol_nl_i10_t_all_ib |
|MOlOLTNlI4TIb  |Ordered list x2 text newline indent of 4 text (indented block)| `1. 1. abc\n    foo` | test_paragraph_series_m_ib_ol_ol_t_nl_i4_t_ib |
|MOlOLTNlI4TAllIb  |Ordered list x2 text newline indent of 4 text (indented block)| `1. 1. abc\n          foo` | test_paragraph_series_m_ib_ol_ol_t_nl_i4_t_all_ib |
|MOlOLTNlNlI4TAllIb  |Ordered list x2 text newline newline indent of 4 text (indented block)| `1. 1. abc\n\n          foo` | test_paragraph_series_m_ib_ol_ol_t_nl_nl_i4_t_all_ib |
|MOlNlI3OLNlI4tIb|Ordered list newline indent of 3 ordered list newline indent of 4 text (indented block)| `1.\n   1.\n    foo` | test_paragraph_series_m_ib_ol_nl_i3_ol_nl_i4_t_ib |
|MOlNlI3OLTNlI4tIb|Ordered list newline indent of 3 ordered list text newline indent of 4 text (indented block)| `1.\n   1. abc\n    foo` | test_paragraph_series_m_ib_ol_nl_i3_ol_t_nl_i4_t_ib |
|MOlTNlI3OLNlI4tIb|Ordered list text newline indent of 3 ordered list newline indent of 4 text (indented block)| `1. abc\n   1.\n    foo` | test_paragraph_series_m_ib_ol_t_nl_i3_ol_nl_i4_t_ib |
|MUlTNlI2UlNlI4tIb|Unordered list text newline indent of 2 unordered list newline indent of 4 text (indented block)| `- abc\n  -\n    foo` | test_paragraph_series_m_ib_ul_t_nl_i2_ul_nl_i4_t_ib |
|MUlTNlI2UlbNlI4tIb|Unordered list text newline indent of 2 unordered list (b) newline indent of 4 text (indented block)| `- abc\n  *\n    foo` | test_paragraph_series_m_ib_ul_t_nl_i2_ul_nl_i4_t_ib |
|MOlTNlI3OLTNlI4tIb|Ordered list text newline indent of 3 ordered list text newline indent of 4 text (indented block)| `1. abc\n   1. abc\n    foo` | test_paragraph_series_m_ib_ol_t_nl_i3_ol_t_nl_i4_t_ib |
|MI3OlNlI5OLNlI4TIb |Indent of 3 ordered list newline indent of 5 ordered list newline indent of 4 text (indented block)| `   1.\n      1.\n    foo` | test_paragraph_series_m_ib_i3_ol_nl_i5_ol_nl_i4_t_ib |
|MI3OlNlI5OLTNlI4TIb |Indent of 3 ordered list newline indent of 5 ordered list text newline indent of 4 text (indented block)| `   1.\n      1. abc\n    foo` | test_paragraph_series_m_ib_i3_ol_nl_i5_ol_t_nl_i4__t_ib |
|MI3OlTNlI5OLNlI4TIb |Indent of 3 ordered list text newline indent of 5 ordered list newline indent of 4 text (indented block)| `   1. abc\n      1.\n    foo` | test_paragraph_series_m_ib_i3_ol_t_nl_i5_ol_nl_i4_t_ib |
|MI3OlTNlI5OLTNlI4TIb |Indent of 3 ordered list text newline indent of 5 ordered list text newline indent of 4 text (indented block)| `   1. abc\n      1. abc\n    foo` | test_paragraph_series_m_ib_i3_ol_t_nl_i5_ol_t_nl_i4_t_ib |
|MI1OlNlI4OLNlI4TIb |Indent of 1 ordered list  newline indent of 4 ordered list newline indent of 4 text (indented block)| ` 1.\n    1.\n    foo` | test_paragraph_series_m_ib_i1_ol_nl_i4_ol_nl_i4_t_ib |
|MI2UlNlI4UlNlI4TIb |Indent of 2 unordered list newline indent of 4 unordered list newline indent of 4 text (indented block)| `  - abc\n    -\n    foo\n` | test_paragraph_series_m_ib_i2_ul_nl_i4_ul_nl_i4_t_ib |
|MI2UlNlI4UlbNlI4TIb |Indent of 2 unordered list newline indent of 4 unordered list (b)newline indent of 4 text (indented block)| `  - abc\n    *\n    foo\n` | test_paragraph_series_m_ib_i2_ul_nl_i4_ul_nl_i4_t_ib |
|MI1OlNlI4OLTNlI4TIb |Indent of 1 ordered list newline indent of 4 ordered list text newline indent of 4 text (indented block)| ` 1.\n    1. def\n    foo` | test_paragraph_series_m_ib_i1_ol_nl_i4_ol_t_nl_i4_t_ib |
|MI1OlTNlI4OLNlI4TIb |Indent of 1 ordered list text newline indent of 4 ordered list newline indent of 4 text (indented block)| ` 1. abc\n    1.\n    foo` | test_paragraph_series_m_ib_i1_ol_t_nl_i4_ol_nl_i4_t_ib |
|MI2UlTNlI4UlNlI4TIb |Indent of 2 unordered list text newline indent of 4 unordered list newline indent of 4 text (indented block)| `  - abc\n    -\n    foo\n` | test_paragraph_series_m_ib_i2_ul_t_nl_i4_ul_nl_i4_t_ib |
|MI2UlTNlI4UlNlI4TIb |Indent of 2 unordered list text newline indent of 4 unordered list (b) newline indent of 4 text (indented block)| `  - abc\n    *\n    foo\n` | test_paragraph_series_m_ib_i2_ul_t_nl_i4_ul_nl_i4_t_ib |
|MI1OlTNlI4OLTNlI4TIb |Indent of 1 ordered list text newline indent of 4 ordered list text newline indent of 4 text (indented block)| ` 1. abc\n    1. def\n    foo` | test_paragraph_series_m_ib_i1_ol_t_nl_i4_ol_t_nl_i4_t_ib |

| t | s | x | y | z |
| --- | --- | --- | --- | --- |
|MOlNlHB        |Ordered list newline html block| `1.\n<s>\nfoo\n</s>` | test_paragraph_series_m_hb_ol_nl_hb |
|MOlNlAllHB     |Ordered list newline (all indented) html block| `1.\n   <s>\n   foo\n   </s>` | test_paragraph_series_m_hb_ol_nl_all_i3_hb |
|MOlNlI2HB      |Ordered list newline indent of 2 html block| `1.\n  <s>\nfoo\n</s>` | test_paragraph_series_m_hb_ol_nl_i2_hb |
|MOlNlI3HB      |Ordered list newline indent of 3 html block| `1.\n   <s>\nfoo\n</s>` | test_paragraph_series_m_hb_ol_nl_i3_hb |
|MOlTNlHB       |Ordered list text newline html block| `1.  abc\n<s>\nfoo\n</s>` | test_paragraph_series_m_hb_ol_t_nl_hb |
|MOlTNlAllHB    |Ordered list text newline (all indented) html block| `1.  abc\n    <s>\n    foo\n    </s>` | test_paragraph_series_m_hb_ol_t_nl_all_i4_hb |
|MOlTNlI3HB     |Ordered list text newline indent of 3 html block| `1.  abc\n   <s>\nfoo\n</s>` | test_paragraph_series_m_hb_ol_t_nl_i3_hb |
|MOlTNlI4HB     |Ordered list text newline indent of 4 html block| `1.  abc\n    <s>\nfoo\n</s>` | test_paragraph_series_m_hb_ol_t_nl_i4_hb |
|MOlOLNlHB      |Ordered list x2 newline html block| `1. 1.\n<s>\nfoo\n</s>` | test_paragraph_series_m_hb_ol_ol_nl_hb |
|MOlOLNlAllHB      |Ordered list x2 newline (all indented) html block| `1. 1. \n      <s>\n      foo\n      </s>` | test_paragraph_series_m_hb_ol_ol_nl_all_i6_hb |
|MOlOLTNlHB     |Ordered list x2 text newline html block| `1. 1. abc\n<s>\nfoo\n</s>` | test_paragraph_series_m_hb_ol_ol_t_nl_hb |
|MOlOLTNlAllHB  |Ordered list x2 text newline (all indented) html block| `1. 1. abc\n      <s>\n      foo\n      </s>` | test_paragraph_series_m_hb_ol_ol_t_nl_all_i6_hb |
|MOlNlI3OLNlHB |Ordered list newline indent of 3 ordered list newline html block| `1.\n   1.\n<s>\nfoo\n</s>` | test_paragraph_series_m_hb_ol_nl_i3_ol_nl_hb |
|MOlNlI3OLTNlHB|Ordered list newline indent of 3 ordered list text newline html block| `1.\n   1. def\n<s>\nfoo\n</s>` | test_paragraph_series_m_hb_ol_nl_i3_ol_t_nl_hb |
|MOlTNlI3OLNlHB |Ordered list text newline indent of 3 ordered list newline html block| `1. abc\n   1.\n<s>\nfoo\n</s>` | test_paragraph_series_m_hb_ol_t_nl_i3_ol_nl_hb |
|MUlTNlI2UlNlHB |Unordered list text newline indent of 2 unordered list newline html block| `- abc\n  -\n<s>\nfoo\n</s>` | test_paragraph_series_m_hb_ul_t_nl_i2_ul_nl_hb |
|MUlTNlI2UlbNlHB |Unordered list text newline indent of 2 unordered list (b) newline html block| `- abc\n  *\n<s>\nfoo\n</s>` | test_paragraph_series_m_hb_ul_t_nl_i2_ulb_nl_hb |
|MOlTNlI3OLTNlHB|Ordered list text newline indent of 3 ordered list text newline html block| `1. abc\n   1. def\n<s>\nfoo\n</s>` | test_paragraph_series_m_hb_ol_t_nl_i3_ol_t_nl_hb |
|MOlNlI3OLNlI2HB|Ordered list newline indent of 3 ordered list newline indent of 2 html block| `1.\n   1.\n  <s>\nfoo\n</s>` | test_paragraph_series_m_hb_ol_nl_i3_ol_nl_i2_hb |
|MOlNlI3OLTNlI2HB|Ordered list newline indent of 3 ordered list text newline indent of 2 html block| `1.\n   1. def\n  <s>\nfoo\n</s>` | test_paragraph_series_m_hb_ol_nl_i3_ol_t_nl_i2_hb |
|MOlTNlI3OLNlI2HB|Ordered list text newline indent of 3 ordered list newline indent of 2 html block| `1. abc\n   1.\n  <s>\nfoo\n</s>` | test_paragraph_series_m_hb_ol_t_nl_i3_ol_nl_i2_hb |
|MUlTNlI2UlNlI1HB|Unordered list text newline indent of 2 unordered list newline indent of 1 html block| `- abc\n  -\n <s>\nfoo\n</s>\n` | test_paragraph_series_m_hb_ul_t_nl_i2_ul_nl_i1_hb |
|MUlTNlI2UlbNlI1HB|Unordered list text newline indent of 2 unordered list (b) newline indent of 1 html block| `- abc\n  *\n <s>\nfoo\n</s>\n` | test_paragraph_series_m_hb_ul_t_nl_i2_ulb_nl_i1_hb |
|MOlTNlI3OLTNlI2HB|Ordered list text newline indent of 3 ordered list text newline indent of 2 html block| `1. abc\n   1. def\n  <s>\nfoo\n</s>` | test_paragraph_series_m_hb_ol_t_nl_i3_ol_t_nl_i2_hb |
|MOlNlI3OLNlI3HB|Ordered list newline indent of 3 ordered list newline indent of 3 html block| `1.\n   1.\n   <s>\nfoo\n</s>` | test_paragraph_series_m_hb_ol_nl_i3_ol_nl_i3_hb |
|MOlNlI3OLTNlI3HB|Ordered list newline indent of 3 ordered list text newline indent of 3 html block| `1.\n   1. def\n   <s>\nfoo\n</s>` | test_paragraph_series_m_hb_ol_t_nl_i3_ol_t_nl_i3_hb |
|MOlTNlI3OLNlI3HB|Ordered list text newline indent of 3 ordered list newline indent of 3 html block| `1. abc\n   1.\n   <s>\nfoo\n</s>` | test_paragraph_series_m_hb_ol_t_nl_i3_ol_nl_i3_hb |
|MUlTNlI2UlNlI2HB|Unordered list text newline indent of 2 unordered list newline indent of 2 html block| `- abc\n  -\n  <s>\nfoo\n</s>\n` | test_paragraph_series_m_hb_ul_t_nl_i2_ul_nl_i2_hb |
|MUlTNlI2UlbNlI2HB|Unordered list text newline indent of 2 unordered list (b) newline indent of 2 html block| `- abc\n  *\n  <s>\nfoo\n</s>\n` | test_paragraph_series_m_hb_ul_t_nl_i2_ulb_nl_i2_hb |
|MOlTNlI3OLTNlI3HB|Ordered list text newline indent of 3 ordered list text newline indent of 3 html block| `1. abc\n   1. def\n   <s>\nfoo\n</s>` | test_paragraph_series_m_hb_ol_t_nl_i3_ol_t_nl_i3_hb |

## Series N

| t | s | x | y | z |
| --- | --- | --- | --- | --- |
|NBqTNlBqT          |block quote text newline block quote text| `> u\n> x` | test_paragraph_series_n_bq_t_nl_bq_t |
|NBqTNlI2T          |block quote text newline indent of 2 text| `> u\n  x` | test_paragraph_series_n_bq_t_nl_i2_t |
|NUlTNlI2BqTNlI2BqT |unordered list text newline indent of 2 block quote text newline indent of 2 block quote text| `* a\n  > u\n  > x\n* d` | test_paragraph_series_n_ul_t_nl_i2_bq_t_nl_i2_bq_t |
|NUlTNlI2BqTNlI4T   |unordered list text newline indent of 2 block quote text newline indent of 4 text| `* a\n  > u\n    x\n* d` | test_paragraph_series_n_ul_t_nl_i2_bq_t_nl_i4_t |

| t | s | x | y | z |
| --- | --- | --- | --- | --- |
|NBqTNlBqHa         |block quote text newline block quote atx heading| `> u\n> # h` | test_paragraph_series_n_bq_t_nl_bq_ha |
|NBqTNlI2Ha         |block quote text newline indent of 2 atx heading| `> u\n  # h` | test_paragraph_series_n_bq_t_nl_i2_ha |
|NUlTNlI2BqTNlI2BqHa|unordered list text newline indent of 2 block quote text newline indent of 2 block quote atx heading| `* a\n  > u\n  > # h\n* d` | test_paragraph_series_n_ul_t_nl_i2_bq_t_nl_i2_bq_ha |
|NUlTNlI2BqTNlI4Ha   |unordered list text newline indent of 2 block quote text newline indent of 4 atx heading| `* a\n  > u\n    # h\n* d` | test_paragraph_series_n_ul_t_i2_bq_t_nl_i4_ha |

| t | s | x | y | z |
| --- | --- | --- | --- | --- |
|NBqTNlBqTb         |block quote text newline block quote thematic break| `> u\n> ---` | test_paragraph_series_n_bq_t_nl_bq_tb |
|NBqTNlI2Tb         |block quote text newline indent of 2 thematic break| `> u\n  ---` | test_paragraph_series_n_bq_t_nl_i2_tb |
|NUlTNlI2BqTNlI2BqTb|unordered list text newline indent of 2 block quote text newline indent of 2 block quote thematic break| `* a\n  > u\n  > ---\n* d` | test_paragraph_series_n_ul_t_nl_i2_bq_t_nl_i2_bq_tb |
|NUlTNlI2BqTNlI4Tb  |unordered list text newline indent of 2 block quote text newline indent of 4 thematic break| `* a\n  > u\n    ---\n* d` | test_paragraph_series_n_ul_t_nl_i2_bq_t_nl_i4_tb |

| t | s | x | y | z |
| --- | --- | --- | --- | --- |
|NBqTNlBqHb         |block quote text newline block quote html block| `> u\n> <!-- c -->` | test_paragraph_series_n_bq_t_nl_bq_hb |
|NBqTNlI2Hb         |block quote text newline indent of 2 html block| `> u\n  <!-- c -->` | test_paragraph_series_n_bq_t_nl_i2_hb |
|NUlTNlI2BqTNlI2BqHb|unordered list text newline indent of 2 block quote text newline indent of 2 block quote html break| `* a\n  > u\n  > <!-- c -->\n* d` | test_paragraph_series_n_ul_t_nl_i2_bq_t_nl_i2_bq_hb |
|NUlTNlI2BqTNlI4Hb  |unordered list text newline indent of 2 block quote text newline indent of 4 html block| `* a\n  > u\n    <!-- c -->\n* d` | test_paragraph_series_n_ul_t_nl_i2_bq_t_nl_i4_hb |

| t | s | x | y | z |
| --- | --- | --- | --- | --- |
|NBqTNlBqFb         |block quote text newline block quote fenced code block| ```` > u\n> ```> d\n> ``` ```` | test_paragraph_series_n_bq_t_nl_bq_fb |
|NBqTNlI2Fb         |block quote text newline indent of 2 fenced code block| ```` > u\n  ```\n  d\n  ``` ```` |test_paragraph_series_n_bq_t_nl_i2_fb |
|NUlTNlI2BqTNlI2BqFb|unordered list text newline indent of 2 block quote text newline indent of 2 block quote fenced code block| ```` * a\n  > u\n  > ```\n  > d\n  > \n```\n* d ```` | test_paragraph_series_n_ul_t_nl_i2_bq_t_nl_i2_bq_fb |
|NUlTNlI2BqTNlI4Fb  |unordered list text newline indent of 2 block quote text newline indent of 4 fenced code block| ```` * a\n  > u\n    ```\n    d\n    ```\n* d ```` | test_paragraph_series_n_ul_t_nl_i2_bq_t_nl_i4_fb |
|NBqTNlBqFbBqOnly1  |block quote text newline block quote fenced code block with block quote only on first| ```` > ```\nfoo\n``` ```` | test_block_quotes_215 |
|NBqTNlBqFbWBq      |block quote text newline block quote fenced code block newlines with block quote| ```` > u\n> ```\n>\n> d\n>\n> ``` ```` | test_paragraph_series_n_bq_t_nl_bq_fb_nl_with_bq |
|NBqTNlBqFbWoBq      |block quote text newline block quote fenced code block newlines without block quote| ```` > u\n> ```\n\n> d\n\n> ``` ```` | test_paragraph_series_n_bq_t_nl_bq_fb_nl_without_bq |

| t | s | x | y | z |
| --- | --- | --- | --- | --- |
|NBqTNlBqIb         |block quote text newline block quote indented block| ` > u\n>     d ` | test_paragraph_series_n_bq_t_nl_bq_ib |
|NBqTNlBqNlBqIb     |block quote text newline block quote newline block quote indented block| `> u\n>\n>     d` | test_paragraph_series_n_bq_t_nl_bq_nl_bq_ib |
|NBqTNlI6Ib         |block quote text newline indent of 6 indented block| ` > u\n      d` | test_paragraph_series_n_bq_t_nl_i6_ib |
|NBqTNlNlI6Ib         |block quote text newline newline indent of 6 indented block| `> u\n\n      d` | test_paragraph_series_n_bq_t_nl_nl_nl_i6_ib |
|NUlTNlI2BqTNlI2BqIb|unordered list text newline indent of 2 block quote text newline indent of 2 block quote indented block| `* a\n  > u\n  >     d\n* d` | test_paragraph_series_n_ul_t_nl_i2_bq_t_nl_i2_bq_ib |
|NUlTNlI2BqTNlI2BqIb|unordered list text newline indent of 2 block quote text newline indent of 2 block quote indented block| `* a\n  > u\n  >\n  >     d\n* d` | test_paragraph_series_n_ul_t_nl_i2_bq_t_nl_bq_nl_i2_bq_ib |
|NUlTNlI2BqTNlI6Ib  |unordered list text newline indent of 2 block quote text newline indent of 4 indented block| `* a\n  > u\n      d\n* d` | test_paragraph_series_n_ul_t_nl_i2_bq_t_nl_i6_ib |
|NUlTNlI2BqTNlNlI4Ib  |unordered list text newline indent of 2 block quote text newline newline indent of 4 indented block| `* a\n  > u\n\n      d\n* d` | test_paragraph_series_n_ul_t_nl_i2_bq_t_nl_nl_i6_ib |
|NBqTNlBqIbBqOnly1  |block quote text newline block quote indented code block with block quote only on first| `>     foo\n    bar` | test_block_quotes_214 |
|NBqI4TNlBqI4NlT    |block quote indent of 4 text newline block quote indent of 4 text| `>     foo\n>     bar` | test_paragraph_series_n_bq_i4_t_nl_bq_i4_t |
|NBqI4TNlBqI3NlT    |block quote indent of 4 text newline block quote indent of 3 text| `>     foo\n>    bar` | test_paragraph_series_n_bq_i4_t_nl_bq_i3_t |
|NBqI4TNlNlBqI4NlT    |block quote indent of 4 text newline newline block quote indent of 4 text| `>     foo\n\n>     bar` | test_paragraph_series_n_bq_i4_t_nl_nl_bq_i4_t |
|NBqI4TNlBqNlBqI4NlT    |block quote indent of 4 text newline block quote newline block quote indent of 4 text| `>     foo\n>\n>     bar` | test_paragraph_series_n_bq_i4_t_nl_bq_nl_bq_i4_t |

Orphan?
|J5  |inline link label split at whitespace| `abc\n[link](\n /uri\n  "title"\n   )\n  def` | test_paragraph_extra_d5 |
|J5i  |inline image label split at whitespace| `abc\n![link](\n /uri\n  "title"\n   )\n  def` | test_paragraph_extra_d6 |
