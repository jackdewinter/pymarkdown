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
- Series L - link inside of link

| t | s | x | y | z |
| -- | --- | --- | --- | --- |
| Ab | starts with a backslash escape | `\\\\this is a fun day` | test_paragraph_extra_01 |
| Abh | starts with a backslash hard line break | `\\\n` | test_paragraph_extra_02 |
| Ash | starts with spaces hard line break | `\a\a\a\n---` | test_paragraph_extra_03 |
| Acs | starts with a code span | `` `this` is a fun day `` | test_paragraph_extra_04 |
| Acr | starts with a character reference | `&amp; the band played on` | test_paragraph_extra_05 |
| Arh | starts with a raw html | `<there it='is'>, really` | test_paragraph_extra_06 |
| Aua | starts with an URI autolink | `<http://google.com> to look` | test_paragraph_extra_07 |
| Aea | starts with an email autolink | `<foo@r.com> for info` | test_paragraph_extra_08 |
| Ae | starts with an emphasis | `*it's* me!` | test_paragraph_extra_09 |
| Al | starts with a link | `[Foo](/uri "t") is a link` | test_paragraph_extra_10 |
| Ai | starts with an image | `![foo](/url "t") is an image` | test_paragraph_extra_11 |

| t | s | x | y | z |
| --- | --- | --- | --- | --- |
| Bb | contains a backslash | `a \\\\fun\\\\ day` | test_paragraph_extra_12 |
| Bcs | contains a code span | `a ``fun`` day` | test_paragraph_extra_13 |
| Bcr | contains a character reference | `fun &amp; joy` | test_paragraph_extra_14 |
| Brh | contains a raw html | `where <there it='is'> it` | test_paragraph_extra_15 |
| Bua | contains an URI autolink | `look <http://www.com> for` | test_paragraph_extra_16 |
| Bea | contains an email autolink | `email <foo@bar.com> for` | test_paragraph_extra_17 |
| Be | contains emphasis | `really! *it's me!* here!` | test_paragraph_extra_18 |
| Bl | contains a link | `at [Foo](/uri "t") more` | test_paragraph_extra_19 |
| Bi | contains an image | `my ![foo](/url "t") image` | test_paragraph_extra_20 |

| t | s | x | y | z |
| --- | --- | --- | --- | --- |
|Cb |ends with a backslash | `a fun day\\\\` | test_paragraph_extra_21 |
|Cbh|ends with a backslash hard line break | `this was \\\n` | test_paragraph_extra_22 |
|Csh|ends with spaces hard line break | `no line break?\a\a\a\n` | test_paragraph_extra_23 |
|Ccs|ends with a code span | ` a fun ``day`` ` | test_paragraph_extra_24 |
|Ccr|ends with a character reference | `played on &amp;` | test_paragraph_extra_25 |
|Crh|ends with a raw html | `really, <there it='is'>` | test_paragraph_extra_26 |
|Cua |ends with an URI autolink | `at <http://www.google.com>` | test_paragraph_extra_27 |
|Cea |ends with an email autolink | `contact <foo@bar.com>` | test_paragraph_extra_28 |
|Ce  |ends with an emphasis | `it's *me*` | test_paragraph_extra_29 |
|Cl  |ends with a link | `like [Foo](/uri)` | test_paragraph_extra_30 |
|Ci  |ends with an image | `an ![foo](/url "t")` | test_paragraph_extra_31 |

| t | s | x | y | z |
| --- | --- | --- | --- | --- |
|Db  |only a backslash| `\\\\` | test_paragraph_extra_32 |
|Dbh |only backslash hard line break| ` \\\n` | test_paragraph_extra_33 |
|Dsh |only spaces hard line break| `\a\a\a\a\n` | test_paragraph_extra_34 |
|Dcs |only code span| ` ``day`` ` | test_paragraph_extra_35 |
|Dcr |only character reference| `&amp;` | test_paragraph_extra_36 |
|Drh |only raw html (html block)| `<there it='is'>` | test_paragraph_extra_37 |
|Dua |only an URI autolink| `<http://www.google.com>` | test_paragraph_extra_38 |
|Dea |only an email autolink| `<foo@bar.com>` | test_paragraph_extra_39 |
|De  |only an emphasis| `*me*` | test_paragraph_extra_40 |
|Dl  |only a link no title| `[Foo](/uri)` | test_paragraph_extra_41 |
|Di  |only an image no title| `![foo](/url)` | test_paragraph_extra_41a |
|Dlt |only a link & title| `[Foo](/uri "title")` | test_paragraph_extra_42a |
|Dit |only an image & title| `![foo](/url "title")` | test_paragraph_extra_42 |

| t | s | x | y | z |
| --- | --- | --- | --- | --- |
|Ecs |code span with newline| ` a``code\nspan``a ` | test_paragraph_extra_43 |
|Erh |raw html with newline| `a<raw\nhtml='cool'>a` | test_paragraph_extra_44 |
|Eua |URI autolink with newline| `a<http://www.\ngoogle.com>a` | test_paragraph_extra_45 |
|Eea |email autolink with newline| `a<foo@bar\n.com>a` | test_paragraph_extra_46 |
|Eem |emphasis with newline| `a*foo\nbar*a` | test_paragraph_extra_46b |

| t | s | x | y | z |
| --- | --- | --- | --- | --- |
|F1  |inline link with newline in link label| `a[Fo\no](/uri "testing")a` | test_paragraph_extra_47 |
|F1i |inline image with newline in link label| `a![Fo\no](/uri "title")a` | test_paragraph_extra_61 |
|F2  |inline link with newline in pre-url| `a[Foo](\n/uri "testing")a` | test_paragraph_extra_48x |
|F2i |inline image with newline in pre-url| `a![Foo](\n/uri "testing")a` | test_paragraph_extra_62 |
|F2a |F2 with whitespace before newline| `a[Foo](\a\a\n/uri "testing")a` | test_paragraph_extra_48a |
|F2ai|F2i with whitespace before newline| `a![Foo](\a\a\n/uri "testing")a` | test_paragraph_extra_62a |
|F2b |F2 with whitespace after newline| `a[Foo](\n   /uri "testing")a` | test_paragraph_extra_48b |
|F2bi|F2i with whitespace after newline| `a![Foo](\n   /uri "testing")a` | test_paragraph_extra_62b |
|F2c |F2 with whitespace before & after newline| `a[Foo](  \n   /uri "testing")a` | test_paragraph_extra_48c |
|F2ci|F2i with whitespace before & after newline| `a![Foo](  \n   /uri "testing")a` | test_paragraph_extra_62c |
|F3  |inline link with newline in url (invalid) | `a[Foo](/ur\ni "testing")a` | test_paragraph_extra_49 |
|F3i |inline image with newline in url (invalid) | `a![Foo](/ur\ni "title")a` | test_paragraph_extra_63 |
|F4  |inline link with newline in post-url | `a[Foo](/uri\a\n"testing")a` | test_paragraph_extra_50x |
|F4i |inline image with newline in post-url | `a![Foo](/uri\a\n"testing")a` | test_paragraph_extra_64x |
|F4a |F4 with whitespace before newline | `a[Foo](/uri\a\a\n"testing")a` | test_paragraph_extra_50a |
|F4ai|F4i with whitespace before newline | `a![Foo](/uri\a\a\n"testing")a` | test_paragraph_extra_64a |
|F4b |F4 with whitespace after newline | `a[Foo](/uri\n   "testing")a` | test_paragraph_extra_50b |
|F4bi|F4i with whitespace after newline | `a![Foo](/uri\n   "testing")a` | test_paragraph_extra_64b |
|F4c |F4 with whitespace before & after newline | `a[Foo](/uri\a\a\n   "testing")a` | test_paragraph_extra_50c |
|F4ci|F4i with whitespace before & after newline | `a![Foo](/uri\a\a\n   "testing")a` | test_paragraph_extra_64c |
|F5  |inline link with newline in title| `a[Foo](/uri "test\ning")a` | test_paragraph_extra_51 |
|F5i |inline image with newline in title| `a![Foo](/uri "test\ning")a` | test_paragraph_extra_66 |
|F6  |inline link with newline in post-title| `a[Foo](/uri "testing"\n)a` | test_paragraph_extra_52x |
|F6i |inline image with newline in post-title| `a![Foo](/uri "testing"\n)a` | test_paragraph_extra_67 |
|F6a |F6 with whitespace before newline| `a[Foo](/uri "testing"\a\a\n)a` | test_paragraph_extra_52a |
|F6ai|F6i with whitespace before newline| `a![Foo](/uri "testing"\a\a\n)a` | test_paragraph_extra_67a |
|F6b |F6 with whitespace after newline| `a[Foo](/uri "testing"\n  )a` | test_paragraph_extra_52b |
|F6bi|F6i with whitespace after newline| `a![Foo](/uri "testing"\n  )a` | test_paragraph_extra_67b |
|F6c |F6 with whitespace before & after newline| `a[Foo](/uri "testing"\a\a\n  )a` | test_paragraph_extra_52c |
|F6ci|F6i with whitespace before & after newline| `a![Foo](/uri "testing"\a\a\n  )a` | test_paragraph_extra_67c |
|F7  |inline link with newline in label no title| `a[Fo\no](/uri)a` | test_paragraph_extra_60 |
|F7i |inline image with newline in label no title| `a![Fo\no](/uri)a` | test_paragraph_extra_60a |
|F8  |inline link with newline in post-url no title| `a[Foo](/uri\n)a` | test_paragraph_extra_65a |
|F8i |inline image with newline in post-url no title| `a![Foo](/uri\n)a` | test_paragraph_extra_65 |
|F9i |inline image with newline in preface (link)| `a!\n[Foo](/uri "testing")a` | test_paragraph_extra_59 |
|F10 |full link with newline in link label| `a[foo\nbar][bar]a` | test_paragraph_extra_53 |
|F10i|full image with newline in link label| `a![foo\nbar][bar]a` | test_paragraph_extra_53a |
|F11 |full link with newline in link reference| `a[foo][ba\nr]a` | test_paragraph_extra_54 |
|F11i|full image with newline in link reference| `a![foo][ba\nr]a` | test_paragraph_extra_54a |
|F12 |full link with newline starting link reference| `a[foo][\nbar]a` | test_paragraph_extra_58 |
|F12i|full image with newline starting link reference| `a![foo][\nbar]a` | test_paragraph_extra_58a |
|F20 |shortcut link with newline in link label| `a[ba\nr]a` | test_paragraph_extra_55 |
|F20i|shortcut image with newline in link label| `a![ba\nr]a` | test_paragraph_extra_55a |
|F30 |collapsed link with newline in link label| `a[ba\nr][]a` | test_paragraph_extra_56 |
|F30i|collapsed image with newline in link label| `a![ba\nr][]a` | test_paragraph_extra_56a |
|F31 |collapsed link with newline starting link label| `a[\nbar][]a` | test_paragraph_extra_57 |
|F31i|collapsed image with newline starting link label  | `a![\nbar][]a` | test_paragraph_extra_57a |

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

| t | s | x | y | z |
| --- | --- | --- | --- | --- |
|J1  |inline link label split before text split| `a[li<de\nfg>nk](/url)a\nb` | test_paragraph_extra_c7 |
|J1i |inline link label split before text split| `a![li<de\nfg>nk](/url)a\nb` | test_paragraph_extra_c8 |
|J2  |inline link label split before span split| `` a[li<de\nfg>nk](/url)`a\nb` `` | test_paragraph_extra_c9 |
|J2i |inline image label split before span split| `` a![li<de\nfg>nk](/url)`a\nb` `` | test_paragraph_extra_d0 |
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

| t | s | x | y | z |
| --- | --- | --- | --- | --- |
|L1  |inline link within inline link| `a[foo [bar](/uri)](/uri)a` | test_paragraph_extra_e3 |
|L1i  |inline image within inline link| `a[foo ![bar](/uri)](/uri)a` | test_paragraph_extra_e3a |
|L2  |Full link w/ matching label inside of inline link| `a[foo [bar][barx]](/uri)a` | test_paragraph_extra_e4 |
|L2i |Full image w/ matching label inside of inline link| `a[foo ![bar][barx]](/uri)a` | test_paragraph_extra_e4a |
|L2a |Full link w/ matching reference inside of inline link| `a[foo [barx][bar]](/uri)a` | test_paragraph_extra_e5 |
|L2ai|Full image w/ matching reference inside of inline link| `a[foo ![barx][bar]](/uri)a` | test_paragraph_extra_e5a |
|L3  |Collapsed link w/ matching reference inside of inline link| `a[foo [bar][]](/uri)a` | test_paragraph_extra_e6 |
|L3i |Collapsed image w/ matching reference inside of inline link| `a[foo ![bar][]](/uri)a` | test_paragraph_extra_e6a |
|L3a |Collapsed link w/o matching reference inside of inline link| `a[foo [barx][]](/uri)a` | test_paragraph_extra_e7 |
|L3ai|Collapsed image w/o matching reference inside of inline link| `a[foo [barx][]](/uri)a` | test_paragraph_extra_e7a |
|L4  |Shortcut link w/ matching reference inside of inline link| `a[foo [bar]](/uri)a` | test_paragraph_extra_e8 |
|L4i |Shortcut image w/ matching reference inside of inline link| `a[foo ![bar]](/uri)a` | test_paragraph_extra_e8a |
|L4a |Shortcut link w/o matching reference inside of inline link| `a[foo [barx]](/uri)a` | test_paragraph_extra_e9 |
|L4ai|Shortcut image w/o matching reference inside of inline link| `a[foo ![barx]](/uri)a` | test_paragraph_extra_e9a |
|L5  |Inline link inside of full link| `a[foo [bar2](/url2)][bar]a` | test_paragraph_extra_f0 |
|L5i |Inline image inside of full link| `a[foo ![bar2](/url2)][bar]a` | test_paragraph_extra_f0a |
|L6  |Full link w/ matching reference inside of full link| `a[foo [bar2][bar]][bar]a` | test_paragraph_extra_f1 |
|L6i |Full image w/ matching reference inside of full link| `a[foo ![bar2][bar]][bar]a` | test_paragraph_extra_f1a |
|L6a |Full link w/o matching reference inside of full link| `a[foo [bar][bar2]][bar]a` | test_paragraph_extra_f2 |
|L6ai|Full image w/o matching reference inside of full link| `a[foo ![bar][bar2]][bar]a` | test_paragraph_extra_f2a |
|L7  |Collapsed link w/ matching reference inside of full link| `a[foo [bar2][]][bar]a` | test_paragraph_extra_f3 |
|L7i |Collapsed image w/ matching reference inside of full link| `a[foo ![bar2][]][bar]a` | test_paragraph_extra_f3a |
|L7a |Collapsed link w/o matching reference inside of full link| `a[foo [bar][]][bar]a` | test_paragraph_extra_f4 |
|L7ai |Collapsed image w/o matching reference inside of full link| `a[foo ![bar][]][bar]a` | test_paragraph_extra_f4a |
|L8  |Shortcut link w/ matching reference inside of full link| `a[foo [bar]][bar]a` | test_paragraph_extra_f6 |
|L8i |Shortcut link w/ matching reference inside of full link| `a[foo [bar]][bar]a` | test_paragraph_extra_f6a |
|L8a |Shortcut link w/o matching reference inside of full link| `a[foo [bar2]][bar]a` | test_paragraph_extra_f5 |
|L8ai|Shortcut image w/o matching reference inside of full link| `a[foo ![bar2]][bar]a` | test_paragraph_extra_f5a |
|L9  |Inline link w/o matching label inside of collapsed link| `a[foo [bar2](/url2)][]a` | test_paragraph_extra_f7 |
|L9i |Inline image w/o matching label inside of collapsed link| `a[foo ![bar2](/url2)][]a` | test_paragraph_extra_f7a |
|L9a |Inline link w/ matching label inside of collapsed link| `a[foo [bar](/url2)][]a` | test_paragraph_extra_f8 |
|L9ai|Inline image w/ matching label inside of collapsed link| `a[foo ![bar](/url2)][]a` | test_paragraph_extra_f8a |
|L10  |Full link w/ matching reference inside of collapsed link| `a[foo [bar2][bar]][]a` | test_paragraph_extra_f9 |
|L10i |Full image w/ matching reference inside of collapsed link| `a[foo ![bar2][bar]][]a` | test_paragraph_extra_f9a |
|L10a |Full link w/o matching reference inside of collapsed link| `a[foo [bar2][bar3]][]a` | test_paragraph_extra_g0 |
|L10ai|Full image w/o matching reference inside of collapsed link| `a[foo ![bar2][bar3]][]a` | test_paragraph_extra_g0a |
|L11  |Collapsed link w/ matching reference inside of collapsed link| `a[foo [bar][]][]a` | test_paragraph_extra_g2 |
|L11i |Collapsed image w/ matching reference inside of collapsed link| `a[foo ![bar][]][]a` | test_paragraph_extra_g2a |
|L11a |Collapsed link w/o matching reference inside of collapsed link| `a[foo [bar2][]][]a` | test_paragraph_extra_g1 |
|L11ai|Collapsed image w/o matching reference inside of collapsed link| `a[foo ![bar2][]][]a` | test_paragraph_extra_g1a |
|L12  |Shortcut link w/ matching reference inside of collapsed link| `a[foo [bar]][]a` | test_paragraph_extra_g4 |
|L12i |Shortcut image w/ matching reference inside of collapsed link| `a[foo ![bar]][]a` | test_paragraph_extra_g4a |
|L12a |Shortcut link w/o matching reference inside of collapsed link| `a[foo [bar2]][]a` | test_paragraph_extra_g3 |
|L12ai|Shortcut image w/o matching reference inside of collapsed link| `a[foo ![bar2]][]a` | test_paragraph_extra_g3a |
|L13  |Inline link w/o matching label inside of shortcut link| `a[foo [bar2](/url2)]a` | test_paragraph_extra_g5 |
|L13  |Inline image w/o matching label inside of shortcut link| `a[foo ![bar2](/url2)]a` | test_paragraph_extra_g5a |
|L13a |Inline link w/ matching label inside of shortcut link| `a[foo [bar](/url2)]a` | test_paragraph_extra_g6 |
|L13ai|Inline image w/ matching label inside of shortcut link| `a[foo ![bar](/url2)]a` | test_paragraph_extra_g6a |
|L14  |Full link w/ matching reference inside of shortcut link| `a[foo [bar2][bar]]a` | test_paragraph_extra_g7 |
|L14i |Full image w/ matching reference inside of shortcut link| `a[foo ![bar2][bar]]a` | test_paragraph_extra_g7a |
|L14a |Full link w/o matching reference inside of shortcut link| `a[foo [bar][bar]]a` | test_paragraph_extra_g8 |
|L14ai|Full image w/o matching reference inside of shortcut link| `a[foo ![bar][bar]]a` | test_paragraph_extra_g8a |
|L15  |Collapsed link w/ matching reference inside of shortcut link| `a[foo [bar][]]a` | test_paragraph_extra_h0 |
|L15i |Collapsed image w/ matching reference inside of shortcut link| `a[foo ![bar][]]a` | test_paragraph_extra_h0a |
|L15a |Collapsed link w/o matching reference inside of shortcut link| `a[foo [bar2][]]a` | test_paragraph_extra_g9 |
|L15ai|Collapsed image w/o matching reference inside of shortcut link| `a[foo ![bar2][]]a` | test_paragraph_extra_g9a |
|L16  |Shortcut link w/ matching reference inside of shortcut link| `a[foo [bar]]a` | test_paragraph_extra_h2 |
|L16i |Shortcut image w/ matching reference inside of shortcut link| `a[foo ![bar]]a` | test_paragraph_extra_h2a |
|L16a |Shortcut link w/o matching reference inside of shortcut link| `a[foo [bar2]]a` | test_paragraph_extra_h1 |
|L16ai|Shortcut image w/o matching reference inside of shortcut link| `a[foo ![bar2]]a` | test_paragraph_extra_h1a |
