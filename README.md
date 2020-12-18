# alma_xml_creator

This script is intended to create XML files for import to the Unified Resource Management System 
[Alma](https://knowledge.exlibrisgroup.com/Alma/Product_Documentation/010Alma_Online_Help_%28English%29/010Getting_Started/010Alma_Introduction/010Alma_Overview)
in the form of a collection of MARC21 records.

# General Information

## Input

The expected Input is a semicolon-delimited and utf-8 encoded csv file with the following structure:
* One column per field
* File needs to have a header of the following format:
    * "LDR" or "leader" for the leader field
    * Tag-number for controlfields
    * Tag-number and both indicators with no delimiters for datafields (e. g. "24500")
    * Any columns with a heading not matching these conditions will be discarded and an error thrown to indicate that
* The content of datafields must be given in the following format:
    * Subfield-Contents with "$$" prefix, followed by the subfield's code and finally its content
    * If there is more than one subfield, they must be provided without any delimiters (e. g. "$$aeng$$aspa")
* If your data might contain semicolons, add quotation marks around the CSV's data cells
    
## Output

Only the information given will be added to the XML, except for the document declaration, which will always be added.

For Subfields please consider the following:

Leading "$" characters are discarded and all "$$" are handled as delimiters. So in theory you could provide the
subfield without the leading "$$", but the first character of the string will have to be the subfield's code.
Otherwise the script will take the first character of your subfield's content to be its code, as there is no way to
tell which subfield it was intended to be.

## Example

Imagine a file like the following, called `test.csv`:

```csv
041  ;1001 ;24500
$$ager;$$aMuster, Sasha;$$aTesttitel
$$ager$$aeng;$$aMuster, Sasha;$$aTesttitel$$bTest title : in two languages /$$cedited by Ryan Public
```

The script's output sould look like this:

```xml
<?xml version='1.0' encoding='utf-8'?>
<collection><record><datafield ind1=" " ind2=" " tag="041"><subfield code="a">ger</subfield></datafield><datafield ind1="1" ind2=" " tag="100"><subfield code="a">Muster, Sasha</subfield></datafield><datafield ind1="0" ind2="0" tag="245"><subfield code="a">Testtitel</subfield></datafield></record><record><datafield ind1=" " ind2=" " tag="041"><subfield code="a">ger</subfield><subfield code="a">eng</subfield></datafield><datafield ind1="1" ind2=" " tag="100"><subfield code="a">Muster, Sasha</subfield></datafield><datafield ind1="0" ind2="0" tag="245"><subfield code="a">Testtitel</subfield><subfield code="b">Test title : in two languages /</subfield><subfield code="c">edited by Ryan Public</subfield></datafield></record></collection>
```

Note that there is no pretty printing, meaning no line breaks and no indentation. Open the file in any web browser
or in an editor with XML-functionality to make it more human readable.

#Usage

```bash
python create_xml test.csv test.xml
```

Input is provided as the first argument, output as the second.