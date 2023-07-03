# Assignment4
WEB: https://6332-assign4.azurewebsites.net/

Description:
You have been using data sets for assignments where you have counted number
of occurrences, largest, smallest, and other analysis which you have done with
a database, a web interface, and some application programming (or “logic”.)
While very common and useful, tables, charts, and lists of numbers are tedious
to read.
It is difficult to find meaning in large volumes of “textual” output, most users
prefer pictures: graphs, pie charts, and other graphical representations.
Various mechanisms for visualizing data within a browser, which are “light weight”
and require no plugins, or additional (local) downloads support showing results
which are easy to read and understand.
(Free) supporting tools and libraries include:
Javascript:
d3js.org -- recommended, widely used, easy to use
InfoVis: philogb.github.io/jit/demos.html
js.cytoscape.org
Other:
developers.google.com/chart/
www.highcharts.com (HTML5)
A survey and comparison is:
creativebloq.com/features/amazing-graphical-javascript-frameworks
Your assignment is to visualize and display the results from your previous assignment
within a browser, allow a user to select intervals or attributes in a data set, show
results as a pie chart, a histogram, or a scatter or point chart (possibly connected:
with a line).
That is, using those SQL tables to do queries, and rather than display the results
as text, display results as an image (a picture).
Users of this service will interact with your service through web page
interfaces, all processing and web service hosting is (of course) cloud based.
Additional Details:
A user should be able to do a query through a web interface, and see the graphical
results in a browser.
This should require no “local” install (in other words, local installs
such as Tableau are really nice, but cost money, don’t run on a phone, and are
otherwise limiting.)
Creating a static image on a server (service) and sending that image
(such as a JPG or (mostly) PDF) have either similar problems
or are not very “expressive”.
Producing (creating) JavaScript is more flexible, robust, and has many other
advantages.
Sample queries might be:
From the quake dataset, show the number of quakes for magnitude below 1, 1 to 2,
2 to 3, up to magnitude 5.
Show a Pie Chart with each pie slice in a different color, with labels (totals)
outside each pie slice.
Perhaps a bar chart (horizontal bars or vertical bars) is easier to understand.
Perhaps putting the totals inside each pie slice (or bar) is better.
What would a graph of magnitude against depth for the 100 recent quakes look like?
(point chart or scatter chart)
Note: How much of the screen area should those graphics occupy?
(Too small looks bad, too large requires scrolling.)
What colors should you use?
Where should labels go: inside bars, outside, left, right?
Labels for axis (point charts) on X and Y axis?
Please, submit through Canvas.
All work must be your own.
