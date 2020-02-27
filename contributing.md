# Contributing to Ada

:+1::tada: Thank you very much for taking the time to contribute! :tada::+1:

## Questions

Please don't hesitate to submit any questions as tickets on github!

## Feature Requests, Bug Reports, Ideas

Same as for questions, please submit your feature requests, ideas and bug reports as tickets on github. Any such contribution is very much appreciated as it helps to improve this project further.

## Pull Requests

Please fork the repo, create a branch for your changes and submit a pull request.
Pull requests should follow the below conventions.
Also note that we are always squashing when merging the PRs so don't worry about the number of commits on your PR.

## Compatibility

We want to keep this library backwards compatible to python 2.7 for now. The reason is that most vfx software currently runs on VFX Platform 2019 and the VFX industry is only moving to Python 3 from 2020 so with that that being said, we also aim for compatibility with python 3.6+. But there is no coverage for this at the moment and no way to test it within any DCC's.

## Unittests

We have some, reliable tests for Nuke and we want to keep it that way, so please write sufficient tests for your contributions for your DCC's and where possible we also want to keep the coverage at 100%. 

### Travis
I'd love to get Travis running the tests on the core module for Ada but I don't have time, but maybe you do!


## Coding styleguide

We generally follow [pep8](https://www.python.org/dev/peps/pep-0008/) using the [black](https://github.com/psf/black) code linter with these additional requirements:

- For docstrings please use the [google style](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings)

# Next Steps: Become a Collaborator on github

If you have made some contributions already and want to become more involved in the project please don't hesitate to ask about becoming a collaborator.
