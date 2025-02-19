
### Contributing / participating

Contributing / participating is always welcome!

Please note the following:

* Please read the [coding convention](https://github.com/testssl/testssl.sh/blob/3.2/Coding_Convention.md).
* If you have something new and/or bigger which you like to contribute, better open an issue first before you get frustrated.
* Please one pull request per feature or bug fix or improvement. Please do not mix issues.
* Documentation pays off in the long run. So please your document your code and the pull request and/or commit message.
* Please test your changes thoroughly as reliability is important for this project. You may want to check different servers with different settings.
* GitHub actions are running automatically when anything is committed. You should see any complains. Beforehand you can check with `prove -v` from the "root dir" of this project.
* If it's a new feature, please consider writing a unit test for it. You can use e.g. `t/10_baseline_ipv4_http.t` or `t/61_diff_testsslsh.t` as a template. The general documentation for [Test::More](https://perldoc.perl.org/Test/More.html) is a good start.
* If it's a new feature, it would need to be documented in the appropriate section in `help()` and in `~/doc/testssl.1.md`

If you're interested in contributing and wonder how you can help, you can search for different tags in the issues (somewhat increasing degree of difficulty):
* [documentation](https://github.com/testssl/testssl.sh/issues?q=is:issue%20state:open%20label:documentation)
* [good first issue](https://github.com/testssl/testssl.sh/issues?q=is:issue%20state:open%20label:%22good%20first%20issue%22)
* [help wanted](https://github.com/testssl/testssl.sh/issues?q=is:issue%20state:open%20label:%22help%20wanted%22)
* [for grabs](https://github.com/testssl/testssl.sh/issues?q=is:issue%20state:open%20label:%22good%20first%20issue%22)

For questions just open an issue.  Thanks for reading this!


