---
title: Reporting Issues
summary: How To Report Issues To Our Team
authors:
  - Jack De Winter
---

## Reporting Issues

If you find anything wrong when using the project or if you have a feature
suggestion for the project, please consider using our
[Issues List](https://github.com/jackdewinter/pymarkdown/issues) to let us know
about your scenario. Before submitting a new issue, please follow these steps:

1. **Clearly identify the problem that you plan to report**.  
   We ask you to
   report your problem with as much clarity as possible, with the goal of
   enabling our team to replicate the problem. If possible, try to narrow down
   all aspects of the problem, especially the command line, the configuration,
   and the Markdown document that causes the application to fail. The ideal
   problem report has a good description and a single command line, distinct
   configuration (command line or configuration file), and a Markdown document
   that is between 1 and 10 lines long that illustrates the
   problem.  
   **OR**  
   **Clearly identify the feature that you would like our
   team to consider.**  
   As with an issue, try and state the feature request
   with as much clarity as possible to enable our team to understand what your
   goal is. Any examples or references that you can provide us with will help us
   decide on the merit of the feature.
1. **Check our project documentation.**  
   Please take the time to double check
   through all the project documentation to ensure that the issue is not
   already addressed by the project documentation. For a problem, it might be
   that our documentation is not as clear as it needs to be, leading to the
   problem that you want to report. For a feature, it may already be present
   in the document, but in a form or location that you feel is not easy to
   find. In either case, feel free to change your issue into a documentation
   issue and submit it as such.
1. **Check our Frequently Asked Questions document.**  
   Consult our
   [Frequently Asked Questions](./faq.md)
   document to see if your issue is a common issue or related to a common
   issue. This document will either solve your problem or help you be more
   specific in your definition of the issue if you submit a new issue.
1. **Check that the issue is not already present in our backlog.**  
   Goto our
   [Issues List](https://github.com/jackdewinter/pymarkdown/issues), remove
   the `is:open` text from the filter selection, and press enter. Then try
   various search terms to look for any issues that are related to your issue.
   If you find an issue that is like your issue, try to provide more
   information on your scenario and how it applies to that issue. If you
   believe that your issue is distinct enough from that issue to call for its
   own issue, remember the issues you found and why you believe your issue is
   distinct from those issues. That information is particularly useful to note
   when submitting your issue.
1. **Submit your issue.**  
   Finally, file the issue in our
   [Issues List](https://github.com/jackdewinter/pymarkdown/issues). Note that
   we pre-populate our issues with lists to help you follow these steps before
   submitting the issue. Note that saying you did follow the process when you
   did not is usually frowned upon.

## Our Triage Process

Roughly once a week, we look at all recently submitted issues. As a first pass,
we go through each issue and figure out if the reporter has followed the process
outlined in the prior section. If not, we simply ask them to do their due
diligence before we look at it further. Our goal is to make sure that we have a
solid requirement from the user: either a reproducible issue or a
well-documented feature request.

Once we are confident that we understand the issue, we check to see if we can
either reproduce the problem or decide if other users would likely find benefit
from the proposed feature. For new features, this may incur multiple
communications with the requester to properly understand the requirements before
making our final decision on the feature. To be clear, if we believe that the
issue has any merit, we will give the requester a fair chance to clarify their
issue before making our decision.

When we agree to work on the issue, we estimate the severity of the issue and
the amount of work that we believe will need to be done to address that issue.
We then look at our current backlog of work and use the severity and cost to
address the issue to assign it a relative position in our list.

For reference, here are examples of what that estimation process typically looks
like:

- If a problem occurs in a scenario that we believe most people will hit, the
  severity is generally high enough to place that issue near the front of our
  backlog. From there, each time we must add a new clause to the reproduction
  scenario summary, the severity is reduced. For example, "must be using
  emphasis within a list block that is nested within a block quote block" will
  cause the severity to get downgraded at least three times.
- With features, the biggest factor in our estimation is the amount of work
  needed to implement and test the feature. For a new parser extension, simple
  behavior changes are easy, with inline changes, leaf block changes, and
  container block changes increasing the effort exponentially. As a contrast,
  a new plugin rule typically has a narrowly defined scope, allowing the
  implementation and testing to be estimated as low effort.

Hopefully, that does not sound too
[wishy-washy](https://www.merriam-webster.com/dictionary/wishy-washy). A summary
of the process is: clearly state the issue, agree that our team needs to work to
address the issue, estimate the impact and cost for our team to address the
issue, and assign it an order for our team to work on the issue.
