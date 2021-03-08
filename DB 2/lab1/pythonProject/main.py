# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from lxml import etree
import io

def format_xml(file):
    root = etree.parse(file)
    items = root.xpath('//item')

    # Create the root element
    r = etree.Element('data')

    # Make a new document tree
    doc = etree.ElementTree(r)

    count = 0
    for item in items:
        url = root.xpath('//url')[count]
        # print(item.xpath('/url'))
        pageElement = etree.SubElement(r, 'page', url=url.text)
        texts = root.xpath('(//text)[$page]/value/text()', page=count + 1)
        for text in texts:
            # textElement = etree.SubElement(pageElement, 'fragment', type='text')
            textValue=text.strip()
            if textValue is not '':
                textElement = etree.SubElement(pageElement, 'fragment', type='text')
                textElement.text = textValue
        countImages = 0
        images = root.xpath('(//image)[$page]/value', page=count + 1)
        for image in images:
            countImages = countImages + 1
            textElement = etree.SubElement(pageElement, 'fragment', type='image')
            textElement.text = image.text
        print(f'Image fragments on page {count}: {countImages}')
        count = count + 1

    # Save to XML file
    outFile = open('output.xml', 'wb')
    doc.write(outFile, xml_declaration=True, pretty_print=True, encoding='utf-16')

def format_xsl(file):
    tree = etree.parse(file)
    xslt_root = etree.XML('''\
        <xsl:stylesheet version="1.0"
            xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns="http://www.w3.org/1999/xhtml">
            <xsl:output method="xml" encoding="utf-8" version="1.0" indent="yes" standalone="no" media-type="text/html" omit-xml-declaration="no" doctype-system="about:legacy-compat" />
            <xsl:template match="/items">
                <html>
                    <body>
                        <table border="1">
                            <tr>
                                <th>Description</th>
                                <th>Price</th>
                                <th>Image</th>
                            </tr>
                            <xsl:for-each select="item">
                                <tr>
                                    <td style="padding:10px"><xsl:value-of select="description"/></td>
                                    <td style="padding:10px"><xsl:value-of select="price"/></td>
                                    <td style="padding:10px" align="center">
                                        <img>
                                            <xsl:attribute name="src">
                                                <xsl:value-of select="image"/>
                                            </xsl:attribute>
                                        </img>
                                    </td>
                                </tr>
                            </xsl:for-each>
                        </table>
                    </body>    
                </html>
             </xsl:template>
         </xsl:stylesheet>''')
    transform = etree.XSLT(xslt_root)
    result = transform(tree)
    outFile = open('table.xhtml', 'wb')
    result.write(outFile, xml_declaration=True, pretty_print=True, encoding='utf-8')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pass
    format_xml("dump.xml")
    # format_xsl("moyo.xml")






# See PyCharm help at https://www.jetbrains.com/help/pycharm/
