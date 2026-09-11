## Read me for Sorting animation

The file contains Python app integration for animation of six sorting algoritms:
- Bubble sort
- Insertion sort
- Merge sort
- Quick sort
- Heap sort
- Bucket sort

For the purpose of animation we define bars of variable heights, each bar's height is proportional to a  number from a set of randomly generated numbers. The numbers being considered for compare and swap are colored differently from the inital colors of the bars which clearly indicates the steps of the sorting five sorting algorithms excluding the Bucket sort. In Quick sort the pivot element is indicated by red bar. In Bucket sort the bars being includded in the same bucket. Since, the random numbers belong to a small range [50, 400] some bars may look very small compared to largest bar in viewing area. However, the user may adjust the range in order to adjust the browser window size and spread. The user also can control the width of the bars by choosing the number of elements according to animation area requirements, but the default size of display is 10 bars. The animation requires basically three files:
- sort_class.py: The basic class file for the sorting algorithms
- app_all-sorts.py: The Python specifications for app routes.
- index.html

The index.html should be placed in directory <strong>templates</strong> which is the child of the directory in which the Python files would be placed. THe user can restructure index.html file into three separate files:
- CSS style file which should be placed in a child directory like templates and named as <strong>static</strong>
- Jave Script file again in static directory and with extension .js
- index.html should include both files from static directory.

The suggested restructures cleans html file from script and style and script from style. Style file is related to presentation in look of text in the animation and allows the user to control them according to the aesthetics that user cares about.
