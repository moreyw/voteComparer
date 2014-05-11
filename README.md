voteComparer
============

A simple script to compare votes of pairs of Representatives/Senators of the US congress.
Will prompt user to enter the name of the Rep/Sen that should be searched for. Will output a .csv file with all of the votes that the members voted together on.

============

Run voteComparer.py using Python 2.7

Currently uses the Sunlight Foundaiton API (http://sunlightfoundation.com/api/) to access the voting history of different members of the US House and Senate, and then compare their votes on all of the bills that they both voted on. 

Requires an Sunlight Foundation API key, which can be obtained at the Snlight Foundation website (http://sunlightfoundation.com/api/accounts/register/).

Once an API Key has been obtained, it should be placed in the variable on line 6.

Currently only access votes from 2009-Present.

Last updated: May 2013
