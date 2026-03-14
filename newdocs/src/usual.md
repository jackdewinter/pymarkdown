---
title: Reporting Issues
summary: How To Report Issues To Our Team
authors:
  - Jack De Winter
---

If you find anything wrong when using the project or if you have a feature
suggestion for the project, please consider using our
[Issues List](https://github.com/jackdewinter/pymarkdown/issues)
to let us know about your issue or idea.

Before submitting a new issue, please follow these steps:

- Decide whether you are reporting a problem or requesting a feature.
- Check the project documentation.
- Check the Frequently Asked Questions.
- Check if the issue already exists in our backlog.
- Submit your issue with clear details.

In more detail:

<!-- pyml disable no-emphasis-as-heading-->
1. **Clearly identify what you plan to report**.

    **If you are reporting a problem**

    Please describe your problem as clearly as you can and narrow it down as much
    as possible. Focus on the command line, the configuration, and any supporting
    information that consistently causes the application to fail. This helps our
    team replicate the problem.

    The ideal problem report has a clear description of the problem and includes:

    - A single command line
    - A distinct configuration (either from the command line or a configuration
      file)
    - A minimal example that illustrates the problem

    **If you are requesting a feature**

    Clearly identify the feature that you would like our team to consider. As with
    an issue, try and state the feature request with as much clarity as possible
    to enable our team to understand what your goal is. Any examples or references
    that you can provide us with will help us decide on the merit of the feature.

2. **Check our project documentation.**

   Please take the time to check the project documentation. If the issue is already
   addressed there, you may not need to file a new issue. For a problem, it might
   be that our documentation is not as clear as it needs to be, leading to the
   problem that you want to report. For a feature, it may already be present
   in the document, but in a form or location that you feel is not easy to
   find. In either case, feel free to change your issue into a documentation
   issue and submit it as such.
3. **Check our Frequently Asked Questions document.**

   Consult our
   [Frequently Asked Questions](./faq.md)
   document to see if your issue is a common issue or related to a common
   issue. This document will either solve your problem or help you be more
   specific in your definition of the issue if you submit a new issue.
4. **Check that the issue is not already present in our backlog.**

   Go to our
   [Issues List](https://github.com/jackdewinter/pymarkdown/issues),
   remove
   the `is:open` text from the filter selection, and press enter. Then try
   various search terms to look for any issues that are related to your issue.
   If you find an issue that is like your issue, try to provide more
   information on your scenario and how it applies to that issue. If you
   believe that your issue is distinct enough from that issue to call for its
   own issue, remember the issues you found and why you believe your issue is
   distinct from those issues. That information is particularly useful to note
   when submitting your issue.
5. **Submit your issue.**

   Finally, file the issue in our
   [Issues List](https://github.com/jackdewinter/pymarkdown/issues).
   Note that we pre-populate our issues with lists to help you follow these steps
   before submitting the issue. Saying you followed the process when you did not
   is usually frowned upon.

<!-- pyml enable no-emphasis-as-heading-->

## Our Triage Process

Roughly once every two weeks, we look at all recently submitted issues.

In short, we:

- Check that the issue follows the reporting steps
- Confirm we understand and can reproduce (or assess) it
- Estimate its impact and effort
- Decide where it fits in our backlog

As a first
pass, we go through each issue and figure out if the reporter has followed the process
outlined in the prior section. If not, we ask them to go back and follow the steps
in the previous section before we review the issue again. Our goal is to make sure
that we have a solid requirement from the user: either a reproducible issue or a
well-documented feature request.

Once we are confident that we understand the issue, we check to see if we can
either reproduce the problem or decide if other users would likely find benefit
from the proposed feature. For new features, we often have several back-and-forth
messages with the requester so we can understand the requirements clearly before
we decide. To be clear, if we believe that the issue has any merit, we will give
the requester a fair chance to clarify their issue before making our decision.

When we agree to work on an issue, we estimate how severe it is and how much work
we believe will be needed to address it. Those two factors determine its position
in our backlog (our internal list of issues ordered by priority).

For reference, here are examples of what that estimation process typically looks
like:

- If a problem occurs in a scenario that we believe most people will hit, the
  severity is generally high enough to place that issue near the front of our
  backlog. From there, each time we must add a new clause to the reproduction
  scenario summary, the severity is reduced. For example, consider a bug that only
  occurs when you are
  using emphasis inside a list, and that list is nested inside a block quote.
  That level of nesting will cause the severity to get downgraded at least three
  times.
- With features, the biggest factor in our estimation is the amount of work
  needed to implement and test the feature. And while we can shortcut the
  work sometimes, our estimates are almost always conservative to ensure that
  we do not take on too much work.

Hopefully, that explanation is clear. A summary of the process is:

- Clearly state the issue
- Agree that our team needs to work to address the issue
- Estimate the impact and the amount of work it will take for our team to address
  the issue
- Assign it an order for our team to work on the issue
