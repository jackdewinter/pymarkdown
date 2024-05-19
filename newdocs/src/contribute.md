---
summary: How to contribute to the application.
authors:
  - Jack De Winter
---

# Contributing

Thanks for your interest in contributing to this application!

## How To Go About Helping Us

Let us say that you have a great idea on what you want to see happen with the PyMarkdown
project.  You submit it to our [issues list](https://github.com/jackdewinter/pymarkdown/issues),
and we tell you it is going to be a long time before we get to it.  Or we say
that it does not fit the direction we have for the project.

What do you do next?

The first thing is to understand our feedback.  We carefully look at
[each issue](./index.md/#what-to-do-next) and try and be as honest and sincere
with our feedback as possible. Our goals are primarily focused on being one
of the best Markdown linters out there.  While something may be a critical
issue for you, it is possible that it does not carry the same importance for
us.

That is where your contributions to the project can help.  We have a small
team that works on this project, and we must prioritize based on that
team.  If you volunteer to help, we can provide guidance and help to you
at a low cost to us.  If what you want to do is not contrary to the direction of
the project, we can usually work something out to help you meet your needs.
  
<!--- pyml disable-next-line no-emphasis-as-heading-->
**OR**  
  
Let us say that you want to get involved with a project and help.  You
are looking for something you can [sink your teeth into](https://dictionary.cambridge.org/dictionary/english/sink-teeth-into)
but are not sure you would be a good fit for this project.  Or you want to have
open-source contributions on your resume because it looks good.  Or...

If you are sincere about helping and can collaborate effectively with our
team, we will work with you to see how you can help us out.

## Are There Any Guidelines?

Yes, definitely.  And we are relaxed about most of our guidelines.  But there
are certain things we will not budge on.

### Test Coverage

We worked hard to ensure that our project has 100% code coverage and near 100%
scenario coverage.  Getting the code covered is usually the easy part.  Getting
every scenario for every element is painful.  By being very stringent about this
upfront, we hope we reduce the number of errors reported by our
users when using our application.

### Static Project Analysis

We are big proponents of static project analysis.  Static project analysis
is the parent group that includes static code analysis but extends that analysis
to the other aspects of the project.  For our team, this means running the
`clean.cmd` script before creating a Pull Request.

Why are we using a script instead of putting everything in our Pre-Commit
configuration?  To be honest, a bit of it is time and a bit of it is a control
issue.  The script allows us to turn various checks on and off more easily,
allowing us to run the script more frequently during development.  However,
we are actively trying to move our analysis tasks from our `clean.cmd` script
into our Pre-Commit scan, but
that is a work in progress.  Our plans included keeping the `clean.cmd`
script around to provide the control we need while delegating as much of
the organization to Pre-Commit as possible.

### One Major Change Per Pull Request

One pull request, one change.  Simple.  A minor change in another area that you
honestly found while making your change?  Probably acceptable.  A Pull Request
with a title that includes too many "and" phrases. Probably not acceptable.

Electrons are cheap.  Focus on merging one complete concept, and then
work on the merge for the next concept.  Remember the [KISS principle](https://en.wikipedia.org/wiki/KISS_principle):
Keep it simple... silly.

## Types of Contributions

Our contributions generally fall into three categories.  These are not the
only categories, just the most frequently asked for ones.

### Adding A New Configuration Value To An Existing Rule

"This rule is just what I want, except that it does not do..."  

If the thing that it does not do is aligned with the purpose of the rule, we
are all for adding configuration options.  One of main problems our team has with
other Markdown linters is that there are rules that look for one thing with a side
effect of looking for something else.  If the configuration option is aligned with
the rule, no problem.  Otherwise, we will direct you to create a new rule
based off an existing rule that focuses on that one thing that you want it to do.

### Add A New Rule

"I wish there was a rule that would check for..."

This is an extension of the last section on new configuration, just with larger
scope.  We believe that each rule should have a single purpose and single thing
that it triggers on.  Configuration values can be used to supplement that single
purpose but must remain aligned with the rule's purpose.

It should also be noted that the best way to propose a new rule is to do research
and have a description that is well thought out.  We typically start our rule
development by writing the rule description page first, writing the Python
code only after we are sure of the requirements.  This is not required, but we
find it helps us out immensely.

### Add A New Extension

"Doesn't PyMarkdown support the ability to do... that I use on my website?"  

There is an apt quote from an old song by Herman's Hermits titled "I'm Henery the
Eighth, I Am" which goes:

> Second verse same as the first, a little bit louder and a little bit worse.

That quote is very applicable here.  For extensions, the scope is typically larger
than a plugin rule, with more things to consider.  For example, the existing
[Pragmas Extension](./extensions/pragmas.md)
had to inject itself high up in the parsing process to ensure that it could be
taken care of before anything else.  Other extensions, such as the
[StrikeThrough Extension](./extensions/strikethrough.md),
leveraged the existing inline emphasis code by adding other emphasis options.

And then there are the scenario tests.  One of our project team's core tenets is
that everything should be tested to the extent of our abilities. That means envisioning
both the good and bad ways in which the extension can be used.  It is not an immense
effort, just a very thorough effort.

## Still Here?

If none of this has scared you off, you may want to consider helping our team
out with the development of this project.  Even if it is only for a small
rule change, a small rule, or an extension, we can help you learn what you need
to contribute.
